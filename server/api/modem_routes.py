"""
Collection of Flask API route functions
https://realpython.com/flask-blueprint/
"""

from flask import Blueprint, json, request
from server.api.frontend_routes import g_requestTracker

modem_endpoints = Blueprint("modem_endpoints", __name__)


@modem_endpoints.route("/ACK", methods=["POST"])
def modem_ack():
    """
    Handler for simple ACKs from the modem
    {requestID: string}
    """
    try:
        if request.content_length > 100:
            return {
                "status": "error",
                "message": "Content too large",
            }
        data_json = json.loads(request.get_data())
        request_id = data_json["requestID"]
    except Exception as e:
        return {"status": "error", "message": str(e)}

    g_requestTracker.updateRequest(requestID=request_id, status="ACK")
    return "ACK", 200


@modem_endpoints.route("/gps", methods=["POST"])
def modem_post_coords():
    """Handler for coordinate data sent from the modem recieved as:
    {
        requestID: string
        location: {
            lat: number,
            lng: number,
        }
        accuracy: number,
    }
    """

    try:
        if request.content_length > 1000:
            return {
                "status": "error",
                "message": "Content too large",
            }

        data_json = json.loads(request.get_data())
        accuracy = data_json["accuracy"]
        lat = data_json["location"]["lat"]
        lng = data_json["location"]["lng"]
        request_id = data_json["requestID"]

    except Exception as e:
        return {"status": "error", "message": str(e)}

    g_requestTracker.updateRequest(requestID=request_id, status="Coordinates Received")
    return {
        "status": "success",
        "message": f"Coordinates ({lat}, {lng}), and accuracy ({accuracy}) received successfully",
    }


@modem_endpoints.route("/sensorData", methods=["POST"])
def modem_post_sensor_data():
    """Handler for sensor data sent from the modem received as:
    {
        "requestID": %s
        "timestamp_begin": %lu,
        "timestamp_end": %lu,
        "readings": [%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f],
        "count": %d
    }
    """

    try:
        if request.content_length > 1000:
            return {
                "status": "error",
                "message": "Content too large",
            }

        data_json = json.loads(request.get_data())
        reading_count = int(data_json["count"])
        readings = data_json["readings"]
        request_id = data_json["requestID"]

    except Exception as e:
        return {"status": "error", "message": str(e)}

    g_requestTracker.updateRequest(requestID=request_id, status="Sensor Data Received")
    return {
        "status": "success",
        "message": "successfully sent sensor data",
    }


@modem_endpoints.route("/battery", methods=["POST"])
def modem_post_battery_status():
    """Handler for sensor data sent from the modem received as:
    {
        "requestID": %s
        "batteryReading": %d
    }
    """

    try:
        if request.content_length > 1000:
            return {
                "status": "error",
                "message": "Content too large",
            }

        data_json = json.loads(request.get_data())
        batteryReading = data_json["batteryReading"]
        request_id = data_json["requestID"]

    except Exception as e:
        return {"status": "error", "message": str(e)}

    g_requestTracker.updateRequest(
        requestID=request_id, status="Battery Status Received"
    )
    return {
        "status": "success",
        "message": "successfully sent sensor data",
    }
