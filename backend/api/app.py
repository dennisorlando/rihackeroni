from flask import Flask, request, jsonify
from backend.api.vroom.options import Options
from vroom.classes import Vehicle, Request

app = Flask(__name__)
options = Options([30, 10])

vehicle_list = []
request_list = []


@app.route('/')
def index():
    return 'index'


@app.get('/routes')
def calc_route():
    global vehicle_list
    global request_list
    if request.is_json:
        data = request.get_json()
        if "vehicle_list" in data:
            vehicle_list = [Vehicle.from_dict(v) for v in data["vehicle_list"]]
        if "patient_list" in data:
            request_list = [Request.from_dict(p) for p in data["patient_list"]]

        # TODO insert vroom function here
        # TODO return the result of the vroom function

        return jsonify({"message": "Received and saved data!"}), 200
    else:
        return jsonify({"error": "Error: the request doesn't contain json"}), 404
