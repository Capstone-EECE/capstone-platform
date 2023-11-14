# import apig_wsgi
import logging
import socket
import time
from http.client import HTTPException

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from routes import endpoints
from socketIO_client import SocketIO as client_socket

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*", logger=True)
app.register_blueprint(endpoints, url_prefix="/capstone")

REMOTE_IP = "10.78.132.213"
REMOTE_PORT = 5555
NGROK_URL = "https://7c66-155-33-134-31.ngrok-free.app"
URL = "7c66-155-33-134-31.ngrok.io"


@socketio.on("connect_drone")
def handle_custom_event():
    print("[REQUEST] turn on drone GPS coordinates")

    try:
        bg96_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Before socket connect")
        time.sleep(1)
        bg96_socket.connect((REMOTE_IP, REMOTE_PORT))
        print("After socket connect")

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


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True, port=5000)


# lambda_handler = apig_wsgi.make_lambda_handler(app)
