from json import loads, dumps, dump, load
from datetime import datetime, time, timedelta
from sys import argv, stderr
from flask import Flask, request, jsonify
from subprocess import check_output

VEHICLES = {
    1: {"start": "trento", "end": "trento", "capacity": 4},
    2: {"start": "rovereto", "end": "trento", "capacity": 3}
}

app = Flask("sesso")

def timewin(t):
    return [
        (datetime.combine(datetime.min, t) - datetime.min - timedelta(minutes=30)) // timedelta(seconds=1),
        (datetime.combine(datetime.min, t) - datetime.min - timedelta(minutes=10)) // timedelta(seconds=1),
    ]

def process_map():
    with open("/home/topongo/downloads/untitled_map(2).geojson") as f:
        data = load(f)["features"]

    dsts = {}
    clients = {}
    for f in data:
        if "properties" not in f:
            continue
        props = f["properties"]
        if "description" not in props:
            dsts[props["name"]] = {"coords": f["geometry"]["coordinates"]}
        else:
            client = {}
            for l in props["description"].split("\n"):
                if "=" not in l:
                    continue
                k, v = l.split("=")
                if k not in ("t", "d", "c"):
                    continue
                if k == "t":
                    t = v.split(":")
                    client["time"] = time(int(t[0]), int(t[1]))
                elif k == "c":
                    client["count"] = int(v)
                elif k == "d":
                    client["dst"] = v
            client["src"] = f["geometry"]["coordinates"]
            client["name"] = props["name"]

            clients[props["name"]] = client

    # check if dst is in dsts
    for c in clients.values():
        if c["dst"] not in dsts:
            print("Destination {} not found".format(c["dst"]))
            exit(1)

    for i, c in enumerate(clients.values()):
        print("Client {} {}: {} -> {} ({} items)".format(c["name"], i, c["src"], c["dst"], c["count"]), file=stderr)

    output = {
        "vehicles": [
            {"id": k, "start": dsts[v["start"]]["coords"], "end": dsts[v["end"]]["coords"], "capacity": [v["capacity"]]}
            for k, v in VEHICLES.items()
        ],
        "shipments": [
            {"amount": [c["count"]], "delivery": {"id": k, "location": dsts[c["dst"]]["coords"], "time_windows": [timewin(c["time"])]}, "pickup": {"id": k, "location": c["src"]}}
            for k, c in enumerate(clients.values())
        ]
    }
    return output

@app.get("/")
def root():
    with open("output.json", "w") as f:
        dump(process_map(), f)

    return jsonify(loads(check_output(["./vroom.sh", "-i", "output.json", "-g", "--host", "10.69.0.2", "--port", "car:5001"])))

if __name__ == "__main__":
    app.run(host="10.69.0.2")
