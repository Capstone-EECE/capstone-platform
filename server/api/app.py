# import apig_wsgi
from flask import Flask
from flask_cors import CORS

from .routes import endpoints

app = Flask(__name__)
CORS(app)


app.register_blueprint(endpoints, url_prefix="/capstone")

# lambda_handler = apig_wsgi.make_lambda_handler(app)
