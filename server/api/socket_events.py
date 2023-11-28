from flask import request
from flask_socketio import SocketIO, emit

socketio = SocketIO(cors_allowed_origins="*", logger=True)


@socketio.on("connect")
def handle_connect():
    print(f"Client id:{request.sid} is connected")
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


@socketio.on("disconnect")
def handle_disconnect():
    print("client disconnected")
    emit("disconnect", f"user:{request.sid} has been disconnected", broadcast=True)
