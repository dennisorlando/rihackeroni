import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from gtts import gTTS
from io import BytesIO
from flask_cors import CORS
import subprocess
import base64
import json

load_dotenv()


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# show the index page in index.html
@app.route("/")
def index():
    return render_template("index.html")


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
    convert_to_mp3(os.path.join("uploads", audio.filename), os.path.join("uploads", "converted.mp3"))
    result = transcribe(os.path.join("uploads", "converted.mp3"))
    print(type(os.path.join("uploads", "converted.mp3")))
    print("Questa è la trascrizione"+str(result))
    missing_keys, full_json = missing_keys_function(result)
    print(full_json)

    response = {
        "status": "incomplete" if missing_keys else "complete",
        "missing_keys": missing_keys,
        "data": full_json
    }

    return jsonify(response), 200


def convert_to_mp3(input_file, output_file):
    try:
        # Run the ffmpeg command
        subprocess.run([
            'ffmpeg', '-i', input_file,
            '-y',
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
    
        # Prompt per ottenere un JSON con tutte le chiavi e i valori disponibili
    prompt = f"""
        Trasforma questa trascrizione in un JSON con le seguenti chiavi:
        'name', 'surname', 'fiscal_code', 'address', 'city', 'zip', 'appointment_time', 'date', 'destination'.
        
        Se una chiave è presente nella trascrizione, inserisci il suo valore nel JSON; 
        se manca, lascia il valore vuoto o come stringa vuota.
        
        Trascrizione: "{transcription}"
        
        Restituisci il JSON completo.
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

#    if response_text.startswith("{") and response_text.endswith("}"):
#        print("All keys are present.")
#        return None, response_text  # No missing keys
#    else:
#        print("Missing keys detected:", response_text)
#       return response_text.split(", "), None

      
    # Trasformiamo il testo JSON di Gemini in un dizionario Python
    try:
            full_json = json.loads(response_text)
    except:
            full_json = {}
    # Controlla per valori vuoti e crea una lista di chiavi mancanti
    missing_keys = [key for key, value in full_json.items() if not value]

    return missing_keys, full_json


def transcribe(audio):

    myfile = genai.upload_file(f'{audio}')
    global gemini_model
    gemini_model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    prompt = "Generate a transcript of the speech."

    response = gemini_model.generate_content([prompt, myfile])
    return response


def generate_audio_for_missing_keys(missing_keys):
    if not missing_keys:
        return None  # No missing keys, no audio
    missing_message = "The following keys are missing: " + ", ".join(missing_keys)
    tts = gTTS(text=missing_message, lang='de')
    audio_io = BytesIO()
    tts.save(audio_io)
    audio_io.seek(0)
    audio_base64 = base64.b64encode(audio_io.read()).decode('utf-8')
    return audio_base64
