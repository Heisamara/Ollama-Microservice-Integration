# Ollama-based Text Generation Microservice

## Overview
This project is a microservice that utilizes **Ollama** to process and generate text responses. The application is built with **Flask** and can be tested using **Postman**.

## Prerequisites
Before running the application, ensure the following:
- **Python** is installed on your system.
- **Ollama** is installed and running.
- **Postman** (or an equivalent API testing tool) is available for testing.

## Installation & Setup

### Step 1: Install Ollama
Download and install **Ollama** on your local desktop from the official website.

### Step 2: Verify Ollama Version
Ensure that the installed **Ollama** version is **Llama 3.2**. If it's not installed, update or install the required version by running:
```sh
ollama pull llama3:2
```

### Step 3: Start Ollama
Make sure Ollama is running before proceeding.
```sh
ollama serve
```

### Step 4: Run the Application
Navigate to the project directory and run:
```sh
python app.py
```

### Step 5: Retrieve the API Endpoint
Once the application starts, it will generate two IP addresses. **Use the first IP address** for testing the API.

## Using the API with Postman

### Step 1: Open Postman
Launch **Postman** or any API testing tool of your choice.

### Step 2: Set Up a POST Request
- **Method**: `POST`
- **URL**: `http://0.0.0.0/generate`
- **Headers**: `Content-Type: application/json`
- **Body (JSON Payload)**:
  ```json
  {
    "text": "What is the capital of India?"
  }
  ```
- Replace the value of `text` with your own query.

### Step 3: Send the Request
Click **Send** and you will receive a response containing the generated output from Ollama.

## Example Response
```json
{
  "response": "The capital of India is New Delhi."
}
```

## Troubleshooting
- If you encounter **connection issues**, verify that **Ollama** is running.
- If you receive an **incorrect version error**, reinstall the correct **Llama 3.2** model.
- Ensure **Flask** is properly installed and running without errors.


