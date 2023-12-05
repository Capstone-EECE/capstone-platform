import random
import threading
import time
from threading import Thread

from flask import Blueprint, request
from server.api.socket_events import socketio

demo_endpoints = Blueprint("deo_endpoints", __name__)
location_thread_instance = None
thread_running = False
emit_points = False

# MOCK DB
database = [
    {"username": "diegovaldivia", "password": "testpassword"},
    {"username": "stepan", "password": "poopoopeepee123"},
]


@demo_endpoints.route("/login", methods=["GET"])
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


def simulateStationaryDrone():
    global thread_running
    current_location = (42.33920931249335, -71.08742903197377)
    while thread_running:
        current_location = (
            current_location[0] + random.uniform(-0.00001, 0.00001),
            current_location[1] + random.uniform(-0.00001, 0.00001),
        )
        if emit_points:
            print("[SENSOR]: RECIEVED RADAR DATA", current_location)
            socketio.emit(
                "point", {"lat": current_location[0], "lng": current_location[1]}
            )
        print("[MODEM]: RECIEVED COORDINATE", current_location)
        socketio.emit(
            "coordinate", {"lat": current_location[0], "lng": current_location[1]}
        )
        time.sleep(2)


@demo_endpoints.route("/gps/start", methods=["GET"])
def frontend_start_coordinate_ingestion():
    global location_thread_instance, thread_running
    thread_running = True
    location_thread_instance = Thread(target=simulateStationaryDrone)
    location_thread_instance.start()

    return ("movement successful", 200)


@demo_endpoints.route("/points/start", methods=["GET"])
def frontend_start_points_ingestion():
    global emit_points
    emit_points = True
    return ("point movement started", 200)


# --------------------------------------------------------------


@demo_endpoints.route("/connect", methods=["GET"])
def frontend_connect_to_device():
    return ("connected", 200)


@demo_endpoints.route("/points/stop", methods=["GET"])
def frontend_stop_points():
    global emit_points
    emit_points = False
    return ("stop successful", 200)


@demo_endpoints.route("/gps/stop", methods=["GET"])
def frontend_stop_coordinate():
    global thread_running, location_thread_instance
    # Check if the thread is running
    if location_thread_instance and location_thread_instance.is_alive():
        thread_running = False  # Reset the flag
        location_thread_instance = None  # Reset the thread instance
        print("Thread stopped")
        return ("movement successful", 200)
    else:
        print("Thread is not running")
        return ("movement successful", 200)
