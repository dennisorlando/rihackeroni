from flask import Blueprint
import google.generativeai as genai
import os

gemini_bp = Blueprint('gemini', __name__)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

@gemini_bp.route('/gemini/<prompt>')
def gemini(prompt):
    response = model.generate_content(f"{prompt}")
    return f"helloooo {response.text}"
