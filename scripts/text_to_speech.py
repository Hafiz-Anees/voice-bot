import os

from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    SpeakOptions
)

# =====================================
# LOAD ENV
# =====================================
load_dotenv()

# =====================================
# API KEY
# =====================================
DEEPGRAM_API_KEY = os.getenv(
    "DEEPGRAM_API_KEY"
)

# =====================================
# CLIENT
# =====================================
deepgram = DeepgramClient(
    DEEPGRAM_API_KEY
)

# =====================================
# TEXT TO SPEECH
# =====================================
def text_to_speech(text):

    options = SpeakOptions(

        model="aura-asteria-en"
    )

    response = deepgram.speak.v("1").stream(

        {"text": text},

        options
    )

    audio_bytes = response.stream_memory

    return audio_bytes