import google.generativeai as genai
import os
from dotenv import load_dotenv
import whisper
from flask import Flask, request, jsonify
from gtts import gTTS
from io import BytesIO
from flask_cors import CORS
import subprocess

model = whisper.load_model("turbo")
load_dotenv()


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key="GEMINI_API_KEY")
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# show the index page in index.html
@app.route("/")
def index():
    return app.send_static_file("index.html")


# define a json, if the transcription doesnt contain one or more
# of the key in the json, return an audio for the missing key(s)
# use tts and a LLM to check if some of the key are missing
# if the transcription is correct, return a json with the transcription
@app.route("/transcribe", methods=["POST"])
def validate_route():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    audio = request.files["audio"]
    audio.save(os.path.join("uploads", audio.filename))
#    result = transcribe(audio)
#    return jsonify({"transcription": result})
    convert_to_mp3(os.path.join("uploads", audio.filename), os.path.join("uploads", "converted.mp3"))
    result = transcribe(os.path.join("uploads", "converted.mp3"))
#    return jsonify({"message": "Transcription successful"}), 200
    missing_keys, full_json = missing_keys_function(result)
    if missing_keys:
        # Genera l'audio e crea il JSON per il caso con chiavi mancanti
        audio_base64 = generate_audio_for_missing_keys(missing_keys)
        response = {
            "status": "incomplete",
            "missing_keys": missing_keys,
            "audio": audio_base64  # Includi l'audio in formato base64 nel JSON
        }
    else:
        # Nessuna chiave mancante, restituisce il JSON completo
        response = {
            "status": "complete",
            "data": full_json
        }

    return jsonify(response), 200


def convert_to_mp3(input_file, output_file):
    try:
        # Run the ffmpeg command
        subprocess.run([
            'ffmpeg', '-i', input_file,
            '-vn',  # No video
            '-ar', '44100',  # Audio sample rate
            '-ac', '2',  # Audio channels
            '-b:a', '192k',  # Audio bitrate
            output_file
        ], check=True)
        print(f"Conversion successful: {output_file}")
    except subprocess.CalledProcessError as e:
        print("An error occurred during conversion:", e)


def missing_keys_function(transcription):
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
        If no keys are missing, write return the json with all the values.
    """
    safe = [
      {
          "category": "HARM_CATEGORY_HARASSMENT",
          "threshold": "BLOCK_NONE",
      },
      {
          "category": "HARM_CATEGORY_HATE_SPEECH",
          "threshold": "BLOCK_NONE",
      },
      {
          "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
          "threshold": "BLOCK_NONE",
      },
      {
          "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
          "threshold": "BLOCK_NONE",
      },
    ]
    gemini_response = gemini_model.generate_content(prompt, safety_settings=safe) 
    response_text = gemini_response.text.strip()

    # Check if the response is the JSON (all keys are present) or a list of missing keys
    if response_text.startswith("{") and response_text.endswith("}"):
        # All keys are present, return the JSON as a dictionary
        print("All keys are present.")
        return None, response_text  # No missing keys
    else:
        # Missing keys detected, return them as a list
        print("Missing keys detected:", response_text)
        return response_text.split(", "), None


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

