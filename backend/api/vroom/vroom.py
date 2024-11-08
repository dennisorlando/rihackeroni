from classes import Vehicle, Request, VroomOutput
import requests as r


class Calculation:
    def __init__(self, vehicles: list[Vehicle], requests: list[Request], options: dict):
        self.vehicles = vehicles
        self.requests = requests
        self.options = options

    def create_request(self):
        data = {}
        data["vehicles"] = [vehicle.to_vroom_dict() for vehicle in self.vehicles]
        data["shipments"] = [request.to_shipment() for request in self.requests]
        return data

    def calculate(self):
        print("Calculating route...")
        request = self.create_request()

        response = r.get("http://vroom:5002", json=request)
        return VroomOutput.from_dict(response.json())
