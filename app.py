import requests
import json
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/chat"

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        # Get input text from request
        data = request.json
        user_input = data.get("text", "")

        if not user_input:
            return jsonify({"error": "No text provided"}), 400

        # Define the payload for Ollama
        payload = {
            "model": "llama3.2",  # Ensure this matches your local model name
            "messages": [{"role": "user", "content": user_input}]
        }

        # Send the request to Ollama with streaming enabled
        ollama_response = requests.post(OLLAMA_URL, json=payload, stream=True)

        if ollama_response.status_code != 200:
            return jsonify({"error": f"Ollama returned {ollama_response.status_code}"}), 500

        # Stream the response to the client and return response
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
    print("Starting Flask server with Ollama streaming...")
    app.run(host='0.0.0.0', port=5000, debug=True)
