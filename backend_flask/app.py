from flask import Flask
from gemini import gemini_bp

app = Flask("Soooooo Wonderful TODO: rename")

app.register_blueprint(gemini_bp)

@app.route("/")
def hello_world():
    print("Yayyyyyyyy a request!!!!!!!!!!!!!!!")
    return "oooops html malformato </p>"
