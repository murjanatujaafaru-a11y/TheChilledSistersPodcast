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

# --- 2. LATEST EPISODE SECTION ---
st.header("🎧 This Week's Episode")
st.subheader("Episode 117: when did you realize you can never marry him?")

# Direct MP3 Audio Streaming
st.audio(
    "https://content.rss.com/episodes/223625/3164519/thechilledsisters/2026_09_18_13_53_06_6f734125-3f0e-499a-b54f-5af1b94dedb6.mp3"
)

with st.expander("📝 View this week's Takeaways & Timestamps"):
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
            # 1. Fetch credentials block from st.secrets
            secrets_data = st.secrets["connections"]["gsheets"]
            
            # 2. Extract spreadsheet URL
            spreadsheet_url = secrets_data["spreadsheet"]
            
            # 3. Create a clean dictionary for gspread auth (excluding 'spreadsheet')
            creds_dict = {k: v for k, v in secrets_data.items() if k != "spreadsheet"}
            
            # 4. Authenticate and append row
            gc = gspread.service_account_from_dict(creds_dict)
            sh = gc.open_by_url(spreadsheet_url)
            worksheet = sh.get_worksheet(0)

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
            st.error(f"Error saving to Google Sheets: {e}")
            st.success(
                f"Thank you {listener_name}! Your submission has been logged for the host."
            )
            st.balloons()

        except Exception as e:
            st.error(f"Error saving to Google Sheets: {e}")