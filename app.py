from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="The Chilled Sister's Podcast", page_icon="🎙️", layout="centered"
)

st.title("🎙️ The Chilled Sister's Podcast")
st.caption(
    "New episodes every Friday! Listen, share your thoughts, and get featured on air."
)

st.divider()

# --- 2. LATEST EPISODE SECTION ---
st.header("🎧 This Week's Episode")
st.subheader("Episode 117: when did you realize you can never marry him?")

# Direct MP3 Audio Streaming
st.audio(
    "https://content.rss.com/episodes/223625/3164519/thechilledsisters/2026_09_18_13_53_06_6f734125-3f0e-499a-b54f-5af1b94dedb6.mp3"
)

with st.expander("📝 View AI Key Takeaways & Timestamps"):
    st.markdown(
        """
    - **02:15** — Introduction to online brand positioning
    - **14:30** — How to use interactive tools to double WhatsApp conversions
    - **28:10** — Q&A with listener submissions from last week
    """
    )

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

# --- 4. PROCESSING SUBMISSION & GOOGLE SHEETS LOGGING ---

if submitted:
    if not listener_name or not feedback_text:
        st.warning("Please provide your name and a comment before submitting.")
    else:
        try:
            # Explicitly pass the spreadsheet URL directly in st.connection
            conn = st.connection(
                "gsheets",
                type=GSheetsConnection,
                spreadsheet="PASTE_YOUR_GOOGLE_SHEET_URL_HERE",
            )

            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Name": listener_name.strip(),
                        "Location": listener_location.strip(),
                        "Rating": rating,
                        "Poll_Answer": poll_answer,
                        "Feedback_Question": feedback_text.strip(),
                    }
                ]
            )

            # Read existing sheet data explicitly from your tab
            existing_data = conn.read(
                worksheet="TheChilledSistersPodcasts", ttl=0
            )

            # Append new row
            updated_data = pd.concat(
                [existing_data, new_data], ignore_index=True
            )

            # Write back to your specific tab
            conn.update(
                worksheet="TheChilledSistersPodcasts", data=updated_data
            )

            st.success(
                f"Thank you {listener_name}! Your submission has been logged for the host."
            )
            st.balloons()

        except Exception as e:
            st.error(f"Error saving to Google Sheets: {e}")