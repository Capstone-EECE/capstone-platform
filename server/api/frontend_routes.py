import base64
from flask import Blueprint
import nanoid
import requests
from server.core.requestTracker import RequestTracker
endpoints = Blueprint("endpoints", __name__)

REQUEST_CODE_CONNECT = "R1111"
REQUEST_CODE_STARTCOORDS = "R2222"
REQUEST_CODE_STOPCOORDS = "R2233"
REQUEST_CODE_STARTSENSOR = "R5555"
REQUEST_CODE_STOPSENSOR = "R5566"
REQUEST_CODE_BATTERY = "R8888"

REQUEST_ID_SIZE = 10
WEBHOOK_BASE = "https://dashboard.hologram.io/api/1/" # os.environ.get("WEBHOOK_BASE")
WEBHOOK_GUID = "ccd213a18dfb8148d43046094c476587" # os.environ.get("WEBHOOK_GUID")
DEVICE_ID = 2566408 # os.environ.get("DEVICE_ID")
webhook_send_message_url = WEBHOOK_BASE + f"devices/messages/{DEVICE_ID}/{WEBHOOK_GUID}"

B64_TEMPLATE = """
    {
        "base64data": "%s=="
    }
    """

g_requestTracker = RequestTracker()

def _send_command_to_device(requestID: str, rawString: str):
    bytestring = B64_TEMPLATE
    print(rawString)

    base64_encoded_data = base64.b64encode(rawString.encode()).decode()
    bytestring = bytestring % base64_encoded_data
    print(bytestring)
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(
            url=webhook_send_message_url,
            data=bytestring,
            headers=headers
        )
        return response
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return ("Error. Check server log for info", 418)


@endpoints.route("/connect", methods=["GET"])
def frontend_connect_to_device():
    """"
        Fire and forget method to send server info to device
        UI will update with ACK from device modem_ack()
    """
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    ngrok_code = "55aa"
    rawString = f"{REQUEST_CODE_CONNECT};\n{ngrok_code};\n{request_id};\n"

    response = _send_command_to_device(requestID=request_id, rawString=rawString)
        
    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return (f"Failed to send data. HTTP Status Code: {response.status_code}")
    
    g_requestTracker.newRequest(request_id)
    return ("Connection request sent. Wait for ACK", 200)

@endpoints.route("/gps/start", methods=["GET"])
def frontend_start_coordinate_ingestion():
    """
        Request that the device start sending its current GPS coordinates
    """
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    rawString = f"{REQUEST_CODE_STARTCOORDS};\n{request_id};\n"

    response = _send_command_to_device(requestID=request_id, rawString=rawString)

    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return (f"Failed to send data. HTTP Status Code: {response.status_code}")

    g_requestTracker.newRequest(request_id)
    return ("START COORDS Request Sent. Wait for ACK and Coordinates in POST", 200)

@endpoints.route("gps/stop", methods=["GET"])
def frontend_stop_coordinate_ingestion():
    """
        Request that the device stop sending its GPS coordinates
    """
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    rawString = f"{REQUEST_CODE_STOPCOORDS};\n{request_id};\n"

    response = _send_command_to_device(requestID=request_id, rawString=rawString)

    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return (f"Failed to send data. HTTP Status Code: {response.status_code}")

    g_requestTracker.newRequest(request_id)
    return ("STOP COORDS Request Sent. Wait for ACK in POST", 200)

@endpoints.route("/points/start", methods=["GET"])
def frontend_start_points_ingestion():
    """
        Request that the device start taking and sending sensor readings
    """
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    rawString = f"{REQUEST_CODE_STARTSENSOR};\n{request_id};\n"

    response = _send_command_to_device(requestID=request_id, rawString=rawString)

    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return (f"Failed to send data. HTTP Status Code: {response.status_code}")
    
    g_requestTracker.newRequest(request_id)
    return ("START SENSOR READING Request Sent. Wait for ACK and data in POST", 200)

@endpoints.route("/points/stop", methods=["GET"])
def frontend_stop_points_ingestion():
    """
        Request that the device stop taking and sending sensor readings
    """
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    rawString = f"{REQUEST_CODE_STOPSENSOR};\n{request_id};\n"

    response = _send_command_to_device(requestID=request_id, rawString=rawString)

    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return (f"Failed to send data. HTTP Status Code: {response.status_code}")
    
    g_requestTracker.newRequest(request_id)
    return ("STOP SENSOR READING Request Sent. Wait for ACK in POST", 200)

@endpoints.route("battery", methods=["GET"])
def frontend_get_battery_status():
    """
        Request updated battery information from device
    """
    request_id = nanoid.generate(size=REQUEST_ID_SIZE)
    rawString = f"{REQUEST_CODE_BATTERY};\n{request_id};\n"

    response = _send_command_to_device(requestID=request_id, rawString=rawString)

    if not response.ok:
        print(f"Failed to send data. HTTP Status Code: {response.status_code}")
        print(response.text)
        return (f"Failed to send data. HTTP Status Code: {response.status_code}")
    
    g_requestTracker.newRequest(request_id)
    return ("BATTERY Request Sent. Wait for ACK and data in POST", 200)