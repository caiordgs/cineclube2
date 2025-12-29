import streamlit as st
import pandas as pd
import random
import time
import os

# --- Banco de Dados ---
ARQUIVO = "filmes.csv"

def carregar():
    if os.path.exists(ARQUIVO):
        try:
            return pd.read_csv(ARQUIVO).to_dict('records')
        except: return []
    return []

def salvar(lista):
    pd.DataFrame(lista).to_csv(ARQUIVO, index=False)

# --- Configuração ---
st.set_page_config(page_title="Cine Clube", page_icon="🎬")

if 'movie_list' not in st.session_state:
    st.session_state.movie_list = carregar()

# --- CSS Corrigido (Cores Fixas para Leitura) ---
st.markdown("""
    <style>
    /* Cartão de filme na lista */
    .filme-card {
        padding: 15px; 
        background-color: #262730; 
        color: white !important; 
        border-radius: 10px;
        margin-bottom: 10px; 
        border-left: 6px solid #E50914;
    }
    .filme-card b { color: #FF4B4B !important; font-size: 1.1em; }
    .filme-card small { color: #cccccc !important; }

    /* Caixa do Vencedor */
    .vencedor-box { 
        padding: 30px; 
        border-radius: 15px; 
        background-color: #1E1E1E; 
        text-align: center; 
        border: 4px solid #FF4B4B;
        color: white !important;
    }
    .vencedor-box h1 { color: #FF4B4B !important; font-size: 3em !important; }
    
    /* Texto da Roleta */
    .roleta-texto {
        font-size: 2.5em;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Cine Clube")

# --- Cadastro ---
with st.expander("➕ Adicionar Novo Filme", expanded=False):
    c1, c2, c3 = st.columns(3)
    t = c1.text_input("Título")
    d = c2.text_input("Diretor")
    p = c3.text_input("Quem indicou?")
    
    if st.button("Salvar Filme"):
        if t and p:
            st.session_state.movie_list.append({"titulo": t, "diretor": d if d else "N/A", "pessoa": p})
            salvar(st.session_state.movie_list)
            st.rerun()

# --- Lista e Sorteio ---
if st.session_state.movie_list:
    st.subheader(f"🍿 Filmes na disputa ({len(st.session_state.movie_list)})")
    
    for f in st.session_state.movie_list:
        st.markdown(f"""
            <div class='filme-card'>
                <b>{f['titulo']}</b><br>
                <small>Direção: {f['diretor']} | Indicado por: {f['pessoa']}</small>
            </div>
        """, unsafe_allow_html=True)

    if st.button("🎲 INICIAR SORTEIO FATAL", type="primary", use_container_width=True):
        placeholder = st.empty() # Espaço que vamos atualizar para a animação
        
        # Animação de Tensão (Roleta)
        for i in range(20): # Quantas vezes vai trocar o nome
            escolha_rapida = random.choice(st.session_state.movie_list)
            placeholder.markdown(f"<div class='roleta-texto'>{escolha_rapida['titulo']}</div>", unsafe_allow_html=True)
            time.sleep(0.05 + (i * 0.02)) # Vai ficando mais lento no final
        
        vencedor = random.choice(st.session_state.movie_list)
        placeholder.empty() # Limpa a roleta
        
        st.balloons()
        st.markdown(f"""
            <div class='vencedor-box'>
                <p style='font-size: 1.2em;'>O FILME DA SEMANA É:</p>
                <h1>{vencedor['titulo']}</h1>
                <p>🎬 Direção: {vencedor['diretor']}</p>
                <p>👤 Sugestão de: <b>{vencedor['pessoa']}</b></p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("A lista está vazia! Adicione filmes para começar.")

# --- Admin Sidebar ---
st.sidebar.title("🔒 Admin")
senha = st.sidebar.text_input("Senha", type="password")
if senha == "pipoca":
    if st.sidebar.button("Limpar Lista"):
        st.session_state.movie_list = []
        if os.path.exists(ARQUIVO): os.remove(ARQUIVO)
        st.rerun()
