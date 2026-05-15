import streamlit as st
import requests
import uuid

from audio_recorder_streamlit import audio_recorder

from scripts.speech_to_text import transcribe_audio
from scripts.text_to_speech import text_to_speech


# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Hotel AI Voice Assistant",
    page_icon="🏨",
    layout="centered"
)

# =========================================
# LOAD BACKEND API URL FROM STREAMLIT SECRETS
# =========================================
API_URL = st.secrets["API_URL"]

# =========================================
# TITLE
# =========================================
st.title("🏨 Hotel AI Voice Assistant")

st.write(
    "Voice Enabled Hotel Booking Assistant"
)

# =========================================
# CREATE FRONTEND SESSION
# =========================================
if "user_id" not in st.session_state:

    st.session_state.user_id = str(
        uuid.uuid4()
    )

# =========================================
# CURRENT USER ID
# =========================================
user_id = st.session_state.user_id

# =========================================
# SIDEBAR
# =========================================
st.sidebar.title("Session")

st.sidebar.write(
    "Frontend Managed Session"
)

st.sidebar.code(user_id)

# =========================================
# TEMP DEBUG (REMOVE LATER)
# =========================================
st.sidebar.write("Backend API")
st.sidebar.code(API_URL)

# =========================================
# NEW SESSION BUTTON
# =========================================
if st.sidebar.button("Start New Session"):

    st.session_state.user_id = str(
        uuid.uuid4()
    )

    st.rerun()

# =========================================
# VOICE INPUT
# =========================================
st.subheader(
    "🎤 Speak Your Booking Request"
)

audio_bytes = audio_recorder(
    text="Click to Record",
    recording_color="#e74c3c",
    neutral_color="#6c757d",
    icon_name="microphone",
    icon_size="2x",
    key="audio_recorder"
)

# =========================================
# PROCESS AUDIO
# =========================================
if audio_bytes:

    try:

        # =================================
        # SPEECH TO TEXT
        # =================================
        with st.spinner("Transcribing..."):

            query = transcribe_audio(
                audio_bytes
            )

        # =================================
        # EMPTY QUERY CHECK
        # =================================
        if not query or not query.strip():

            st.warning(
                "Could not detect speech."
            )

            st.stop()

        # =================================
        # SHOW USER SPEECH
        # =================================
        st.subheader("🗣 You Said")

        st.write(query)

        # =================================
        # SEND TO BACKEND API
        # =================================
        with st.spinner(
            "Generating response..."
        ):

            headers = {
                "Content-Type": "application/json"
            }

            payload = {

                "user_id": user_id,

                "query": query
            }

            response = requests.post(

                API_URL,

                json=payload,

                headers=headers,

                stream=True,

                timeout=300
            )

        # =================================
        # CHECK API STATUS
        # =================================
        if response.status_code != 200:

            st.error(
                f"API Error: {response.status_code}"
            )

            try:

                st.write(
                    response.json()
                )

            except:

                st.write(
                    response.text
                )

            st.stop()

        # =================================
        # RESPONSE UI
        # =================================
        st.subheader("🤖 Assistant")

        response_placeholder = st.empty()

        full_response = ""

        # =================================
        # STREAM RESPONSE
        # =================================
        for chunk in response.iter_content(

            chunk_size=512,

            decode_unicode=True
        ):

            if chunk:

                full_response += chunk

                response_placeholder.markdown(
                    full_response
                )

        # =================================
        # EMPTY RESPONSE CHECK
        # =================================
        if not full_response.strip():

            st.warning(
                "No response generated."
            )

            st.stop()

        # =================================
        # TEXT TO SPEECH
        # =================================
        with st.spinner(
            "Generating voice response..."
        ):

            audio_output = text_to_speech(
                full_response
            )

        # =================================
        # PLAY AUDIO
        # =================================
        st.audio(
            audio_output,
            format="audio/mp3"
        )

    # =====================================
    # CONNECTION ERROR
    # =====================================
    except requests.exceptions.ConnectionError as e:

        st.error(
            f"Could not connect to backend API: {str(e)}"
        )

    # =====================================
    # TIMEOUT ERROR
    # =====================================
    except requests.exceptions.Timeout:

        st.error(
            "Request timeout."
        )

    # =====================================
    # GENERAL ERROR
    # =====================================
    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )