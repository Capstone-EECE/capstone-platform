import socket

from flask_socketio import emit

from ..core.drone_location import get_drone_gps_coordinates
from .app import socketio

BG96_DEVICE_PORT = 1234
BG96_DEVICE_IP = "TEMP"


# @socketio.on("connect")
def handle_connect():
    print("Client connected")


# @socketio.on("hello")
def handle_hello(arg):
    try:
        print(arg)  # "world"
        emit("response", "got it", broadcast=True)
    except Exception as e:
        print("Error: ", str(e))
        emit("response", "Error occurred", broadcast=True)


# @socketio.on('connect_drone')
def handle_custom_event():
    print("Received custom_event")

    try:
        # Create a socket connection to the BG96 modem
        bg96_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bg96_socket.connect(("temp", BG96_DEVICE_PORT))

        # Send a message to the BG96 modem
        bg96_socket.send(b"Your Message\r\n")

        # Receive a response from the BG96 modem
        response = bg96_socket.recv(1024)

        # Close the socket connection
        bg96_socket.close()

        # Emit the response to the client
        emit("response", response.decode("utf-8"), broadcast=True)

    except Exception as e:
        print("Error: ", str(e))
        emit("response", "Error occurred", broadcast=True)


# @socketio.on("disconnect")
def handle_drone_disconnect():
    print("Client disconnected from drone namespace")


# Run the background task to emit drone GPS coordinates
# socketio.start_background_task(emit_drone_gps_coordinates)
