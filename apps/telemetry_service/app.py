from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)

telemetry_db = []
alerts_db = []

def parse_datetime(value):
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        abort(400, description="Неверный формат времени. Используйте ISO 8601.")

@app.route("/telemetry/<string:device_id>", methods=["GET"])
def get_telemetry(device_id):
    filtered = [t for t in telemetry_db if t["device_id"] == device_id]
    return jsonify(filtered)

@app.route("/telemetry/alert", methods=["POST"])
def set_alert():
    data = request.get_json()
    if not data:
        abort(400, description="Нет JSON-данных")
    required_fields = ("device_id", "threshold_temperature", "notify_email")
    if not all(k in data for k in required_fields):
        abort(400, description="Отсутствуют обязательные поля")
    alerts_db.append({
        "device_id": data["device_id"],
        "threshold_temperature": float(data["threshold_temperature"]),
        "notify_email": data["notify_email"]
    })
    return jsonify({"status": "alert configured"}), 201

@app.route("/telemetry/alerts/<string:device_id>", methods=["GET"])
def get_alerts(device_id):
    filtered = [a for a in alerts_db if a["device_id"] == device_id]
    return jsonify(filtered)

@app.route("/telemetry", methods=["POST"])
def add_telemetry():
    data = request.get_json()
    required_fields = ("device_id", "timestamp", "temperature", "humidity")
    if not all(k in data for k in required_fields):
        abort(400, description="Отсутствуют обязательные поля")
    telemetry_entry = {
        "device_id": data["device_id"],
        "timestamp": parse_datetime(data["timestamp"]).isoformat(),
        "temperature": float(data["temperature"]),
        "humidity": float(data["humidity"]),
    }
    telemetry_db.append(telemetry_entry)
    return jsonify({"status": "telemetry saved"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
