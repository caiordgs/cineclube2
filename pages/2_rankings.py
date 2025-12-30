import streamlit as st
from db import supabase

st.set_page_config(
    page_title="🏆 Ranking - Cine Clube",
    page_icon="🏆"
)

st.title("🏆 Ranking do Cine Clube")

# =========================
# RANKING DE FILMES
# =========================
st.subheader("🎬 Ranking de Filmes")

resp_filmes = (
    supabase
    .table("ranking_filmes")
    .select("*")
    .order("nota_media", desc=True)
    .execute()
)

ranking_filmes = resp_filmes.data or []

if not ranking_filmes:
    st.info("Ainda não há reviews suficientes para gerar ranking.")
else:
    for i, f in enumerate(ranking_filmes, start=1):
        st.markdown(
            f"""
            **{i}º — {f['titulo']}**  
            🎬 Diretor: {f['diretor']}  
            ⭐ Nota média: {f['nota_media']}  
            🗣️ Reviews: {f['total_reviews']}
            """
        )
        st.divider()

# =========================
# RANKING DE DIRETORES
# =========================
st.subheader("🎥 Ranking de Diretores")

resp_diretores = (
    supabase
    .table("ranking_diretores")
    .select("*")
    .order("nota_media", desc=True)
    .execute()
)

ranking_diretores = resp_diretores.data or []

if not ranking_diretores:
    st.info("Ainda não há reviews suficientes para gerar ranking de diretores.")
else:
    for i, d in enumerate(ranking_diretores, start=1):
        st.markdown(
            f"""
            **{i}º — {d['diretor']}**  
            ⭐ Nota média: {d['nota_media']}  
            🗣️ Reviews: {d['total_reviews']}
            """
        )
        st.divider()
