from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
import time
import threading
import socket

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

# Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/chat"

# Service Discovery Settings
SERVICE_NAME = "ollama_service"
REGISTRAR_URL = "http://10.0.0.109:5001"  # Machine A (Service Registrar)

# Automatically determine Machine B's IP
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to an external server to get the IP
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Failed to get local IP: {e}")
        return "127.0.0.1"  # Fallback

SERVICE_ADDRESS = f"http://{get_local_ip()}:5000"  # Use actual local IP

# Function to register with the Service Registrar
def register_service():
    try:
        data = {"service_name": SERVICE_NAME, "address": SERVICE_ADDRESS}
        response = requests.post(f"{REGISTRAR_URL}/register", json=data)
        print(response.json())  # Debugging output
    except Exception as e:
        print(f"Failed to register service: {e}")

# Function to send heartbeats every 2 minutes
def send_heartbeat():
    while True:
        time.sleep(120)
        try:
            requests.post(f"{REGISTRAR_URL}/heartbeat", json={"service_name": SERVICE_NAME})
            print("Heartbeat sent to service registrar.")
        except Exception as e:
            print(f"Failed to send heartbeat: {e}")

# Start the heartbeat in a background thread
threading.Thread(target=send_heartbeat, daemon=True).start()

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.json
        user_input = data.get("text", "")

        if not user_input:
            return jsonify({"error": "No text provided"}), 400

        payload = {
            "model": "llama3.2",
            "messages": [{"role": "user", "content": user_input}]
        }

        ollama_response = requests.post(OLLAMA_URL, json=payload, stream=True)

        if ollama_response.status_code != 200:
            return jsonify({"error": f"Ollama returned {ollama_response.status_code}"}), 500

        def stream_response():
            for line in ollama_response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        json_data = json.loads(line)
                        if "message" in json_data and "content" in json_data["message"]:
                            yield json_data["message"]["content"] + " "
                    except json.JSONDecodeError:
                        yield "\n[Error: Could not parse response]\n"

        return Response(stream_response(), content_type="text/plain")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"Starting Flask server on {SERVICE_ADDRESS}...")
    register_service()  # Register with the service registrar
    threading.Thread(target=send_heartbeat, daemon=True).start()  # Start heartbeat thread
    app.run(host='0.0.0.0', port=5000, debug=True)
