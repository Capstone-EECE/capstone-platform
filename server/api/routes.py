"""
Collection of Flask API route functions
https://realpython.com/flask-blueprint/
"""
import functools
import logging
import os
from datetime import datetime
from http.client import HTTPException

from flask import Blueprint, json, jsonify, request

endpoints = Blueprint("endpoints", __name__)


@endpoints.get("/")
def test_route():
    temp = "<h1> I miss charly </h1>"
    return (temp, 200)


@endpoints.get("/points")
def test_param():
    return "TEST"


@endpoints.route("/gps", methods=["POST"])
def get_coordinates_modem():
    try:
        data_str = request.args.get("data")

        data = json.loads(data_str)
        print(data)

        # Extract the required information
        location = data.get("location", {})
        lat = location.get("lat")
        lng = location.get("lng")
        accuracy = data.get("accuracy")

        print(accuracy, lat, lng)

        return {
            "status": "success",
            "message": f"Coordinates {accuracy}, {lat}, {lng} received successfully",
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


@endpoints.get("/key/")
def google_key():
    return ("you thought", 200)
