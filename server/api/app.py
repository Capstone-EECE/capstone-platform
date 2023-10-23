# import apig_wsgi
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from .routes import endpoints

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000", logger=True)

app.register_blueprint(endpoints, url_prefix="/capstone")


# lambda_handler = apig_wsgi.make_lambda_handler(app)
