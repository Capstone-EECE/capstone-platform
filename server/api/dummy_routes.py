import math
import random
import threading
import time
from threading import Thread

import requests
from flask import Blueprint, jsonify, request
from flask_socketio import Namespace, SocketIO, emit
from server.api.socket_events import socketio

dummy_endpoints = Blueprint("dummy_endpoints", __name__)


# MOCK DB
database = [
    {"username": "diegovaldivia", "password": "testpassword"},
    {"username": "stepan", "password": "poopoopeepee123"},
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


# ----------------------------------------------------------


point_events_per_stop = [5, 7, 3, 10, 6]
current_location = (42.319121, -71.120366)
i = 0
emit_points = False


def simulateDrone():
    global i

    # Define the four lat lng values
    locations = [
        (42.319121, -71.120366),
        (42.318979, -71.121108),
        (42.318342, -71.120869),
        (42.318525, -71.119824),
        (42.319121, -71.120366),
    ]

    increment = 0.00001
    current_location = locations[0]  # Start from the first location

    for target_location in locations:
        i += 1

        while True:
            # Calculate the distance between current_location and target_location
            distance = math.dist(current_location, target_location)

            if (
                distance < 1e-4
            ):  # You can adjust this threshold based on your precision requirements
                break

            # Increment or decrement the lat and/or lng based on the target_location
            lat_diff = target_location[0] - current_location[0]
            lng_diff = target_location[1] - current_location[1]

            if lat_diff != 0:
                current_location = (
                    current_location[0] + increment
                    if lat_diff > 0
                    else current_location[0] - increment,
                    current_location[1],
                )
            if lng_diff != 0:
                current_location = (
                    current_location[0],
                    current_location[1] + increment
                    if lng_diff > 0
                    else current_location[1] - increment,
                )

            # Print or use the current_location as needed
            socketio.emit(
                "coordinate", {"lat": current_location[0], "lng": current_location[1]}
            )
            # print(f"Current Location: {current_location}")
            time.sleep(0.1)

        for _ in range(60):  # Assuming each iteration represents 0.1 seconds
            time.sleep(0.1)
            # Introduce small random variations to simulate slight movements
            current_location = (
                current_location[0] + random.uniform(-0.00001, 0.00001),
                current_location[1] + random.uniform(-0.00001, 0.00001),
            )
            socketio.emit(
                "coordinate", {"lat": current_location[0], "lng": current_location[1]}
            )

            if emit_points:
                for _ in range(point_events_per_stop[i]):
                    socketio.emit(
                        "point",
                        {
                            "lat": current_location[0],
                            "lng": current_location[1],
                            "value": point_events_per_stop[i],
                        },
                    )


@dummy_endpoints.route("/gps/start", methods=["GET"])
def frontend_start_coordinate_ingestion():
    global location_thread_instance, i
    location_thread_instance = Thread(target=simulateDrone)
    location_thread_instance.start()

    return ("movement successful", 200)


@dummy_endpoints.route("/points/start", methods=["GET"])
def frontend_start_points_ingestion():
    global emit_points
    emit_points = True
    return ("point movement started", 200)


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
