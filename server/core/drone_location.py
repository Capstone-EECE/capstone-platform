import serial


def get_drone_gps_coordinates():
    return
    try:
        with serial.Serial("/dev/ttyS0", 9600, timeout=1) as ser:
            # Send command to request GPS coordinates
            ser.write(b"AT+GPS\r\n")

            # Read and parse response
            response = ser.readline().decode("utf-8")
            # Parse the response to extract GPS coordinates
            latitude, longitude = parse_gps_response(response)

            return {"latitude": latitude, "longitude": longitude}
    except Exception as e:
        print(f"Error while getting GPS coordinates: {str(e)}")
        return None


def parse_gps_response(response):
    # Implement parsing logic specific to your modem's response format
    # Example: Parse NMEA sentences for GPS data
    parts = response.split(",")
    if len(parts) >= 6 and parts[0] == "$GPGGA":
        latitude = float(parts[2]) / 100
        longitude = float(parts[4]) / 100
        return latitude, longitude
    else:
        return None
