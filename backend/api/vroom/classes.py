import json
from typing import List, Optional

class Vehicle:
    def __init__(self, id, start_location, capacity_walking, capacity_wheelchair, capacity_stretcher, capacity_white_cross, max_capacity):
        self.id = id
        self.start_location = start_location
        self.capacity_walking = capacity_walking
        self.capacity_wheelchair = capacity_wheelchair
        self.capacity_stretcher = capacity_stretcher
        self.capacity_white_cross = capacity_white_cross
        self.max_capacity = max_capacity

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            start_location=data["start_location"],
            capacity_walking=data["capacity_walking"],
            capacity_wheelchair=data["capacity_wheelchair"],
            capacity_stretcher=data["capacity_stretcher"],
            capacity_white_cross=data["capacity_white_cross"],
            max_capacity=data["max_capacity"]
        )

    def to_vroom_dict(self):
        return {
            "id": self.id,
            "start": self.start_location,
            "end": self.start_location,
            # "capacity": [self.capacity_walking, self.capacity_wheelchair, self.capacity_stretcher, self.capacity_white_cross]
            "capacity": [1]
        }


class Request:
    def __init__(self, id, accompanied, pickup_location, destination, appointment_time):
        self.id = id
        self.accompanied = accompanied
        self.pickup_location = pickup_location
        self.destination = destination
        self.appointment_time = appointment_time

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            accompanied=data["accompanied"],
            pickup_location=data["pickup_location"],
            destination=data["destination"],
            appointment_time=data["appointment_time"]
        )

# ======================================================================================================================
# Classes for Vroom output

class Violation:
    def __init__(self, cause: str, duration: Optional[int] = None):
        self.cause = cause
        self.duration = duration

    @classmethod
    def from_dict(cls, data: dict):
        return cls(cause=data["cause"], duration=data.get("duration"))

    def to_dict(self):
        return {"cause": self.cause, "duration": self.duration}


class Step:
    def __init__(self, step_type: str, arrival: int, duration: int, setup: int, service: int, waiting_time: int,
                 violations: Optional[List[Violation]], description: Optional[str] = None, location: Optional[List[float]] = None,
                 location_index: Optional[int] = None, task_id: Optional[int] = None, load: Optional[List[int]] = None,
                 distance: Optional[int] = None):
        self.type = step_type
        self.arrival = arrival
        self.duration = duration
        self.setup = setup
        self.service = service
        self.waiting_time = waiting_time
        self.violations = [Violation.from_dict(v) for v in violations] if violations else []
        self.description = description
        self.location = location
        self.location_index = location_index
        self.id = task_id
        self.load = load
        self.distance = distance

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            step_type=data["type"],
            arrival=data["arrival"],
            duration=data["duration"],
            setup=data["setup"],
            service=data["service"],
            waiting_time=data["waiting_time"],
            violations=data.get("violations", []),
            description=data.get("description"),
            location=data.get("location"),
            location_index=data.get("location_index"),
            task_id=data.get("id"),
            load=data.get("load"),
            distance=data.get("distance")
        )

    def to_dict(self):
        return {
            "type": self.type,
            "arrival": self.arrival,
            "duration": self.duration,
            "setup": self.setup,
            "service": self.service,
            "waiting_time": self.waiting_time,
            "violations": [v.to_dict() for v in self.violations],
            "description": self.description,
            "location": self.location,
            "location_index": self.location_index,
            "id": self.id,
            "load": self.load,
            "distance": self.distance
        }


class Route:
    def __init__(self, vehicle: int, steps: List[Step], cost: int, setup: int, service: int, duration: int,
                 waiting_time: int, priority: int, violations: Optional[List[Violation]] = None,
                 delivery: Optional[int] = None, pickup: Optional[int] = None, description: Optional[str] = None,
                 geometry: Optional[str] = None, distance: Optional[int] = None):
        if all(isinstance(s, Step) for s in steps):
            self.steps = steps
        else:
            self.steps = [Step.from_dict(s) for s in steps]

        self.vehicle = vehicle
        self.cost = cost
        self.setup = setup
        self.service = service
        self.duration = duration
        self.waiting_time = waiting_time
        self.priority = priority
        self.violations = [Violation.from_dict(v) for v in violations] if violations else []
        self.delivery = delivery
        self.pickup = pickup
        self.description = description
        self.geometry = geometry
        self.distance = distance

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            vehicle=data["vehicle"],
            steps=data["steps"],
            cost=data["cost"],
            setup=data["setup"],
            service=data["service"],
            duration=data["duration"],
            waiting_time=data["waiting_time"],
            priority=data["priority"],
            violations=data.get("violations", []),
            delivery=data.get("delivery"),
            pickup=data.get("pickup"),
            description=data.get("description"),
            geometry=data.get("geometry"),
            distance=data.get("distance")
        )

    def to_dict(self):
        return {
            "vehicle": self.vehicle,
            "steps": [s.to_dict() for s in self.steps],
            "cost": self.cost,
            "setup": self.setup,
            "service": self.service,
            "duration": self.duration,
            "waiting_time": self.waiting_time,
            "priority": self.priority,
            "violations": [v.to_dict() for v in self.violations],
            "delivery": self.delivery,
            "pickup": self.pickup,
            "description": self.description,
            "geometry": self.geometry,
            "distance": self.distance
        }


class Summary:
    def __init__(self, cost: int, routes: int, unassigned: int, setup: int, service: int, duration: int,
                 waiting_time: int, priority: int, delivery: Optional[int] = None, pickup: Optional[int] = None,
                 distance: Optional[int] = None):
        self.cost = cost
        self.routes = routes
        self.unassigned = unassigned
        self.setup = setup
        self.service = service
        self.duration = duration
        self.waiting_time = waiting_time
        self.priority = priority
        self.delivery = delivery
        self.pickup = pickup
        self.distance = distance

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            cost=data["cost"],
            routes=data["routes"],
            unassigned=data["unassigned"],
            setup=data["setup"],
            service=data["service"],
            duration=data["duration"],
            waiting_time=data["waiting_time"],
            priority=data["priority"],
            delivery=data.get("delivery"),
            pickup=data.get("pickup"),
            distance=data.get("distance")
        )

    def to_dict(self):
        return {
            "cost": self.cost,
            "routes": self.routes,
            "unassigned": self.unassigned,
            "setup": self.setup,
            "service": self.service,
            "duration": self.duration,
            "waiting_time": self.waiting_time,
            "priority": self.priority,
            "delivery": self.delivery,
            "pickup": self.pickup,
            "distance": self.distance
        }


class VroomOutput:
    def __init__(self, code: int, summary: Summary, routes: List[Route], unassigned: Optional[List[dict]] = None):
        self.code = code
        self.summary = summary
        self.routes = [Route.from_dict(r) for r in routes]
        self.unassigned = unassigned if unassigned else []

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            code=data["code"],
            summary=Summary.from_dict(data["summary"]),
            routes=data["routes"],
            unassigned=data.get("unassigned", [])
        )

    def to_dict(self):
        return {
            "code": self.code,
            "summary": self.summary.to_dict(),
            "routes": [r.to_dict() for r in self.routes],
            "unassigned": self.unassigned
        }

    @staticmethod
    def from_json(json_str: str):
        data = json.loads(json_str)
        return VroomOutput.from_dict(data)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)



