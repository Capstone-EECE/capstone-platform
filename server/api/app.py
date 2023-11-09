# import apig_wsgi
import logging

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

# from .routes import endpoints

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*", logger=True)
# app.register_blueprint(endpoints, url_prefix="/capstone")


@app.route("/http-example")
def http_call():
    data = {"data": "this text was fetched using an http call"}
    return jsonify(data)


@socketio.on("connect")
def handle_connect():
    print(request.sid)
    print("client connected")
    print("*************************************")
    emit("connected", f"id:{request.sid} is connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("client disconnected")
    emit("disconnect", f"user:{request.sid} has been disconnected", broadcast=True)


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


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)


# lambda_handler = apig_wsgi.make_lambda_handler(app)
