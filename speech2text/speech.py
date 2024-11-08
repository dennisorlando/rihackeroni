import google.generativeai as genai
import os
from dotenv import load_dotenv
import whisper
from flask import Flask, request, jsonify
from gtts import gTTS
from io import BytesIO

model = whisper.load_model("turbo")
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key="GEMINI_API_KEY")
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


app = Flask(__name__)


@app.route("/transcribe", methods=["POST"])
def transcribe_route():
    audio = request.files["audio"]
    result = transcribe(audio)
    return jsonify({"transcription": result})


# define a json, if the transcription doesnt contain one or more
# of the key in the json, return an audio for the missing key(s)
# use tts and a LLM to check if some of the key are missing
# if the transcription is correct, return a json with the transcription
@app.route("/validate", methods=["POST"])
def validate_route():
    audio = request.files["audio"]
    result = transcribe(audio)
    return jsonify({"transcription": result})


def missing_keys(transcription):
    expected_json = {
        "name": "",
        "surname": "",
        "fiscal_code": "",
        "address": "",
        "city": "",
        "zip": "",
        "appointment_time": "",
        "date": "",
        "destination": "",
        }
    prompt = f"""
        You are a helper that checks whether a transcription includes all the following details:
        {expected_json}
    
        The transcription is: "{transcription}"
    
        Please check if all the possible values of the keys ('name', 'age', 'city') are mentioned in the transcription.
        If any keys are missing, list them, with this syntax: if 'name' and 'city' are missing, write 'name, city'.
        If only one key is missing, write the name of the key.
    """
    gemini_response = gemini_model.generate_content(prompt) 
    print(gemini_response.text)
    return gemini_response.text.split(", ")


def transcribe(audio):
    return model.transcribe(audio)


# Function to generate audio for the missing keys
def generate_audio_for_missing_keys(missing_keys):
    if not missing_keys:
        return None  # No missing keys, no audio
    missing_message = "The following keys are missing: " + ", ".join(missing_keys)
    tts = gTTS(text=missing_message, lang='de')
    audio_io = BytesIO()
    tts.save(audio_io)
    audio_io.seek(0)
    
    return audio_io
