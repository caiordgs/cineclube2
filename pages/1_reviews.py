import streamlit as st

from db import (
	carregar_filmes_sorteados,
	salvar_review,
	carregar_reviews, review_ja_existe
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

filme_da_semana = filmes[0]




if not filmes:
    st.info("Nenhum filme sorteado ainda.")
    st.stop()

opcoes = {
    f"{f['titulo']} ({f.get('data_lancamento', '')})": f
    for f in filmes
}

labels = list(opcoes.keys())
index_padrao = labels.index(
    f"{filme_da_semana['titulo']} ({filme_da_semana.get('data_lancamento', '')})"
)

filme_label = st.selectbox(
    "🎬 Selecione o filme para review",
    labels,
    index=index_padrao
)

filme = opcoes[filme_label]

if filme["id"] == filme_da_semana["id"]:
    st.caption("⭐ Este é o filme da semana")

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

    if review_ja_existe(filme["id"], autor):
        st.warning("Você já avaliou este filme.")
    else:
        salvar_review(
            filme_sorteado_id=filme["id"],
            autor=autor,
            comentario=comentario,
            nota=nota,
            diretor=filme["diretor"]
        )
        st.success("Review salva com sucesso!")
        st.rerun()

    if enviado:
        if not autor:
            st.warning("Informe seu nome.")
        else:
            salvar_review(
                filme_sorteado_id=filme["id"],
                autor=autor,
                comentario=comentario,
                nota=nota,
                diretor=filme["diretor"]
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
