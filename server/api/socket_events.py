import socket

from flask import request
from flask_socketio import emit

from ..core.drone_location import get_drone_gps_coordinates
from .app import socketio

BG96_DEVICE_PORT = 1234
BG96_DEVICE_IP = "TEMP"

bg96_socket = None


def connect_to_hardware():
    if bg96_socket == None:
        # Create a socket connection to the BG96 modem
        bg96_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bg96_socket.connect(("temp", BG96_DEVICE_PORT))


@socketio.on("connect")
def handle_connect():
    print(request.sid)
    print("client connected")
    print("*************************************")
    emit("connected", f"id:{request.sid} is connected")


@socketio.on("data")
def handle_event(data):
    print("Data from the frontend", str(data))
    emit("data", {"data": data, "id": request.sid}, broadcast=True)


@socketio.on("hello")
def handle_hello(arg):
    print("__________________________________________________")
    try:
        print(arg)  # "world"
        emit("response", "got it", broadcast=True)
    except Exception as e:
        print("Error: ", str(e))
        emit("response", "Error occurred", broadcast=True)


@socketio.on("connect_drone")
def handle_custom_event():
    print("[REQUEST] turn on drone GPS coordinates")

    try:
        connect_to_hardware()

        # Send a message to the BG96 modem
        bg96_socket.send(b"TURN ON GPS COORDINATES\r\n")

        # Receive a response from the BG96 modem
        response = bg96_socket.recv(1024)

        # Close the socket connection
        # TODO: We probably want to keep this socket open for continuing broadcast
        # bg96_socket.close()

        # Emit the response to the client
        emit("GPS", response.decode("utf-8"), broadcast=True)

    except Exception as e:
        print("Error: ", str(e))
        emit("GPS", "Error occurred connecting to drone", broadcast=True)


@socketio.on("request_sensor")
def handle_custom_event():
    print("[REQUEST] turn on drone GPS coordinates")

    try:
        connect_to_hardware()

        # Send a message to the BG96 modem
        bg96_socket.send(b"TURN ON SENSOR READINGS\r\n")

        # Receive a response from the BG96 modem
        response = bg96_socket.recv(1024)

        # Close the socket connection
        # TODO: We probably want to keep this socket open for continuing broadcast
        # bg96_socket.close()

        # Emit the response to the client
        emit("sensor", response.decode("utf-8"), broadcast=True)

    except Exception as e:
        print("Error: ", str(e))
        emit("sensor", "Error occurred requesting sensor readings", broadcast=True)


@socketio.on("disconnect")
def handle_disconnect():
    print("client disconnected")
    emit("disconnect", f"user:{request.sid} has been disconnected", broadcast=True)
