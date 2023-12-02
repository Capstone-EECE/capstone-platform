import random
import time
from threading import Thread

import requests
from flask import Blueprint, jsonify, request
from flask_socketio import Namespace, SocketIO, emit
from server.api.socket_events import socketio

dummy_endpoints = Blueprint("dummy_endpoints", __name__)


initial_location = {"lat": 42.327494, "lng": -71.115162}
loop_running = False
emit_points = False

# MOCK DB
database = [
    {"username": "diegovaldivia", "password": "testpassword"},
    {"username": "stepan", "password": "peepoopee"},
]


@dummy_endpoints.route("/login", methods=["GET"])
def login_attempt():
    time.sleep(4)

    username = request.args.get("username")
    password = request.args.get("password")

    # Find user login info in Mock DB
    user_data = next((user for user in database if user["username"] == username), None)

    if user_data:
        if user_data["password"] != password:
            return (
                {
                    "success": False,
                    "body": {"name": "pass", "message": "Invalid password"},
                },
                200,
            )
        else:
            return (
                {"success": True, "body": {"name": "-", "message": "Login Succesful"}},
                200,
            )
    else:
        return (
            {
                "success": False,
                "body": {"name": "uname", "message": "Username not found"},
            },
            200,
        )


def generate_and_emit_coordinates():
    global initial_location
    random_lat_offset = random.uniform(0, 0.0001)
    random_lng_offset = random.uniform(0, 0.0001)

    initial_location["lat"] += random_lat_offset
    initial_location["lng"] += random_lng_offset

    print("New Location:", initial_location)
    socketio.emit("coordinate", initial_location)

    return initial_location


def generate_and_emit_points():
    global initial_location
    for i in range(10):  # Emit "point" event 10 times (adjust as needed)
        socketio.emit("point", initial_location)


def continuous_loop():
    global loop_running, emit_points
    counter = 0
    while loop_running and counter < 50:
        generate_and_emit_coordinates()

        if emit_points:
            generate_and_emit_points()

        counter += 1
        time.sleep(0.5)


@dummy_endpoints.route("/gps/start", methods=["GET"])
def frontend_start_coordinate_ingestion():
    global loop_running, emit_points
    if not loop_running:
        loop_running = True
        emit_points = False  # Set the flag to emit coordinates
        Thread(target=continuous_loop).start()
    return ("movement successful", 200)


@dummy_endpoints.route("/points/start", methods=["GET"])
def frontend_start_points_ingestion():
    global loop_running, emit_points
    emit_points = True
    Thread(target=continuous_loop).start()
    return ("stop successful", 200)


# --------------------------------------------------------------


@dummy_endpoints.route("/connect", methods=["GET"])
def frontend_connect_to_device():
    return ("connected", 200)


@dummy_endpoints.route("/points/stop", methods=["GET"])
def frontend_stop_points():
    global emit_points
    emit_points = False
    return ("stop successful", 200)


@dummy_endpoints.route("/gps/stop", methods=["GET"])
def frontend_stop_coordinate():
    global loop_running
    loop_running = False
    return ("stop successful", 200)
