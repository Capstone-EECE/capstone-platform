import random
import time

import requests
from flask import Blueprint
from flask_socketio import emit
from server.api.socket_events import socketio

dummy_endpoints = Blueprint("dummy_endpoints", __name__)


@dummy_endpoints.route("/connect", methods=["GET"])
def frontend_connect_to_device():
    return ("connected", 200)


@dummy_endpoints.route("/gps/start", methods=["GET"])
def frontend_start_coordinate_ingestion():
    initial_location = {"lat": 42.3325046, "lng": -71.1031778}
    counter = 0

    while counter < 20:
        random_lat_offset = random.uniform(0, 0.001)
        random_lng_offset = random.uniform(0, 0.001)

        initial_location["lat"] += random_lat_offset
        initial_location["lng"] += random_lng_offset

        print("New Location:", initial_location)
        socketio.emit("coordinate", initial_location)
        for i in range(counter * 2):
            socketio.emit("point", initial_location)

        counter += 1
        time.sleep(1)


@dummy_endpoints.route("/points/start", methods=["GET"])
def frontend_start_points_ingestion():
    socketio.emit("points", {"lat": 40.3391998, "lng": -70.0})
