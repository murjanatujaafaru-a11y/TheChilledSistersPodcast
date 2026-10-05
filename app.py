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
# CUSTOM CSS: DOMINANT MUSTARD YELLOW & SUBTLE PURPLE ACCENTS
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Playfair+Display:ital,wght@0,600;1,400&family=Poppins:wght@300;400;600&display=swap');

    /* Main App Background - Warm Off-White / Light Cream */
    .stApp {
        background-color: #FAF6EE;
        color: #2D1A02;
        font-family: 'Poppins', sans-serif;
    }

    /* Calligraphy Title */
    .podcast-title {
        font-family: 'Great Vibes', cursive;
        color: #D48806;
        font-size: 66px !important;
        text-align: center;
        margin-bottom: -15px;
        font-weight: normal;
        text-shadow: 1px 1px 2px rgba(61, 12, 90, 0.15);
    }

    /* Subtitles & Section Titles */
    .podcast-subtitle {
        font-family: 'Playfair Display', serif;
        color: #3D0C5A;
        font-size: 24px;
        text-align: center;
        font-style: italic;
        margin-bottom: 25px;
        font-weight: 600;
    }

    h1, h2, h3 {
        color: #3D0C5A !important;
        font-family: 'Playfair Display', serif !important;
    }

    /* Cards & Containers - Mustard Border & White Base */
    [data-testid="stForm"], .css-card {
        background-color: #FFFFFF;
        border: 2px solid #E5A93C;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0px 6px 18px rgba(229, 169, 60, 0.15);
    }

    label {
        color: #2D1A02 !important;
        font-weight: 600 !important;
    }

    /* Input Field Styling */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        background-color: #FFFDF9 !important;
        border: 2px solid #E5A93C !important;
        border-radius: 8px !important;
        color: #2D1A02 !important;
    }

    input, textarea {
        color: #2D1A02 !important;
        font-weight: 500 !important;
    }

    /* Primary Mustard Buttons */
    .stButton>button {
        background-color: #E5A93C !important;
        color: #2D1A02 !important;
        border-radius: 25px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 10px rgba(229, 169, 60, 0.3);
    }

    .stButton>button:hover {
        background-color: #D48806 !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
    }

    /* Dividers */
    hr {
        border-color: #E5A93C !important;
    }

    /* Platform Links Styling */
    .platform-btn {
        display: inline-block;
        background-color: #FFFFFF;
        border: 1.5px solid #E5A93C;
        border-radius: 20px;
        padding: 8px 16px;
        margin: 4px;
        color: #3D0C5A !important;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.2s ease;
    }
    .platform-btn:hover {
        background-color: #E5A93C;
        color: #2D1A02 !important;
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
# 1. BRANDING HEADER, COVER ART & SOCIAL PLATFORM LINKS
# -------------------------------------------------------------
st.markdown('<p class="podcast-title">The Chilled Sisters Podcast</p>', unsafe_allow_html=True)
st.markdown('<p class="podcast-subtitle">Real Conversations, Good Vibes & Sisterhood</p>', unsafe_allow_html=True)

# Official Podcast Cover Image
col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
with col_img2:
    st.image(
        "https://media.rss.com/thechilledsisters/podcast_cover_20260815_102742_9c94aaeb2f6dc5c4b25a5ac571bc4efc.png",
        use_container_width=True
    )

st.write("")

# Social & Streaming Platform Badges
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 25px;">
        <a href="https://open.spotify.com/show/3KUrQmpkpufSUrybyICH0J?si=3X25a3JQTder2QpSdER00g" target="_blank" class="platform-btn">🎧 Listen on Spotify</a>
        <a href="https://podcasts.apple.com/us/podcast/the-chilled-sisters-podcast/id1702086052" target="_blank" class="platform-btn">🎙️ Apple Podcasts</a>
        <a href="https://www.instagram.com/thechilledsisterspodcast?stkn=MWJkbGt5OWJ5cmZlNQ==" target="_blank" class="platform-btn">📸 Instagram</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Host Bio & About Section
with st.expander("✨ About The Hosts & Show"):
    st.write(
        "Welcome to **The Chilled Sisters Podcast**! Join us every week for unfiltered, funny, "
        "and deeply relatable chats on life, relationships, career, personal growth, and everything in between. "
        "Grab your favorite drink and kick back with us!"
    )

st.divider()

# -------------------------------------------------------------
# 2. FEATURED EPISODE & AUDIO PLAYER
# -------------------------------------------------------------
try:
    episode_data = conn.read(worksheet="currentEpisode", ttl="1m")
    title = episode_data.loc[episode_data['key'] == 'title', 'value'].values[0]
    audio_url = episode_data.loc[episode_data['key'] == 'audio_url', 'value'].values[0]
    timestamps = episode_data.loc[episode_data['key'] == 'timestamps', 'value'].values[0]

    st.subheader(f"🎧 Latest Episode: {title}")
    
    # Audio Player
    st.audio(audio_url)
    
    # Show Notes & Timestamps
    with st.expander("📌 Show Notes & Timestamps"):
        st.markdown(timestamps)

except Exception:
    st.subheader("🎧 Featured Episode")
    st.info("Loading latest episode details...")

# -------------------------------------------------------------
# 3. INTERACTIVE EPISODE POLL & QUICK RATING
# -------------------------------------------------------------
st.divider()
st.subheader("📊 Episode Reaction & Quick Poll")

col_poll1, col_poll2 = st.columns(2)

with col_poll1:
    rating = st.select_slider(
        "Rate today's episode:",
        options=["⭐ 1", "⭐⭐ 2", "⭐⭐⭐ 3", "⭐⭐⭐⭐ 4", "⭐⭐⭐⭐⭐ 5"],
        value="⭐⭐⭐⭐⭐ 5"
    )

with col_poll2:
    poll_choice = st.radio(
        "Should we do a Part 2 on this topic?",
        ["Yes, absolutely!", "No, move to a new topic", "Maybe later"]
    )

# -------------------------------------------------------------
# 4. OPTIONAL ANONYMOUS STORY & CONFESSION BOX
# -------------------------------------------------------------
st.divider()
st.subheader("📬 Listener Messages & Confession Box (Optional)")
st.write(
    "Have something you'd like to share, ask, or confess for an upcoming episode? "
    "Feel free to leave a message below. You can submit anonymously or leave your name!"
)

with st.form("listener_feedback_form", clear_on_submit=True):
    is_anonymous = st.checkbox("🕵️ Submit anonymously", value=True)
    
    if not is_anonymous:
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name / Alias", placeholder="e.g. Mary from Abuja")
        with c2:
            location = st.text_input("City / Location", placeholder="e.g. Lagos, Nigeria")
    else:
        name = "Anonymous Listener"
        location = "Confidential"

    story_input = st.text_area(
        "Message, Question, or Confession (Optional)",
        placeholder="Type your story, thoughts, or questions for the hosts here...",
        height=130
    )
    
    submitted = st.form_submit_button("✨ Submit Feedback & Poll Response")

# Submit Data to Google Sheets
if submitted:
    try:
        existing_data = conn.read(worksheet="Sheet1", ttl=0)
        numeric_rating = rating.split(" ")[0].count("⭐")
        
        new_entry = pd.DataFrame([{
            "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Location": location,
            "Rating": numeric_rating,
            "Poll_Answer": poll_choice,
            "Feedback_Question": story_input if story_input.strip() else "N/A"
        }])
        
        updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        
        st.success("💛 Thank you for tuning in and sharing your thoughts!")
        st.balloons()
        
    except Exception as e:
        st.error("Could not save your response right now. Please try again later!")

# -------------------------------------------------------------
# 5. NEWSLETTER SUBSCRIPTION FOOTER
# -------------------------------------------------------------
st.divider()
st.subheader("💌 Join The Chilled Sisters Squad")
st.write("Never miss an episode drop, live Q&A session, or exclusive merch release!")

col_email1, col_email2 = st.columns([2, 1])
with col_email1:
    email_sub = st.text_input("Email Address", placeholder="e.g. sisterhood@example.com", label_visibility="collapsed")
with col_email2:
    sub_btn = st.button("Subscribe")

if sub_btn:
    if email_sub and "@" in email_sub:
        st.success("🎉 You're subscribed! Welcome to the family.")
    else:
        st.warning("Please enter a valid email address.")