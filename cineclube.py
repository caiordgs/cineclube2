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
from utils import calcular_dias_restantes, formatar_tempo_restante, formatar_data_br
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
    animation: pulse 0.3s ease-in-out;
}
@keyframes pulse {
    0% { transform: scale(0.8); opacity: 0; }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); opacity: 1; }
}
.vencedor-revelacao {
    font-size: 3em;
    font-weight: bold;
    color: #FFD700;
    text-align: center;
    margin: 40px 0;
    animation: revelar 1s ease-out;
    text-shadow: 0 0 20px #FFD700, 0 0 40px #FF4B4B;
}
@keyframes revelar {
    0% { 
        transform: scale(0) rotate(-180deg); 
        opacity: 0; 
    }
    50% { 
        transform: scale(1.2) rotate(10deg); 
    }
    100% { 
        transform: scale(1) rotate(0deg); 
        opacity: 1; 
    }
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

    # Calcula tempo restante
    info_prazo = calcular_dias_restantes(filme.get("data_sorteio"), dias_limite=7)
    tempo_restante = formatar_tempo_restante(info_prazo)

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
                <p>📅 <b>Sorteado em:</b> {formatar_data_br(filme.get('data_sorteio'))}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Timer do prazo
        if info_prazo:
            if info_prazo["expirado"]:
                st.warning(tempo_restante)
            else:
                st.info(tempo_restante)

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
    st.subheader(f"🍿 Filmes na disputa ({len(st.session_state.movie_list)})")

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

            # Embaralha a lista para o efeito de roleta
            roleta = random.sample(
                st.session_state.movie_list,
                k=len(st.session_state.movie_list)
            )

            # Escolhe o vencedor antecipadamente
            vencedor = random.choice(st.session_state.movie_list)

            # Adiciona o vencedor no final algumas vezes para "parar" nele
            roleta = roleta + [vencedor] * 3

            # Efeito de desaceleração progressiva
            velocidades = []

            # Fase 1: rápido (primeiros 60%)
            num_rapido = int(len(roleta) * 0.6)
            velocidades.extend([0.05] * num_rapido)

            # Fase 2: desacelerando (próximos 30%)
            num_medio = int(len(roleta) * 0.3)
            for i in range(num_medio):
                velocidades.append(0.05 + (i * 0.02))

            # Fase 3: muito lento (últimos 10%)
            num_lento = len(roleta) - num_rapido - num_medio
            velocidades.extend([0.3] * num_lento)

            # Roda a roleta com velocidade variável
            for i, escolha in enumerate(roleta):
                placeholder.markdown(
                    f"<div class='roleta-texto'>{escolha['titulo']}</div>",
                    unsafe_allow_html=True
                )
                time.sleep(velocidades[i] if i < len(velocidades) else 0.3)

            placeholder.empty()

            # Revelação dramática do vencedor
            placeholder.markdown(
                f"<div class='vencedor-revelacao'>🎉 {vencedor['titulo']} 🎉</div>",
                unsafe_allow_html=True
            )

            # Confetti!
            st.markdown(
                """
                <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
                <script>
                    // Confetti animation
                    var duration = 3 * 1000;
                    var end = Date.now() + duration;

                    (function frame() {
                        confetti({
                            particleCount: 7,
                            angle: 60,
                            spread: 55,
                            origin: { x: 0 },
                            colors: ['#FF4B4B', '#FFD700', '#00FF00', '#00BFFF']
                        });
                        confetti({
                            particleCount: 7,
                            angle: 120,
                            spread: 55,
                            origin: { x: 1 },
                            colors: ['#FF4B4B', '#FFD700', '#00FF00', '#00BFFF']
                        });

                        if (Date.now() < end) {
                            requestAnimationFrame(frame);
                        }
                    }());
                </script>
            """, unsafe_allow_html=True
                )

            time.sleep(3)  # Deixa o vencedor visível com confetti

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