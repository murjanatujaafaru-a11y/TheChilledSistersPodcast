import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# -------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(
    page_title="The Chilled Sisters Podcast",
    page_icon="🎙️",
    layout="centered"
)

# -------------------------------------------------------------
# CUSTOM CSS: CALLIGRAPHY & PURPLE / MUSTARD YELLOW PALETTE
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Playfair+Display:ital,wght@0,600;1,400&family=Poppins:wght@300;400;600&display=swap');

    /* Background & Main Body */
    .stApp {
        background-color: #FAF5FF;
        color: #36013F;
        font-family: 'Poppins', sans-serif;
    }

    /* Calligraphy Title */
    .podcast-title {
        font-family: 'Great Vibes', cursive;
        color: #4B0082;
        font-size: 64px !important;
        text-align: center;
        margin-bottom: -15px;
        font-weight: normal;
        text-shadow: 1px 1px 2px rgba(229, 169, 60, 0.3);
    }

    /* Subtitles & Episode Headers */
    .podcast-subtitle {
        font-family: 'Playfair Display', serif;
        color: #D48806;
        font-size: 24px;
        text-align: center;
        font-style: italic;
        margin-bottom: 25px;
        font-weight: 600;
    }

    h1, h2, h3 {
        color: #4B0082 !important;
        font-family: 'Playfair Display', serif !important;
    }

    /* Form Container */
    [data-testid="stForm"] {
        background-color: #FFFFFF;
        border: 2px solid #E5A93C;
        border-radius: 18px;
        padding: 30px;
        box-shadow: 0px 8px 20px rgba(75, 0, 130, 0.1);
    }

    label {
        color: #36013F !important;
        font-weight: 600 !important;
    }

    /* Input Field Styling */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        background-color: #FAF5FF !important;
        border: 2px solid #4B0082 !important;
        border-radius: 10px !important;
        color: #36013F !important;
    }

    input, textarea {
        color: #36013F !important;
        font-weight: 500 !important;
    }

    /* Mustard Yellow Accent Buttons */
    .stButton>button {
        background-color: #E5A93C !important;
        color: #36013F !important;
        border-radius: 25px !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 12px 28px !important;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 10px rgba(229, 169, 60, 0.4);
    }

    .stButton>button:hover {
        background-color: #4B0082 !important;
        color: #E5A93C !important;
        transform: translateY(-2px);
    }

    /* Divider Lines */
    hr {
        border-color: #E5A93C !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# GOOGLE SHEETS CONNECTION
# -------------------------------------------------------------
conn = st.connection("gsheets", type=GSheetsConnection)

# -------------------------------------------------------------
# 1. DYNAMIC EPISODE HEADER & AUDIO PLAYER
# -------------------------------------------------------------
st.markdown('<p class="podcast-title">The Chilled Sisters Podcast</p>', unsafe_allow_html=True)

try:
    # Read episode metadata from Google Sheet
    episode_data = conn.read(worksheet="currentEpisode", ttl="1m")
    
    title = episode_data.loc[episode_data['key'] == 'title', 'value'].values[0]
    audio_url = episode_data.loc[episode_data['key'] == 'audio_url', 'value'].values[0]
    timestamps = episode_data.loc[episode_data['key'] == 'timestamps', 'value'].values[0]

    st.markdown(f'<p class="podcast-subtitle">{title}</p>', unsafe_allow_html=True)
    
    # Dynamic MP3 Audio Player
    st.audio(audio_url)
    
    # Timestamps & Highlights
    with st.expander("📌 Episode Timestamps & Highlights"):
        st.markdown(timestamps)

except Exception:
    st.markdown('<p class="podcast-subtitle">Welcome to Our Latest Episode</p>', unsafe_allow_html=True)

st.divider()

# -------------------------------------------------------------
# 2. EPISODE RATING & ANONYMOUS STORY / CONFESSION BOX
# -------------------------------------------------------------
st.subheader("📬 Rate This Episode & Share Your Story")
st.write(
    "Let us know what you thought of today's episode! You can also share a personal story, "
    "relationship dilemma, or secret confession for us to read on air."
)

with st.form("listener_feedback_form", clear_on_submit=True):
    # Episode Rating System
    rating = st.select_slider(
        "⭐ How would you rate this episode?",
        options=["⭐ 1 - Needs Work", "⭐⭐ 2 - Fair", "⭐⭐⭐ 3 - Good", "⭐⭐⭐⭐ 4 - Great!", "⭐⭐⭐⭐⭐ 5 - Amazing!"],
        value="⭐⭐⭐⭐⭐ 5 - Amazing!"
    )
    
    st.markdown("---")
    
    # Anonymity Option
    is_anonymous = st.checkbox("🕵️ Submit anonymously", value=True)
    
    if not is_anonymous:
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name / Alias", placeholder="e.g. Mary from Abuja")
        with col2:
            location = st.text_input("City / Location", placeholder="e.g. Lagos, Nigeria")
    else:
        name = "Anonymous Listener"
        location = "Confidential"

    # Story & Confession Input Box
    story_input = st.text_area(
        "Your Story, Confession, or Personal Question for the Hosts",
        placeholder="Type your story, thoughts on the episode, or a situation you want us to talk about...",
        height=160
    )
    
    submitted = st.form_submit_button("✨ Submit Rating & Story")

# -------------------------------------------------------------
# 3. SAVE SUBMISSION TO GOOGLE SHEETS
# -------------------------------------------------------------
if submitted:
    try:
        existing_data = conn.read(worksheet="Sheet1", ttl=0)
        
        # Clean up rating value for clean dataset recording (e.g., "5")
        numeric_rating = rating.split(" ")[0].count("⭐")
        
        new_entry = pd.DataFrame([{
            "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Location": location,
            "Rating": numeric_rating,
            "Poll_Answer": "Episode Review & Story",
            "Feedback_Question": story_input
        }])
        
        updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        
        st.success("💜 Thank you! Your rating and story have been recorded.")
        st.balloons()
        
    except Exception as e:
        st.error("Could not save your feedback right now. Please try again later!")