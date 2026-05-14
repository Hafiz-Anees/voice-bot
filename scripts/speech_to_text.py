import os
from dotenv import load_dotenv
from core.config import settings
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource
)
# import google.generativeai as genai


# genai.configure(
#     api_key=settings.GEMINI_API_KEY
# )

# gemini_model = genai.GenerativeModel(
#     "gemini-2.5-flash"
# )

# =====================================
# API KEY
# =====================================
DEEPGRAM_API_KEY = settings.DEEPGRAM_API_KEY

# =====================================
# CLIENT
# =====================================
deepgram = DeepgramClient(
    DEEPGRAM_API_KEY
)

# translate urdu to english

# =====================================
# URDU TO ENGLISH TRANSLATION
# =====================================

# def translate_urdu_to_english(urdu_text):

#     prompt = f"""
#     Translate the following Urdu text into natural fluent English.

#     Urdu Text:
#     {urdu_text}
#     """

#     response = gemini_model.generate_content(
#         prompt
#     )

#     return response.text.strip()

# =====================================
# TRANSCRIBE FUNCTION
# =====================================
def transcribe_audio(audio_bytes):

    payload: FileSource = {

        "buffer": audio_bytes
    }

    options = PrerecordedOptions(

        model="nova-2",

        smart_format=True
    )

    response = deepgram.listen.rest.v("1").transcribe_file(

        payload,

        options
    )

    transcript = (

        response.results
        .channels[0]
        .alternatives[0]
        .transcript
    )
    
    return transcript

# =====================================
# TRANSCRIBE URDU FUNCTION

# def transcribe_urdu(audio_bytes):

#     payload: FileSource = {
#         "buffer": audio_bytes
#     }

#     options = PrerecordedOptions(

#         model="nova-3",

#         language="ur",

#         smart_format=True
#     )

#     response = deepgram.listen.rest.v("1").transcribe_file(

#         payload,

#         options
#     )

#     transcript = (

#         response.results
#         .channels[0]
#         .alternatives[0]
#         .transcript
#     )

#     return translate_urdu_to_english(transcript)