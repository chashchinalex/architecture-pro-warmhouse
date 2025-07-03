        from flask import Flask, jsonify, request, abort

        app = Flask(__name__)

        devices_db = []

        @app.route("/devices", methods=["GET"])
        def list_devices():
            return jsonify(devices_db)

        @app.route("/devices", methods=["POST"])
        def register_device():
            data = request.get_json()
            if not data or not all(k in data for k in ("device_id", "name", "location")):
                abort(400, description="Missing device data")

            if any(d["device_id"] == data["device_id"] for d in devices_db):
                abort(400, description="Device already exists")

            devices_db.append(data)
            return jsonify({"status": "device registered"}), 201

        @app.route("/devices/<string:device_id>", methods=["GET"])
        def get_device(device_id):
            for device in devices_db:
                if device["device_id"] == device_id:
                    return jsonify(device)
            abort(404, description="Device not found")

        if __name__ == "__main__":
            app.run(host="0.0.0.0", port=8080)
