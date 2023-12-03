from flask import request
from flask_socketio import SocketIO, emit

socketio = SocketIO(cors_allowed_origins="*", logger=True)


@socketio.on("connect")
def handle_connect():
    print(f"Client id:{request.sid} is connected")
    print("*************************************")
    emit("battery", 20)


@socketio.on("disconnect")
def handle_disconnect():
    print("client disconnected")
    emit("disconnect", f"user:{request.sid} has been disconnected", broadcast=True)
