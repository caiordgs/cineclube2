import streamlit as st
import random
import time
import os

from config.env import ENV
from tmdb import buscar_filmes, buscar_diretor, poster_url
from db import (
    carregar_filmes,
    salvar_filme,
    remover_filme,
    limpar_todos,
    salvar_filme_sorteado,
    filme_ja_existe,
    carregar_filme_da_semana,
    filme_e_novo
)
from datetime import date, datetime


def normalizar_data(valor):
    if valor is None:
        return None
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    return valor


if ENV == "homologation":
    st.sidebar.warning("🧪 AMBIENTE: HOMOLOGAÇÃO")
else:
    st.sidebar.success("1.2")

# =========================
# CONFIGURAÇÕES
# =========================
st.set_page_config(page_title="Cine Clube", page_icon="🎬")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# =========================
# ESTADO
# =========================
if "movie_list" not in st.session_state:
    with st.spinner("Carregando filmes..."):
        st.session_state.movie_list = carregar_filmes()

if "filme_sorteado" not in st.session_state:
    # Busca o filme da semana do banco
    filme_da_semana = carregar_filme_da_semana()
    st.session_state["filme_sorteado"] = filme_da_semana

# =========================
# CSS
# =========================
st.markdown(
    """
<style>
.filme-card {
    padding: 15px;
    background-color: #262730;
    color: white;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 6px solid #E50914;
    position: relative;
}
.filme-card b {
    color: #FF4B4B;
    font-size: 1.1em;
}
.badge-novo {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: #00FF00;
    color: #000;
    padding: 3px 8px;
    border-radius: 5px;
    font-size: 0.7em;
    font-weight: bold;
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
.contador-destaque {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
}
.contador-destaque h2 {
    color: white;
    margin: 0;
    font-size: 2.5em;
}
.contador-destaque p {
    color: #E0E0E0;
    margin: 5px 0 0 0;
    font-size: 1.1em;
}
</style>
""", unsafe_allow_html=True
    )

# =========================
# TÍTULO
# =========================
st.title("🎬 Cine Clube")

# =========================
# FILME DA SEMANA (DESTAQUE NO TOPO)
# =========================
filme = st.session_state.get("filme_sorteado")
if filme:
    st.markdown("---")
    st.markdown("## 🏆 Filme da Semana")
    col1, col2 = st.columns([2, 3])
    with col1:
        if filme.get("poster"):
            st.image(filme["poster"], use_container_width=True)
    with col2:
        st.markdown(
            f"""
            <div class='vencedor-box'>
                <h2 style="margin-bottom:10px">{filme['titulo']}</h2>
                <p>🎬 <b>Direção:</b> {filme['diretor']}</p>
                <p>👤 <b>Sugestão de:</b> {filme['pessoa']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("---")
else:
    st.info("⏳ Ainda não há filme da semana sorteado. Aguarde o próximo sorteio!")
    st.markdown("---")

# =========================
# ADMIN (SIDEBAR)
# =========================
st.sidebar.title("🔒 Admin")
senha = st.sidebar.text_input("Senha", type="password")

if ADMIN_PASSWORD is None:
    st.sidebar.warning("Senha de admin não configurada")
elif senha == ADMIN_PASSWORD:
    if st.sidebar.button("Limpar lista"):
        with st.spinner("Limpando lista..."):
            limpar_todos()
            st.session_state.movie_list = carregar_filmes()
        st.success("Lista limpa com sucesso!")
        time.sleep(1)
        st.rerun()

# =========================
# CADASTRO DE FILMES
# =========================
with st.expander("➕ Adicionar novo filme"):
    busca = st.text_input(
        "🎥 Digite o título do filme (ou parte dele) e pressione Enter"
    )

    filme_escolhido = None
    diretor = None
    poster = None

    if len(busca) >= 3:
        with st.spinner("Buscando filmes..."):
            resultados = buscar_filmes(busca)

        if resultados:
            opcoes = {
                f"{f['title']} ({f.get('release_date', '')[:4]})": f
                for f in resultados[:5]
            }

            escolha = st.selectbox("Resultado", list(opcoes.keys()))
            filme_escolhido = opcoes[escolha]

            with st.spinner("Buscando informações do diretor..."):
                diretor = buscar_diretor(filme_escolhido["id"])

            poster = poster_url(filme_escolhido.get("poster_path"))

            if poster:
                st.image(poster, width=200)

            st.write(f"🎬 Diretor: **{diretor}**")
        else:
            st.info("Nenhum filme encontrado. Tente outro termo de busca.")

    with st.form("form_adicionar_filme", clear_on_submit=True):
        pessoa = st.text_input("👤 Quem está indicando?")
        submitted = st.form_submit_button("Adicionar ao Cine Clube 🎬")

        if submitted:
            if not pessoa:
                st.warning("Informe quem está indicando o filme.")
            elif not filme_escolhido:
                st.warning("Selecione um filme da lista.")
            elif filme_ja_existe(
                    filme_escolhido["title"],
                    diretor
            ):
                st.warning("🎬 Esse filme já consta na lista.")
            else:
                with st.spinner("Salvando filme..."):
                    salvar_filme(
                        filme_escolhido["title"],
                        diretor,
                        pessoa,
                        poster,
                        filme_escolhido.get("release_date")
                    )
                    st.session_state.movie_list = carregar_filmes()
                st.success("Filme adicionado com sucesso!")
                time.sleep(1)
                st.rerun()

# =========================
# LISTA DE FILMES
# =========================
if st.session_state.movie_list:
    # Contador destacado
    total_filmes = len(st.session_state.movie_list)
    st.markdown(
        f"""
        <div class='contador-destaque'>
            <h2>{total_filmes}</h2>
            <p>{'filme' if total_filmes == 1 else 'filmes'} na disputa</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    for f in st.session_state.movie_list:
        col_img, col_info, col_admin = st.columns([1, 4, 1])

        with col_img:
            if f.get("poster"):
                st.image(f["poster"], width=100)

        with col_info:
            # Verifica se é novo
            badge_html = ""
            if filme_e_novo(f.get("created_at")):
                badge_html = "<span class='badge-novo'>NOVO</span>"

            st.markdown(
                f"""
                <div class='filme-card'>
                    {badge_html}
                    <b>{f['titulo']}</b><br>
                    <small>
                        Direção: {f['diretor']} |
                        Indicado por: {f['pessoa']}
                    </small>
                </div>
            """, unsafe_allow_html=True
            )

        with col_admin:
            if senha == ADMIN_PASSWORD:
                if st.button(
                        "🗑️",
                        key=f"delete_{f['id']}",
                        help="Remover este filme"
                ):
                    with st.spinner("Removendo filme..."):
                        remover_filme(f["id"])
                        st.session_state.movie_list = carregar_filmes()
                    st.success("Filme removido!")
                    time.sleep(0.5)
                    st.rerun()

    # =========================
    # SORTEIO (PROTEGIDO)
    # =========================
    pode_sortear = (
            ADMIN_PASSWORD is not None
            and senha == ADMIN_PASSWORD
    )

    if not pode_sortear:
        st.button(
            "🎲 INICIAR SORTEIO!",
            type="primary",
            use_container_width=True,
            disabled=True,
            key="sortear_disabled"
        )
        st.caption("🔒 Apenas administradores podem realizar o sorteio.")
    else:
        if st.button(
                "🎲 INICIAR SORTEIO!",
                type="primary",
                use_container_width=True,
                key="sortear"
        ):
            # Loading antes do sorteio
            with st.spinner("Preparando sorteio..."):
                time.sleep(1)

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

            # Salva o vencedor com loading
            with st.spinner("Salvando resultado..."):
                st.session_state["filme_sorteado"] = vencedor

                filme_vencedor = st.session_state["filme_sorteado"]

                data_lancamento = normalizar_data(
                    filme_vencedor.get("data_lancamento")
                )

                salvar_filme_sorteado(
                    titulo=filme_vencedor["titulo"],
                    diretor=filme_vencedor["diretor"],
                    pessoa=filme_vencedor["pessoa"],
                    poster=filme_vencedor["poster"],
                    data_lancamento=data_lancamento
                )

                remover_filme(filme_vencedor["id"])
                st.session_state.movie_list = carregar_filmes()

            st.success("Sorteio realizado com sucesso!")
            time.sleep(1)
            st.rerun()

else:
    st.info("A lista está vazia. Adicione filmes para começar.")