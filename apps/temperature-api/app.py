from flask import Flask, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

SENSOR_MAP = {
    "1": "Living Room",
    "2": "Bedroom",
    "3": "Kitchen"
}

LOCATION_MAP = {v: k for k, v in SENSOR_MAP.items()}

@app.route('/temperature', methods=['GET'])
def get_temperature():
    location = request.args.get('location', '')
    sensor_id = request.args.get('sensorID', '')

    if not location:
        location = SENSOR_MAP.get(sensor_id, 'Unknown')

    if not sensor_id:
        sensor_id = LOCATION_MAP.get(location, '0')

    temperature = round(random.uniform(18.0, 30.0), 1)

    response = {
        "sensorId": sensor_id,
        "location": location,
        "temperature": temperature,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
