# 🚀 FastAPI Cloud Run Job Proxy + ADK Agent + MCP Toolbox

A production-ready cloud-native platform for secure AI-powered job orchestration using FastAPI, Google Cloud Run, ADK Agents, and MCP Toolbox integration.

---

## ⚡ Overview

This project provides a secure service-to-service architecture for orchestrating AI workflows using Google Cloud technologies.

The platform enables:

- AI agent orchestration with ADK
- Secure inter-service communication using IAM
- MCP Toolbox integration for backend execution
- Vertex AI / Gemini-powered intelligent workflows
- Fully serverless deployment on Cloud Run

---

## 🏗️ Architecture
```
┌─────────────────────────────┐
│ FastAPI Proxy Service       │
│ (Cloud Run)                 │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Jobs Agent Service          │
│ ADK + Gemini + Vertex AI    │
│ (Cloud Run)                 │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ MCP Toolbox Service         │
│ Backend Execution Layer     │
│ (Cloud Run)                 │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Vertex AI / External APIs   │
└─────────────────────────────┘
```
---

## ✨ Features
✔ FastAPI Proxy Layer
- REST API endpoints
- Secure token generation
- Cloud Run integration
- Health check endpoints
- Agent execution APIs
  
✔ Jobs Agent (ADK)
- AI orchestration layer
- Gemini integration
- Toolbox tool invocation
- Vertex AI integration
  
✔ MCP Toolbox
- Backend execution engine
- Tool abstraction layer
- Cloud-native deployment
  
✔ Security
- IAM-based authentication
- OIDC identity tokens
- Service account impersonation
- Cloud Run custom audiences
- Secure service-to-service communication

---

## 📦 Tech Stack

- FastAPI
- Uvicorn
- Python 3.10+
- Docker
- Google Cloud Run
- Google IAM
- Vertex AI (Gemini)
- ADK
- MCP Toolbox

---

## 📁 Project Structure

```text
fastapi-job-proxy/           # API proxy for MCP agent and toolbox
│
├── main.py              # FastAPI entrypoint
├── requirements.txt     # Dependencies
├── Dockerfile           # FastAPI container definition
│
agent/                   # Deployment scripts (Toolbox + Jobs Agent)
│
├── deploy-toolbox
│    │
│    ├── Dockerfile       # Toolbox container definition
│    ├── tools.yaml       # MCP Toolbox container definition
├── jobs_agent
│    │
│    ├── agent.py         # MCP agent script
│    ├── .env             # Environment variables
├── Dockerfile            # Jobs Agent container definition
```

---

## 🚀 FastAPI Features

### ✔ API Layer

- REST APIs for job execution
- Health check endpoint
- Secure service-to-service communication

---

## 🐳 Docker

### Build Image

```bash
cd fastapi-job-proxy/
docker build -t fastapi-job-proxy .
```

### Run Container

```bash
docker run -p 8080:8080 fastapi-job-proxy
```

---

## ☁️ Cloud Architecture

```text
FastAPI Proxy Service (Cloud Run)
      ↓
Jobs Agent Service (Cloud Run)
      ↓
MCP Toolbox Service (Cloud Run)
      ↓
Vertex AI / External APIs
```

---

## 🚀 Deployment Commands

### Deploy FastApi Proxy Service

```bash
gcloud run deploy fastapi-job-proxy --source . --region us-central1 --project=waybackhome-qxln4tprji8q9zklz8 --allow-unauthenticated --service-account fastapi-job-proxy@waybackhome-qxln4tprji8q9zklz8.iam.gserviceaccount.com
```

### Deploy MCP Toolbox Service

```bash
cd agent/
gcloud run deploy toolbox-service \
  --source deploy-toolbox/ \
  --region $REGION \
  --project=$GOOGLE_CLOUD_PROJECT \
  --set-env-vars "DB_PASSWORD=$DB_PASSWORD,DB_INSTANCE=$DB_INSTANCE,DB_NAME=$DB_NAME,GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,REGION=$REGION,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION" \
  --quiet > logs/deploy_toolbox.log 2>&1 &
```

---

### Retrieve Toolbox URL

```bash
TOOLBOX_URL=$(gcloud run services describe toolbox-service \
  --region=$REGION \
  --project=$GOOGLE_CLOUD_PROJECT \
  --format='value(status.url)')

echo "Toolbox URL: $TOOLBOX_URL"
```

---

### Deploy Jobs Agent

```bash
gcloud run deploy jobs-agent \
  --source jobs-agent \
  --region $REGION \
  --project=$GOOGLE_CLOUD_PROJECT \
  --set-env-vars "TOOLBOX_URL=$TOOLBOX_URL,GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_GENAI_USE_VERTEXAI=TRUE"
```

---

### Retrieve Agent URL

```bash
AGENT_URL=$(gcloud run services describe jobs-agent \
  --region=$REGION \
  --project=$GOOGLE_CLOUD_PROJECT \
  --format='value(status.url)')

echo "Agent URL: $AGENT_URL"
```

---

### Configure Custom Audiences

```bash
gcloud run services update jobs-agent \
  --add-custom-audiences=jobs-agent \
  --project=waybackhome-qxln4tprji8q9zklz8 \
  --region=us-central1
```

---

### Alternatively, Deploy Sidecar Version (Jobs Agent + Toolbox)

```bash
gcloud run services replace service.yaml \
  --project=waybackhome-qxln4tprji8q9zklz8 \
  --region=$REGION
```

---

### Describe MCP Service

```bash
gcloud run services describe jobs-agent-mcp \
  --region=$REGION \
  --project=waybackhome-qxln4tprji8q9zklz8
```

---

### Generate Identity Token

```bash
gcloud auth print-identity-token \
  --impersonate-service-account way-back-home-sa@waybackhome-qxln4tprji8q9zklz8.iam.gserviceaccount.com \
  --audiences='jobs-agent' \
  --project=waybackhome-qxln4tprji8q9zklz8
```

---

## 🔐 Security

- IAM-based service-to-service authentication
- Service account impersonation
- Custom audiences for Cloud Run services
- Secure token-based API calls

---

## 🧠 Use Cases

- AI-powered job orchestration
- Workflow automation pipelines
- Microservice communication layer
- Cloud-native backend systems

---

## 🚀 Demo

1. API list
<img width="1022" height="636" alt="image" src="https://github.com/user-attachments/assets/f22fd799-b5d4-4fdf-bb0b-645e39fc749a" />

2. POST /generate-token Generate Token
<img width="1744" height="710" alt="image" src="https://github.com/user-attachments/assets/25b78d90-1fa9-4f52-8952-fdb84b4211df" />

3. POST /run-agent Run Agent
<img width="1756" height="884" alt="image" src="https://github.com/user-attachments/assets/602e1594-920c-4198-b7bb-011241ef80c0" />

<img width="1757" height="812" alt="image" src="https://github.com/user-attachments/assets/7fa0c842-e457-458c-bc8e-5badce6b968b" />

5. POST /add-job Add Job
<img width="1754" height="853" alt="image" src="https://github.com/user-attachments/assets/04d644f5-5845-4c1e-8b53-7f1be178174a" />


