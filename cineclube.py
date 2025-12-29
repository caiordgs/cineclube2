import streamlit as st
import pandas as pd
import random
import time
import os

# --- Configuração do Arquivo de Dados ---
ARQUIVO_DADOS = "lista_filmes.csv"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        return pd.read_csv(ARQUIVO_DADOS).to_dict('records')
    return []

def salvar_dados(lista):
    pd.DataFrame(lista).to_csv(ARQUIVO_DADOS, index=False)

# --- Configuração da Página ---
st.set_page_config(page_title="Cine Clube - Seletor", page_icon="🎬")

# --- Estilização Customizada ---
st.markdown("""
    <style>
    .big-font { font-size:35px !important; font-weight: bold; color: #E50914; }
    .winner-box { 
        padding: 25px; 
        border-radius: 15px; 
        background-color: #f0f2f6; 
        text-align: center; 
        border: 3px solid #E50914;
        margin-top: 25px;
    }
    .movie-card {
        padding: 12px;
        background-color: #ffffff;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 5px solid #E50914;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Inicialização do Estado ---
if 'movie_list' not in st.session_state:
    st.session_state.movie_list = carregar_data()

# --- Título ---
st.title("🎬 Cine Clube: Roleta de Filmes")
st.write("Adicione as sugestões e prepare a pipoca!")

# --- Seção de Entrada ---
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        titulo = st.text_input("Título do Filme", placeholder="Ex: Parasita")
    with col2:
        diretor = st.text_input("Diretor(a)", placeholder="Ex: Bong Joon-ho")
    with col3:
        quem_indicou = st.text_input("Indicado por", placeholder="Ex: Maria")

    if st.button("Adicionar à Lista ➕"):
        if titulo and quem_indicou:
            novo_filme = {
                "titulo": titulo, 
                "diretor": diretor if diretor else "Não informado", 
                "pessoa": quem_indicou
            }
            st.session_state.movie_list.append(novo_filme)
            salvar_dados(st.session_state.movie_list)
            st.success(f"'{titulo}' adicionado com sucesso!")
            st.rerun()
        else:
            st.warning("Por favor, preencha pelo menos o Título e quem indicou.")

# --- Exibição da Lista Atual ---
if st.session_state.movie_list:
    st.divider()
    st.subheader(f"🍿 Filmes no Balde ({len(st.session_state.movie_list)})")
    
    for i, filme in enumerate(st.session_state.movie_list):
        st.markdown(f"""
        <div class="movie-card">
            <b>{i+1}. {filme['titulo']}</b> <br>
            <span style="font-size:0.9em; color:gray;">Dir: {filme['diretor']}</span> | 
            <span style="font-size:0.9em; color:gray;">Sugestão de: <b>{filme['pessoa']}</b></span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- Mecanismo de Sorteio ---
    if st.button("🎲 SOR

