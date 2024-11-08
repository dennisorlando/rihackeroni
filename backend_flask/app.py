from flask import Flask

app = Flask("Soooooo Wonderful TODO: rename")


@app.route("/")
def hello_world():
    print("Yayyyyyyyy a request!!!!!!!!!!!!!!!")
    return "oooops html malformato </p>"
