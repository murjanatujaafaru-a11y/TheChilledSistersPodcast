from datetime import datetime
import pandas as pd
import gspread
import streamlit as st

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="The Chilled Sister's Podcast", page_icon="🎙️", layout="centered"
)

st.title("🎙️ The Chilled Sister's Podcast")
st.caption(
    "New episodes every Friday! Listen, share your thoughts, and get featured on air."
)

st.divider()

# --- GOOGLE SHEETS CONNECTION & DYNAMIC EPISODE FETCH ---
secrets_data = st.secrets["connections"]["gsheets"]
spreadsheet_url = secrets_data["spreadsheet"]
creds_dict = {k: v for k, v in secrets_data.items() if k != "spreadsheet"}

gc = gspread.service_account_from_dict(creds_dict)
sh = gc.open_by_url(spreadsheet_url)

# Load dynamic episode details from the 'CurrentEpisode' tab
try:
    episode_sheet = sh.worksheet("CurrentEpisode")
    data = episode_sheet.get_all_records()
    
    # Convert list of dicts to key-value mapping
    ep_data = {row["key"]: row["value"] for row in data}
    
    ep_title = ep_data.get("title", "Latest Episode")
    ep_audio = ep_data.get("audio_url", "")
    ep_timestamps = ep_data.get("timestamps", "")
except Exception:
    # Fallback default values if sheet isn't loaded yet
    ep_title = "Episode 117: when did you realize you can never marry him?"
    ep_audio = "https://content.rss.com/episodes/223625/3164519/thechilledsisters/2026_09_18_13_53_06_6f734125-3f0e-499a-b54f-5af1b94dedb6.mp3"
    ep_timestamps = "- **02:15** — Introduction\n- **14:30** — Conversions\n- **28:10** — Q&A"

# --- 2. LATEST EPISODE SECTION ---
st.header("🎧 This Week's Episode")
st.subheader(ep_title)

# Direct MP3 Audio Streaming
if ep_audio:
    st.audio(ep_audio)

with st.expander("📝 View this week's Takeaways & Timestamps"):
    st.markdown(ep_timestamps)

st.divider()

# --- 3. LISTENER FEEDBACK FORM ---
st.header("💬 Log Your Feedback & Submit Questions")
st.write(
    "Have a question or comment about this episode? Submit it below to get featured on next Friday's episode!"
)

with st.form("listener_feedback_form"):
    listener_name = st.text_input("Your Name or Social Handle")
    listener_location = st.text_input("City / Country (Optional)")
    rating = st.slider("Rate today's episode topic:", 1, 5, 5)

    poll_answer = st.radio(
        "Weekly Poll: Did you enjoy this week's episode?",
        [
            "Yes, definitely!",
            "Not really",
            "I have mixed feelings",
            "I didn't listen yet",
        ],
    )

    feedback_text = st.text_area(
        "Your Question or Thought for Next Week's Episode:"
    )

    submitted = st.form_submit_button("🚀 Submit to Podcast Host")

# --- 4. PROCESSING SUBMISSION ---
if submitted:
    if not listener_name or not feedback_text:
        st.warning("Please provide your name and a comment before submitting.")
    else:
        try:
            worksheet = sh.get_worksheet(0)  # Tab 1: Listener Submissions

            worksheet.append_row(
                [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    listener_name.strip(),
                    listener_location.strip(),
                    rating,
                    poll_answer,
                    feedback_text.strip(),
                ]
            )

            st.success(
                f"Thank you {listener_name}! Your submission has been logged for the host."
            )
            st.balloons()

        except Exception as e:
            st.error("Error saving to Google Sheets:")
            st.exception(e)