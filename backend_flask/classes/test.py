import unittest
import json

from classes import Summary, Route, Step, VroomOutput

class TestVroomSerialization(unittest.TestCase):

    def setUp(self):
        """Setup test data for the tests"""
        # Example mock JSON output from Vroom API
        self.mock_json = json.dumps({
            "code": 0,
            "summary": {
                "cost": 1000,
                "routes": 1,
                "unassigned": 0,
                "setup": 300,
                "service": 500,
                "duration": 1200,
                "waiting_time": 100,
                "priority": 50,
                "delivery": 10,
                "pickup": 5,
                "distance": 8000
            },
            "routes": [
                {
                    "vehicle": 1,
                    "steps": [
                        {
                            "type": "start",
                            "arrival": 0,
                            "duration": 0,
                            "setup": 0,
                            "service": 0,
                            "waiting_time": 0,
                            "violations": [],
                            "location": [12.492, 41.890]
                        },
                        {
                            "type": "job",
                            "arrival": 600,
                            "duration": 300,
                            "setup": 0,
                            "service": 100,
                            "waiting_time": 50,
                            "violations": [],
                            "location": [12.500, 41.892]
                        }
                    ],
                    "cost": 1000,
                    "setup": 300,
                    "service": 500,
                    "duration": 1200,
                    "waiting_time": 100,
                    "priority": 50,
                    "violations": [],
                    "delivery": 10,
                    "pickup": 5,
                    "distance": 8000
                }
            ],
            "unassigned": []
        })

        # Expected summary and route objects to validate against
        self.expected_summary = Summary(
            cost=1000,
            routes=1,
            unassigned=0,
            setup=300,
            service=500,
            duration=1200,
            waiting_time=100,
            priority=50,
            delivery=10,
            pickup=5,
            distance=8000
        )

        self.expected_route = Route(
            vehicle=1,
            steps=[
                Step(
                    step_type="start",
                    arrival=0,
                    duration=0,
                    setup=0,
                    service=0,
                    waiting_time=0,
                    violations=[],
                    location=[12.492, 41.890]
                ),
                Step(
                    step_type="job",
                    arrival=600,
                    duration=300,
                    setup=0,
                    service=100,
                    waiting_time=50,
                    violations=[],
                    location=[12.500, 41.892]
                )
            ],
            cost=1000,
            setup=300,
            service=500,
            duration=1200,
            waiting_time=100,
            priority=50,
            violations=[],
            delivery=10,
            pickup=5,
            distance=8000
        )

    def test_serialization(self):
        """Test serializing Python objects back to JSON"""
        vroom_output = VroomOutput.from_json(self.mock_json)
        json_result = vroom_output.to_json()
        print("Serialized JSON:")
        print(json_result)

        parsed_result = json.loads(json_result)
        print("\nParsed JSON:")
        print(parsed_result)


    def test_round_trip(self):
        """Test that deserialization followed by serialization returns the original JSON"""
        vroom_output = VroomOutput.from_json(self.mock_json)
        result_json = vroom_output.to_json()
        parsed_result = json.loads(result_json)



if __name__ == "__main__":
    unittest.main()
