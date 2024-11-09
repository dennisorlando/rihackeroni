import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from gtts import gTTS
from io import BytesIO
from flask_cors import CORS
import subprocess
import base64

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
        "status": "complete" if not missing_keys else "incomplete",
        "missing_keys": missing_keys,
        "data": full_json,
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
    prompt = f"""
        You are a helper that checks whether a transcription includes all the following details:
        {list(expected_json.keys())}
        The transcription is: "{transcription}"
    
        Please check if all the possible values of the keys ('name', 'age', 'city') are mentioned in the transcription.
        If any keys are missing, list them, with this syntax: if 'name' and 'city' are missing, write 'name, city'.
        If only one key is missing, write the name of the key.
        If no keys are missing, write return the json with all the values.
        Remember to translate the keys given by the transcription from German to English if the transcription is in German.
        Remember to translate the keys given by the transcription from Italian to English if the transcription is in Italian.
        Example if a transcription says Meine Name ist John, the key 'name' is equivalent to 'Name' in German.
        If the transcription is in Italian, and it says Il mio nome è John, the key 'name' is equivalent to John.
        If the transcription is in German, and it says Ich wohne in Berlin, the key 'city' is equivalent to 'Berlin'.
        For each missing key, list them exactly like this: 'name, city' if both are missing.
        If all keys are present, just return 'all present'.
        Return this structure
        {
                full_json: {
                    \"name\": If given in the transcription,},
                    \"surname\": If given in the transcription,
                    \"fiscal_code\": If given in the transcription,
                    \"address\": If given in the transcription,
                    \"city\": If given in the transcription,
                    \"zip\": If given in the transcription,
                    \"appointment_time\": If given in the transcription,
                    \"date\": If given in the transcription,
                    \"destination\": If given in the transcription,
                    },
                missing_keys: If any keys are missing, list

                }
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

    missing_keys = []
    if response_text == "all present":
        full_json = expected_json.copy()  # Populate with the transcription values
    else:
        missing_keys = response_text.split(", ")
        full_json = expected_json.copy()
        for key in full_json.keys():
            print(response_text)           

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
