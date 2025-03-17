from flask import Flask, request, jsonify, Response
import requests
import json
import time
import threading
import socket

app = Flask(__name__)

# Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/chat"

# Service Discovery Settings
SERVICE_NAME = "ollama_service"
REGISTRAR_URL = "http://10.0.0.109:5001"  # Change this to the actual machine running `service_registrar.py`

# Automatically determine the machine's IP address
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

SERVICE_ADDRESS = f"http://{get_local_ip()}:5000"  # Dynamically set this machine's address

# Function to register with the Service Registrar
def register_service():
    try:
        data = {"service_name": SERVICE_NAME, "address": SERVICE_ADDRESS}
        response = requests.post(f"{REGISTRAR_URL}/register", json=data)
        print(response.json())  # Print response for debugging
    except Exception as e:
        print(f"Failed to register service: {e}")

# Function to send heartbeats every 2 minutes
def send_heartbeat():
    while True:
        time.sleep(120)
        try:
            requests.post(f"{REGISTRAR_URL}/heartbeat", json={"service_name": SERVICE_NAME})
        except Exception as e:
            print(f"Failed to send heartbeat: {e}")

# Start heartbeat in a background thread
threading.Thread(target=send_heartbeat, daemon=True).start()

# Ollama text generation endpoint
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

# Receive messages from other services
@app.route('/receive', methods=['POST'])
def receive_message():
    data = request.json
    sender = data.get("from")
    message = data.get("message")

    print(f"Received message from {sender}: {message}")

    payload = {
        "model": "llama3.2",
        "messages": [{"role": "user", "content": message}]
    }

    try:
        ollama_response = requests.post(OLLAMA_URL, json=payload, stream=True)

        if ollama_response.status_code != 200:
            return jsonify({"error": f"Ollama returned {ollama_response.status_code}"}), 500

        response_message = ""
        for line in ollama_response.iter_lines(decode_unicode=True):
            if line:
                try:
                    json_data = json.loads(line)
                    if "message" in json_data and "content" in json_data["message"]:
                        response_message += json_data["message"]["content"] + " "
                except json.JSONDecodeError:
                    continue  # Skip invalid JSON lines

        return jsonify({"message": response_message.strip()}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to Ollama: {str(e)}"}), 500

if __name__ == '__main__':
    print(f"Starting Flask server on {SERVICE_ADDRESS}...")
    register_service()  # Register this service with the Service Registrar on startup
    app.run(host='0.0.0.0', port=5000, debug=True)
