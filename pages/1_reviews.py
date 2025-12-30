import streamlit as st

from db import (
    carregar_filmes_sorteados,
    salvar_review,
    carregar_reviews
)

st.set_page_config(
    page_title="⭐ Reviews - Cine Clube",
    page_icon="⭐"
)

st.title("⭐ Reviews dos Filmes Sorteados")

# =========================
# SELEÇÃO DO FILME
# =========================
filmes = carregar_filmes_sorteados()

if not filmes:
    st.info("Nenhum filme sorteado ainda.")
    st.stop()

opcoes = {
    f"{f['titulo']} ({f.get('data_lancamento', '')})": f
    for f in filmes
}

filme_label = st.selectbox(
    "🎬 Selecione um filme",
    list(opcoes.keys())
)

filme = opcoes[filme_label]

# =========================
# DETALHES DO FILME
# =========================
c1, c2 = st.columns([1, 3])

with c1:
    if filme.get("poster"):
        st.image(filme["poster"], width=180)

with c2:
    st.subheader(filme["titulo"])
    st.write(f"🎬 Diretor: **{filme['diretor']}**")
    st.write(f"👤 Indicado por: **{filme['pessoa']}**")
    st.write(f"📅 Sorteado em: {filme['data_sorteio'][:10]}")

st.divider()

# =========================
# FORMULÁRIO DE REVIEW
# =========================
st.subheader("✍️ Deixe sua review")

with st.form("form_review", clear_on_submit=True):
    autor = st.text_input("Seu nome")

    nota = st.select_slider(
        "Nota",
        options=[x / 2 for x in range(1, 11)],
        value=4.0
    )

    comentario = st.text_area(
        "Comentário",
        placeholder="O que achou do filme?"
    )

    enviado = st.form_submit_button("Salvar review ⭐")

    if enviado:
        if not autor:
            st.warning("Informe seu nome.")
        else:
            salvar_review(
                filme_sorteado_id=filme["id"],
                autor=autor,
                comentario=comentario,
                nota=nota
            )
            st.success("Review salva com sucesso!")
            st.rerun()

# =========================
# LISTAGEM DE REVIEWS
# =========================
st.divider()
st.subheader("🗣️ Reviews")

reviews = carregar_reviews(filme["id"])

if not reviews:
    st.info("Nenhuma review ainda para este filme.")
else:
    notas = [r["nota"] for r in reviews]
    media = round(sum(notas) / len(notas), 2)

    st.metric("⭐ Nota média", media)

    for r in reviews:
        st.markdown(
            f"""
            **{r['autor']}** — ⭐ {r['nota']}  
            {r['comentario'] or "_Sem comentário_"}
            """
        )
        st.divider()
