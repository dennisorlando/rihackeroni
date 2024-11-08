from flask import Flask, request, jsonify

app = Flask(__name__)

vehicle_list = {}
patient_list = {}


@app.route('/')
def index():
    return 'index'


@app.get('/routes')
def calc_route():
    global vehicle_list
    if request.is_json:
        data = request.get_json()
        if "vehicle_list" in data:
            vehicle_list.update(data["vehicle_list"])
        if "patient_list" in data:
            patient_list.update(data["patient_list"])
        return jsonify({"message": "Received and saved data!"}), 200
    else:
        return jsonify({"error": "Error: the request doesn't contain json"}), 404
