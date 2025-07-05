from flask import Flask, request, Response
import requests
from dotenv import load_dotenv
import os
import logging

load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

REQUIRED_ENV_VARS = ["ROUTE_V1", "ROUTE_V2_DEVICES", "ROUTE_V2_TELEMET"]
for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        raise EnvironmentError(f"Переменная окружения {var} не задана.")

@app.route('/api/<version>/<path:subpath>', methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def proxy(version, subpath,):
    if version == "v1":
        if subpath == "sensors" or subpath == "sensors/":
            target_base = os.getenv("ROUTE_V1_SENSORS")    
            subpath= subpath.replace("sensors", "temperature", 1)  
        else:
            target_base = os.getenv("ROUTE_V1")
    elif version == "v2":
        if subpath == "devices" or subpath == "devices/":
            target_base = os.getenv("ROUTE_V2_DEVICES")
        elif subpath == "telemetry" or subpath.startswith("telemet/"):
            target_base = os.getenv("ROUTE_V2_TELEMET")
        else:
            return Response(f"Unsupported v2 subpath: {subpath}", status=404)
    else:
        return Response(f"Unsupported API version: {version}", status=404)

    target_url = f"{target_base.rstrip('/')}/{subpath.lstrip('/')}"
    logging.info(f"Проксируем {request.method} запрос на: {target_url}")

    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ['host', 'content-length', 'connection']
    }

    kwargs = {
        "method": request.method,
        "url": target_url,
        "headers": headers,
        "params": request.args,
        "cookies": request.cookies,
        "allow_redirects": False,
    }

    if request.is_json:
        kwargs["json"] = request.get_json()
    else:
        kwargs["data"] = request.get_data()

    try:
        resp = requests.request(**kwargs)
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при обращении к целевому сервису: {e}")
        return Response(f"Backend error: {e}", status=502)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [
        (k, v) for k, v in resp.headers.items()
        if k.lower() not in excluded_headers
    ]

    return Response(
        response=resp.content,
        status=resp.status_code,
        headers=response_headers
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
