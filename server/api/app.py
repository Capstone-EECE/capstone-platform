# app.py
from flask import Flask
from flask_cors import CORS
from server.api.dummy_routes import dummy_endpoints
from server.api.frontend_routes import frontend_endpoints
from server.api.modem_routes import modem_endpoints
from server.api.socket_events import socketio

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# app.config['SECRET_KEY'] = 'your_secret_key'

app.register_blueprint(modem_endpoints, url_prefix="/modem")
app.register_blueprint(frontend_endpoints, url_prefix="/frontend")
app.register_blueprint(dummy_endpoints, url_prefix="/dummy")

if __name__ == "__main__":
    socketio.init_app(app)
    socketio.run(app, host="0.0.0.0", debug=True, port=5235)
