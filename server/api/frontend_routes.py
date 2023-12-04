import base64

import nanoid
import requests
from flask import Blueprint
from server.api.socket_events import socketio
from server.core.constants import (
    B64_TEMPLATE,
    DEVICE_ID,
    REQUEST_CODE_BATTERY,
    REQUEST_CODE_CONNECT,
    REQUEST_CODE_STARTCOORDS,
    REQUEST_CODE_STARTSENSOR,
    REQUEST_CODE_STOPCOORDS,
    REQUEST_CODE_STOPSENSOR,
    REQUEST_ID_SIZE,
    WEBHOOK_BASE,
    WEBHOOK_GUID,
)
from server.core.requestTracker import RequestTracker

frontend_endpoints = Blueprint("frontend_endpoints", __name__)

webhook_send_message_url = WEBHOOK_BASE + f"devices/messages/{DEVICE_ID}/{WEBHOOK_GUID}"
g_requestTracker = RequestTracker()


def _send_command_to_device(rawString: str):
    bytestring = B64_TEMPLATE

    base64_encoded_data = base64.b64encode(rawString.encode()).decode()
    bytestring = bytestring % base64_encoded_data
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            url=webhook_send_message_url, data=bytestring, headers=headers
        )
        return response

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return ("Error. Check server log for info", 418)


@frontend_endpoints.route("/connect", methods=["GET"])
def frontend_connect_to_device():
    """ "
    Fire and forget method to send server info to device
    UI will update with ACK from device modem_ack()
    FORMAT: XXXX-NGROKIP(3D-2D-3D-2D)
    """
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    ngrok_code = "55aa"
    rawString = f"{REQUEST_CODE_CONNECT};\n{ngrok_code};\n{request_id};\n"
    response = _send_command_to_device(rawString=rawString)

    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return f"Failed to send data. HTTP Status Code: {response.status_code}"

    g_requestTracker.newRequest(request_id)
    return ("Connection request sent. Wait for ACK", 200)


@frontend_endpoints.route("/gps/start", methods=["GET"])
def frontend_start_coordinate_ingestion():
    """
    Request that the device start sending its current GPS coordinates
    """
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    rawString = f"{REQUEST_CODE_STARTCOORDS};\n{request_id};\n"

    response = _send_command_to_device(rawString=rawString)
    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return f"Failed to send data. HTTP Status Code: {response.status_code}"

    g_requestTracker.newRequest(request_id)
    return ("START COORDS Request Sent. Wait for ACK and Coordinates in POST", 200)


@frontend_endpoints.route("/gps/stop", methods=["GET"])
def frontend_stop_coordinate_ingestion():
    """
    Request that the device stop sending its GPS coordinates
    """

    print("STOPPPING")
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    rawString = f"{REQUEST_CODE_STOPCOORDS};\n{request_id};\n"

    response = _send_command_to_device(rawString=rawString)

    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return f"Failed to send data. HTTP Status Code: {response.status_code}"

    g_requestTracker.newRequest(request_id)
    return ("STOP COORDS Request Sent. Wait for ACK in POST", 200)


@frontend_endpoints.route("/points/start", methods=["GET"])
def frontend_start_points_ingestion():
    """
    Request that the device start taking and sending sensor readings
    """
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    rawString = f"{REQUEST_CODE_STARTSENSOR};\n{request_id};\n"

    response = _send_command_to_device(rawString=rawString)

    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return f"Failed to send data. HTTP Status Code: {response.status_code}"

    g_requestTracker.newRequest(request_id)
    return ("START SENSOR READING Request Sent. Wait for ACK and data in POST", 200)


@frontend_endpoints.route("/points/stop", methods=["GET"])
def frontend_stop_points_ingestion():
    """
    Request that the device stop taking and sending sensor readings
    """
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    rawString = f"{REQUEST_CODE_STOPSENSOR};\n{request_id};\n"

    response = _send_command_to_device(rawString=rawString)

    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return f"Failed to send data. HTTP Status Code: {response.status_code}"

    g_requestTracker.newRequest(request_id)
    return ("STOP SENSOR READING Request Sent. Wait for ACK in POST", 200)


@frontend_endpoints.route("/battery", methods=["GET"])
def frontend_get_battery_status():
    """
    Request updated battery information from device
    """
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    rawString = f"{REQUEST_CODE_BATTERY};\n{request_id};\n"

    response = _send_command_to_device(rawString=rawString)

    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return f"Failed to send data. HTTP Status Code: {response.status_code}"

    g_requestTracker.newRequest(request_id)
    return ("BATTERY Request Sent. Wait for ACK and data in POST", 200)


@frontend_endpoints.route("/login", methods=["GET"])
def login_attempt():
    return (
        {"success": True, "body": {"name": "-", "message": "Login Succesful"}},
        200,
    )
