
---

# 🐧 Bash Script (Linux / Mac)

Save as: `generate-readme.sh`

```bash
#!/bin/bash

cat << 'EOF' > README.md

# FastAPI Cloud Run Job Proxy 🚀

A FastAPI-based service deployed on Google Cloud Run for secure service-to-service communication.

---

## 📌 Features

- FastAPI + Uvicorn
- Dockerized deployment
- Google Cloud Run ready
- IAM-secured service-to-service calls
- Service Account authentication

---

## 🚀 Local Run

python3 -m uvicorn main:app --reload

Open:
http://127.0.0.1:8000/docs

---

## 🐳 Docker

docker build -t fastapi-job-proxy .
docker run -p 8080:8080 fastapi-job-proxy

---

## ☁️ Deploy to Cloud Run

gcloud run deploy fastapi-job-proxy \
--source . \
--region us-central1 \
--allow-unauthenticated \
--service-account fastapi-job-proxy@waybackhome-qxln4tprji8q9zklz8.iam.gserviceaccount.com

---

## 🔐 IAM Setup

gcloud run services add-iam-policy-binding toolbox-service \
--member="serviceAccount:fastapi-job-proxy@waybackhome-qxln4tprji8q9zklz8.iam.gserviceaccount.com" \
--role="roles/run.invoker" \
--region=us-central1

---

## 🧠 Architecture

FastAPI Cloud Run → (Auth Token) → Toolbox Cloud Run Service

EOF

echo "README.md generated successfully 🚀"