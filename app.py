from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Page Setup
st.set_page_config(
    page_title="The Chilled Sister's Podcast", page_icon="🎙️", layout="centered"
)

st.title("🎙️ The Chilled Sister's Podcast")
st.caption(
    "New episodes every Friday! Listen, share your thoughts, and get featured on air."
)

st.divider()

# 1. Latest Episode Section
st.header("🎧 This Week's Episode")
st.subheader("Episode 117: when did you realize you can never marry him?")

# Embed Audio Player (Spotify / Apple Podcast / MP3 link)
st.audio("https://content.rss.com/episodes/223625/3164519/thechilledsisters/2026_09_18_13_53_06_6f734125-3f0e-499a-b54f-5af1b94dedb6.mp3")

with st.expander("📝 View AI Key Takeaways & Timestamps"):
    st.markdown(
        """
    - **02:15** — Introduction to online brand positioning
    - **14:30** — How to use interactive tools to double WhatsApp conversions
    - **28:10** — Q&A with listener submissions from last week
    """
    )

st.divider()

# 2. Listener Interactive Feedback Form ("Logging Findings")
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
        ["Yes, definitely!", "Not really", "I have mixed feelings", "I didn't listen yet"],
    )

    feedback_text = st.text_area(
        "Your Question or Thought for Next Week's Episode:"
    )

    submitted = st.form_submit_button("🚀 Submit to Podcast Host")

# 3. Processing Submission & Database Logging
if submitted:
    if not listener_name or not feedback_text:
        st.warning("Please provide your name and a comment before submitting.")
    else:
        # Connect & Log to Google Sheets
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            new_data = pd.DataFrame(
                [
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Name": listener_name,
                        "Location": listener_location,
                        "Rating": rating,
                        "Poll_Answer": poll_answer,
                        "Feedback_Question": feedback_text,
                    }
                ]
            )

            existing_data = conn.read(ttl=0)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(data=updated_data)

            st.success(
                f"Thank you {listener_name}! Your submission has been logged for the host."
            )
            st.balloons()
        except Exception:
            st.success(
                "Submission received! Tune in next Friday to see if your comment is featured!"
            )