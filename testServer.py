import base64
import nanoid
import requests

from server.core.constants import (
    B64_TEMPLATE,
    DEVICE_ID,
    REQUEST_CODE_STOPSENSOR,
    WEBHOOK_BASE,
    WEBHOOK_GUID,
)

webhook_send_message_url = WEBHOOK_BASE + f"devices/messages/{DEVICE_ID}/{WEBHOOK_GUID}"

base64_encoded_data = base64.b64encode("Hello World!".encode()).decode()
print(base64_encoded_data)


def _send_command_to_device(rawString: str):
    bytestring = B64_TEMPLATE
    print(rawString)

    base64_encoded_data = base64.b64encode(rawString.encode()).decode()
    bytestring = bytestring % base64_encoded_data
    print(bytestring)
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            url=webhook_send_message_url, data=bytestring, headers=headers
        )
        return response

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return ("Error. Check server log for info", 418)


request_id = nanoid.generate(size=10)
ngrok_code = "55aa"
rawString = f"{REQUEST_CODE_STOPSENSOR};\n{request_id};\n"

response = _send_command_to_device(rawString)
if not response.ok:
    print(f"Failed to send data. HTTP Status Code: {response.status_code}")
    print(response.text)
else:
    print("Data sent successfully")
