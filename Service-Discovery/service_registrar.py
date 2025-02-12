from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)

# Dictionary to store registered services
services = {}  # Example: { "service1": { "address": "http://127.0.0.1:5002", "last_seen": timestamp } }

# Test route to check if the service registrar is running
@app.route('/')
def home():
    return "Service Registrar is Running!", 200

# Endpoint for registering microservices
@app.route('/register', methods=['POST'])
def register_service():
    data = request.json
    service_name = data.get('service_name')
    address = data.get('address')

    if not service_name or not address:
        return jsonify({"error": "Service name and address required"}), 400

    # Register the service with its last heartbeat timestamp
    services[service_name] = {"address": address, "last_seen": time.time()}
    
    return jsonify({"message": f"Service {service_name} registered at {address}"}), 200

# Endpoint for receiving heartbeats from services
@app.route('/heartbeat', methods=['POST'])
def service_heartbeat():
    data = request.json
    service_name = data.get('service_name')

    if service_name in services:
        services[service_name]['last_seen'] = time.time()
        return jsonify({"message": f"Heartbeat received from {service_name}"}), 200
    else:
        return jsonify({"error": "Service not registered"}), 404


# Endpoint to get a list of registered services
@app.route('/services', methods=['GET'])
def list_services():
    return jsonify({"services": {name: details["address"] for name, details in services.items()}}), 200


# Function to remove services that haven't sent heartbeats in 5 minutes
def remove_stale_services():
    while True:
        time.sleep(30)  # Check every 30 seconds
        now = time.time()
        to_remove = [name for name, details in services.items() if now - details["last_seen"] > 300]

        for service in to_remove:
            del services[service]

        if to_remove:
            print(f"Removed inactive services: {to_remove}")

# Start the cleanup task in the background
threading.Thread(target=remove_stale_services, daemon=True).start()

import requests

# Endpoint to forward messages between services
@app.route('/forward', methods=['POST'])
def forward_message():
    data = request.json
    from_service = data.get("from")
    to_service = data.get("to")
    message = data.get("message")

    if not from_service or not to_service or not message:
        return jsonify({"error": "Missing required fields (from, to, message)"}), 400

    if to_service not in services:
        return jsonify({"error": f"Service {to_service} not found"}), 404

    # Get the address of the target service
    to_service_address = services[to_service]["address"]

    try:
        # Send the message to the target service
        response = requests.post(f"{to_service_address}/receive", json={"from": from_service, "message": message})
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({"error": f"Failed to reach {to_service} at {to_service_address}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
