# 🚀 FastAPI Cloud Run Job Proxy

A production-ready FastAPI service deployed on Google Cloud Run for secure service-to-service communication between Toolbox and Jobs Agent services.

---

## ⚡ Overview

This system is a cloud-native job orchestration platform built using FastAPI and Google Cloud Run. It enables secure communication between microservices using IAM authentication and service accounts.

It consists of:

- **FastAPI Service** → API gateway
- **Toolbox Service** → backend execution layer
- **Jobs Agent Service** → orchestration + AI (Vertex AI / Gemini)
- **Google Cloud Run** → serverless compute
- **IAM authentication** → secure service-to-service communication

---

## 📦 Tech Stack

- FastAPI
- Uvicorn
- Python 3.10+
- Docker
- Google Cloud Run
- Google IAM
- Vertex AI (Gemini)

---

## 📁 Project Structure


fastapi-job-proxy/
│
├── main.py # FastAPI entrypoint
├── requirements.txt # Dependencies
├── Dockerfile # Container definition
└── agent/ # Deployment scripts (Toolbox + Jobs Agent)


---

## 🚀 FastAPI Features

### ✔ API Layer
- REST APIs for job execution
- Health check endpoint
- Secure service-to-service communication

---

## 🧪 Example API Endpoints

### Health Check

```http
GET /health

Response:

{
  "status": "ok"
}
Run Job
POST /run-job

Request:

{
  "job_name": "data-processing",
  "payload": {
    "key": "value"
  }
}

Response:

{
  "message": "Job triggered successfully"
}
```

## 🐳 Docker
Build Image
docker build -t fastapi-job-proxy .
Run Container
docker run -p 8080:8080 fastapi-job-proxy
☁️ Cloud Architecture
FastAPI Service
      ↓
Toolbox Service (Cloud Run)
      ↓
Jobs Agent Service (Cloud Run)
      ↓
Vertex AI / External APIs
🔐 Security
IAM-based service-to-service authentication
Service account impersonation
Custom audiences for Cloud Run services
Secure token-based API calls
🧠 Use Cases
AI-powered job orchestration
Workflow automation pipelines
Microservice communication layer
Cloud-native backend systems
🚀 Deployment Flow
Deploy Toolbox service to Cloud Run
Retrieve Toolbox service URL
Deploy Jobs Agent with Toolbox URL injected
Configure IAM permissions
Enable secure service-to-service communication
📌 Notes
Always use service accounts with least privilege
Prefer IAM authentication over public endpoints
Store secrets in Secret Manager (not env vars in production)
