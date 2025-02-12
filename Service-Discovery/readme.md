# **Microservices-Based Service Discovery and Communication System**

## **📌 Overview**
This project implements a **service discovery and communication system** using **Flask-based microservices**. It allows microservices to register themselves, communicate with each other via a **Service Registrar**, and dynamically manage active services.

### **🎯 Goals**
- Provide a **centralized discovery system** so services can locate each other dynamically.
- Enable **seamless communication** between microservices without hardcoding addresses.
- Implement **fault tolerance** by automatically removing inactive services.
- Leverage **Ollama AI** for generating intelligent responses in a microservices-based architecture.

### **📌 Why Service Discovery?**
In a microservices architecture, services need to communicate but **do not always know where other services are running**. For example:

- A user wants to ask **Ollama AI** a question but **does not know its address**.
- Instead of hardcoding the service's address, they **query the Service Registrar**.
- The **Service Registrar finds and forwards the request** to the correct service.
- The user **gets the response without needing to know where Ollama is running**.

This setup ensures **dynamic service discovery** and enables **flexible communication** between services.

---
## **📌 1. Project Structure**
This project contains two microservices:

### **🔹 Service Registrar (`service_registrar.py`)**
- Runs on **port 5001**.
- Manages the registration and discovery of services.
- Handles message forwarding between services.

### **🔹 Ollama Microservice (`app.py`)**
- Runs on **port 5000**.
- Handles AI-based responses using Ollama.
- Receives messages forwarded by the Service Registrar.

### **📂 Directory Structure**
```
📁 project-folder
│-- 📄 service_registrar.py  # Service Discovery System
│-- 📄 app.py                # Ollama AI Microservice
│-- 📄 README.md             # Documentation
│-- 📄 requirements.txt      # Python dependencies
```

---
## **📌 2. Installation & Setup**
### **🔹 Step 1: Install Dependencies**
Ensure Python (>=3.8) is installed. Install required dependencies:
```sh
pip install flask requests
```

### **🔹 Step 2: Start the Service Registrar**
In **one terminal**, start the service discovery system:
```sh
python service_registrar.py
```
Expected Output:
```
Running on http://0.0.0.0:5001
```

### **🔹 Step 3: Start the Ollama Microservice**
In **another terminal**, start the AI microservice:
```sh
python app.py
```
Expected Output:
```
Starting Flask server with Ollama streaming...
{"message": "Service ollama_service registered at http://127.0.0.1:5000"}
```

---
## **📌 3. How It Works**
### **1️⃣ Service Registration**
When a microservice starts, it **registers itself** with the Service Registrar.

📌 **Check registered services:**
```sh
curl -X GET http://127.0.0.1:5001/services
```
✅ Expected Output:
```json
{
    "services": {
        "ollama_service": "http://127.0.0.1:5000"
    }
}
```

---
### **2️⃣ Heartbeat System**
Each microservice sends a **heartbeat every 2 minutes** to indicate it is still active. If a service **fails to send a heartbeat for 5 minutes**, it is automatically removed from the registry.

📌 **Manually send a heartbeat (for testing):**
```sh
curl -X POST http://127.0.0.1:5001/heartbeat \
     -H "Content-Type: application/json" \
     -d '{"service_name": "ollama_service"}'
```
✅ Expected Output:
```json
{
    "message": "Heartbeat received from ollama_service"
}
```

---
### **3️⃣ Service Discovery**
Microservices can query the **Service Registrar** to get the list of available services.

📌 **Fetch all registered services:**
```sh
curl -X GET http://127.0.0.1:5001/services
```
✅ Expected Output:
```json
{
    "services": {
        "ollama_service": "http://127.0.0.1:5000"
    }
}
```

---
### **4️⃣ Service-to-Service Communication**
Microservices can **send messages to each other** through the Service Registrar.

📌 **Send a message from one service to another:**
```sh
curl -X POST http://127.0.0.1:5001/forward \
     -H "Content-Type: application/json" \
     -d '{"from": "test_service", "to": "ollama_service", "message": "What is AI?"}'
```
✅ Expected Response (Ollama's Answer):
```json
{
    "message": "Artificial Intelligence (AI) is the simulation of human intelligence in machines."
}
```

---
### **5️⃣ AI Response Handling**
The `ollama_service` sends messages to **Ollama AI** and returns the response.

📌 **Send a question directly to Ollama:**
```sh
curl -X POST http://127.0.0.1:5000/receive \
     -H "Content-Type: application/json" \
     -d '{"from": "service_registrar", "message": "Capital of India?"}'
```
✅ Expected Output:
```json
{
    "message": "The capital of India is New Delhi."
}
```

---
## **📌 4. Troubleshooting**
| **Issue** | **Solution** |
|-----------|-------------|
| `Failed to reach ollama_service at http://127.0.0.1:5000` | Ensure `app.py` is running and registered correctly. Use `GET /services` to verify. |
| `JSONDecodeError` when parsing Ollama response | Ensure `app.py` correctly extracts only the assistant’s response. |
| `Service disappears from registry` | Make sure the service is sending heartbeats. |


