import streamlit as st
import random
import time

# --- Page Config ---
st.set_page_config(page_title="Film Club Selector", page_icon="🎬")

# --- Styling ---
st.markdown("""
    <style>
    .big-font { font-size:30px !important; font-weight: bold; color: #E50914; }
    .winner-box { 
        padding: 20px; 
        border-radius: 10px; 
        background-color: #f0f2f6; 
        text-align: center; 
        border: 2px solid #E50914;
        margin-top: 20px;
    }
    .movie-card {
        padding: 10px;
        background-color: #f9f9f9;
        border-radius: 5px;
        margin-bottom: 5px;
        border-left: 4px solid #E50914;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Title ---
st.title("🎬 Film Club Roulette")
st.write("Add movies, build the suspense, and pick the winner!")

# --- Session State to hold the list ---
if 'movie_list' not in st.session_state:
    st.session_state.movie_list = []

# --- Input Section ---
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        movie_title = st.text_input("Movie Title", placeholder="e.g. Parasite")
    with col2:
        director = st.text_input("Director", placeholder="e.g. Bong Joon-ho")
    with col3:
        recommender = st.text_input("Recommended By", placeholder="e.g. Sarah")

    if st.button("Add to List ➕"):
        if movie_title and recommender:
            # We save the data as a dictionary
            entry = {
                "title": movie_title, 
                "director": director if director else "Unknown", 
                "person": recommender
            }
            st.session_state.movie_list.append(entry)
            st.success(f"Added: {movie_title}")
        else:
            st.warning("Please enter at least the Movie Title and Recommender.")

# --- Display Current List ---
if st.session_state.movie_list:
    st.divider()
    st.subheader(f"🍿 The Bucket ({len(st.session_state.movie_list)} movies)")
    
    # Display list nicely
    for i, entry in enumerate(st.session_state.movie_list):
        st.markdown(f"""
        <div class="movie-card">
            <b>{i+1}. {entry['title']}</b> <br>
            <span style="font-size:0.9em; color:gray;">Dir. {entry['director']}</span> | 
            <span style="font-size:0.9em; color:gray;">Rec by: {entry['person']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- The Selection Mechanism ---
    if st.button("🎲 SPIN THE WHEEL! 🎲", type="primary", use_container_width=True):
        
        # 1. The Drum Roll Effect
        progress_text = "Mixing the popcorn..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.02)
            if percent_complete == 40:
                my_bar.progress(percent_complete + 1, text="Dimming the lights...")
            elif percent_complete == 80:
                my_bar.progress(percent_complete + 1, text="Checking IMDb rating...")
            else:
                my_bar.progress(percent_complete + 1)
        
        time.sleep(0.5)
        my_bar.empty()

        # 2. Select the Winner
        winner = random.choice(st.session_state.movie_list)
        
        # 3. The Reveal
        st.balloons()
        
        st.markdown(f"""
            <div class="winner-box">
                <h2>And the winner is...</h2>
                <p class="big-font">{winner['title']}</p>
                <p><i>Directed by {winner['director']}</i></p>
                <hr>
                <p>Selected by: <strong>{winner['person']}</strong></p>
            </div>
        """, unsafe_allow_html=True)

else:
    st.info("The bucket is currently empty.")

# --- ADMIN SECTION (Sidebar) ---
st.sidebar.title("🔒 Admin Controls")
st.sidebar.write("Only the host can clear the list.")

# Define your secret password here
SECRET_PASSWORD = "popcorn" 

user_password = st.sidebar.text_input("Enter Password", type="password")

if user_password == SECRET_PASSWORD:
    st.sidebar.success("Access Granted")
    if st.sidebar.button("⚠️ Clear Entire List"):
        st.session_state.movie_list = []
        st.rerun() # Refreshes the app immediately
elif user_password:
    st.sidebar.error("Wrong Password")