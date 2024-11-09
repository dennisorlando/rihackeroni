from configs import Configs
from .classes import Vehicle, Request, VroomOutput
from datetime import datetime, timedelta
import requests as r


def request_to_shipment(request: Request, tw: list[int]):
        time_windows = [
            request.appointment_time - tw[0],
            request.appointment_time - tw[1],
        ]

        return {
            "amount": [1],
            "delivery": {
                "id": request.id,
                "location": request.destination,
                "time_windows": [time_windows]
            },
            "pickup": {
                "id": request.id,
                "location": request.pickup_location
            }
        }

class Calculation:
    def __init__(self, vehicles: list[Vehicle], requests: list[Request], configs: Configs):
        self.vehicles = vehicles
        self.requests = requests
        self.configs = configs

    def create_request(self):
        data = {}
        data["vehicles"] = [vehicle.to_vroom_dict() for vehicle in self.vehicles]
        data["shipments"] = [request_to_shipment(request, self.configs.tw) for request in self.requests]
        return data

    def calculate(self):
        print("Calculating route...")
        request = self.create_request()

        # TODO: restore this to use internal serializer
        response = r.post("http://vroom:3000", json=request)
        return VroomOutput.from_dict(response.json())
