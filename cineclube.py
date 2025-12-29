import streamlit as st
import random
import time
import os

from tmdb import buscar_filmes, buscar_diretor, poster_url
from db import (
    carregar_filmes,
    salvar_filme,
    remover_filme,
    limpar_todos
)

# =========================
# CONFIGURAÇÕES
# =========================
st.set_page_config(page_title="🎬 Cine Clube", page_icon="🎬")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

if "movie_list" not in st.session_state:
    st.session_state.movie_list = carregar_filmes()

# =========================
# CSS
# =========================
st.markdown("""
<style>
.filme-card {
    padding: 15px;
    background-color: #262730;
    color: white;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 6px solid #E50914;
}
.filme-card b {
    color: #FF4B4B;
    font-size: 1.1em;
}
.vencedor-box {
    padding: 30px;
    border-radius: 15px;
    background-color: #1E1E1E;
    text-align: center;
    border: 4px solid #FF4B4B;
    color: white;
}
.vencedor-box h1 {
    color: #FF4B4B;
    font-size: 3em;
}
.roleta-texto {
    font-size: 2.5em;
    font-weight: bold;
    color: #FF4B4B;
    text-align: center;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.title("🎬 Cine Clube")

# =========================
# CADASTRO DE FILMES
# =========================
with st.expander("➕ Adicionar novo filme"):

    busca = st.text_input("🎥 Digite o nome do filme")

    filme_escolhido = None
    diretor = None
    poster = None

    if len(busca) >= 3:
        resultados = buscar_filmes(busca)

        if resultados:
            opcoes = {
                f"{f['title']} ({f.get('release_date','')[:4]})": f
                for f in resultados[:5]
            }

            escolha = st.selectbox("Sugestões", list(opcoes.keys()))

            filme_escolhido = opcoes[escolha]
            diretor = buscar_diretor(filme_escolhido["id"])
            poster = poster_url(filme_escolhido.get("poster_path"))

            if poster:
                st.image(poster, width=200)

            st.write(f"🎬 Diretor: **{diretor}**")

    with st.form("form_adicionar_filme", clear_on_submit=True):
        pessoa = st.text_input("👤 Quem está indicando?")
        submitted = st.form_submit_button("Adicionar ao Cine Clube 🎬")

        if submitted:
            if not pessoa:
                st.warning("Informe quem está indicando o filme.")
            elif not filme_escolhido:
                st.warning("Selecione um filme da lista.")
            else:
                salvar_filme(
                    filme_escolhido["title"],
                    diretor,
                    pessoa,
                    poster
                )
                st.session_state.movie_list = carregar_filmes()
                st.success("🎬 Filme adicionado com sucesso!")
                st.rerun()

# =========================
# LISTA DE FILMES
# =========================
if st.session_state.movie_list:
    st.subheader(f"🍿 Filmes na disputa ({len(st.session_state.movie_list)})")

    for f in st.session_state.movie_list:
        c1, c2 = st.columns([1, 4])

        with c1:
            if f.get("poster"):
                st.image(f["poster"], width=100)

        with c2:
            st.markdown(f"""
                <div class='filme-card'>
                    <b>{f['titulo']}</b><br>
                    <small>Direção: {f['diretor']} | Indicado por: {f['pessoa']}</small>
                </div>
            """, unsafe_allow_html=True)

    if st.button("🎲 INICIAR SORTEIO FATAL", type="primary", use_container_width=True):
        placeholder = st.empty()

        roleta = random.sample(
            st.session_state.movie_list,
            k=len(st.session_state.movie_list)
        )

        for escolha in roleta:
            placeholder.markdown(
                f"<div class='roleta-texto'>{escolha['titulo']}</div>",
                unsafe_allow_html=True
            )
            time.sleep(0.08)

        vencedor = random.choice(st.session_state.movie_list)
        placeholder.empty()

        st.balloons()
        st.markdown(f"""
            <div class='vencedor-box'>
                <p>O FILME DA SEMANA É:</p>
                <h1>{vencedor['titulo']}</h1>
                <p>🎬 Direção: {vencedor['diretor']}</p>
                <p>👤 Sugestão de: <b>{vencedor['pessoa']}</b></p>
            </div>
        """, unsafe_allow_html=True)

        remover_filme(vencedor["id"])
        st.session_state.movie_list = carregar_filmes()

else:
    st.info("A lista está vazia. Adicione filmes para começar.")

# =========================
# ADMIN
# =========================
st.sidebar.title("🔒 Admin")
senha = st.sidebar.text_input("Senha", type="password")

if ADMIN_PASSWORD is None:
    st.sidebar.warning("Senha de admin não configurada")
elif senha == ADMIN_PASSWORD:
    if st.sidebar.button("Limpar lista"):
        limpar_todos()
        st.session_state.movie_list = carregar_filmes()
        st.rerun()
