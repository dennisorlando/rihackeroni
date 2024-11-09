from flask import Flask, request, jsonify
from vroom.classes import Vehicle, Request
from configs import Configs
from vroom.vroom import Calculation

app = Flask(__name__)
configs = Configs([30 * 60, 10 * 60])


@app.route('/')
def index():
    return 'index'


@app.route('/routes', methods=['POST'])
def calc_route():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()

    vehicles = [Vehicle.from_dict(v) for v in data["vehicles"]]
    requests = [Request.from_dict(r) for r in data["requests"]]

    response = Calculation(vehicles, requests, configs).calculate()
    json_out = response.serialize_vroom_output()

    return json_out
