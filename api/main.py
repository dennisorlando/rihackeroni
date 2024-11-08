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

class Vehicle:
    def __init__(self, id, start_location, capacity_walking, capacity_wheelchair, capacity_stretcher, capacity_white_cross, max_capacity):
        self.id = id
        self.start_location = start_location
        self.capacity_walking = capacity_walking
        self.capacity_wheelchair = capacity_wheelchair
        self.capacity_stretcher = capacity_stretcher
        self.capacity_white_cross = capacity_white_cross
        self.max_capacity = max_capacity

    
    
class Request:
    def __init__(self, id, accompanied, pickup_location, destionation, appointment_time):
        self.id = id
        self.accompanied = accompanied
        self.pickup_location = pickup_location
        self.destionation = destionation
        self.appointment_time = appointment_time
