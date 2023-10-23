from flask_socketio import emit

from ..core.drone_location import get_drone_gps_coordinates
from .app import socketio


@socketio.on("connect")
def handle_connect():
    print("Client connected")


# Assuming you have a function to get and emit drone GPS coordinates
def emit_drone_gps_coordinates():
    while True:
        coordinates = get_drone_gps_coordinates()
        emit("gpsUpdate", coordinates, namespace="/drone")
        socketio.sleep(1)


@socketio.on("disconnect", namespace="/drone")
def handle_drone_disconnect():
    print("Client disconnected from drone namespace")


# Run the background task to emit drone GPS coordinates
# socketio.start_background_task(emit_drone_gps_coordinates)
