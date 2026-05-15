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
Toolbox Service (Cloud Run)
      ↓
Vertex AI / External APIs
```

---

## 🚀 Deployment Commands

### Deploy FastApi Proxy Service

```bash
gcloud run deploy fastapi-job-proxy --source . --region us-central1 --project=waybackhome-qxln4tprji8q9zklz8 --allow-unauthenticated --service-account fastapi-job-proxy@waybackhome-qxln4tprji8q9zklz8.iam.gserviceaccount.com
```

### Deploy Toolbox Service

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

### Alternatively, deploy jobs-agent-mcp which is a jobs agent + toolbox containers as a sidecar

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

## 🚀 Deployment Flow

1. Deploy Toolbox service to Cloud Run
2. Retrieve Toolbox service URL
3. Deploy Jobs Agent with Toolbox URL injected
4. Configure IAM permissions
5. Enable secure service-to-service communication

---

## 📌 Notes

- Always use service accounts with least privilege
- Prefer IAM authentication over public endpoints
- Store secrets in Secret Manager (not env vars in production)
