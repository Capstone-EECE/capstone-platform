#
#   Request Codes
#
REQUEST_CODE_CONNECT = "R1111"
REQUEST_CODE_STARTCOORDS = "R2222"
REQUEST_CODE_STOPCOORDS = "R2233"
REQUEST_CODE_STARTSENSOR = "R5555"
REQUEST_CODE_STOPSENSOR = "R5566"
REQUEST_CODE_BATTERY = "R8888"

#
#   Request URL components
#
WEBHOOK_BASE = "https://dashboard.hologram.io/api/1/"  # os.environ.get("WEBHOOK_BASE")
WEBHOOK_GUID = "ccd213a18dfb8148d43046094c476587"  # os.environ.get("WEBHOOK_GUID")
B64_TEMPLATE = """
    {
        "base64data": "%s=="
    }
    """
REQUEST_ID_SIZE = 10

#
#   Device info
#
REMOTE_IP = "10.78.132.213"
REMOTE_PORT = 5555
DEVICE_ID = 2566408  # os.environ.get("DEVICE_ID")
