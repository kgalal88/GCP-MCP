#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Starting full setup..."

###############################################################################
# 📄 Generate README.md
###############################################################################

cat << 'EOF' > README.md

# FastAPI Cloud Run Job Proxy 🚀

A FastAPI-based service deployed on Google Cloud Run for secure service-to-service communication.

---

## 📌 Features

- FastAPI + Uvicorn
- Dockerized deployment
- Cloud Run multi-service architecture
- IAM-secured communication
- Toolbox + Jobs Agent integration
- Vertex AI support

---

## 🧠 Architecture

FastAPI → Toolbox Service → Jobs Agent → Vertex AI → External APIs

EOF

echo "📄 README.md generated"

###############################################################################
# ⚙️ Config
###############################################################################

cd agent/

: "${REGION:=us-central1}"
: "${GOOGLE_CLOUD_PROJECT:?GOOGLE_CLOUD_PROJECT not set}"

###############################################################################
# ☁️ Deploy Toolbox Service
###############################################################################

echo "☁️ Deploying toolbox-service..."

gcloud run deploy toolbox-service \
  --source deploy-toolbox/ \
  --region "$REGION" \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --set-env-vars "DB_PASSWORD=$DB_PASSWORD,DB_INSTANCE=$DB_INSTANCE,DB_NAME=$DB_NAME,GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,REGION=$REGION,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION" \
  --allow-unauthenticated \
  --quiet > ../logs_deploy_toolbox.log 2>&1 &

###############################################################################
# ⏳ Fetch Toolbox URL
###############################################################################

echo "⏳ Waiting for toolbox URL..."

sleep 15

TOOLBOX_URL=$(gcloud run services describe toolbox-service \
  --region "$REGION" \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --format='value(status.url)')

echo "✅ Toolbox URL: $TOOLBOX_URL"

###############################################################################
# 🤖 Deploy Jobs Agent
###############################################################################

echo "🤖 Deploying jobs-agent..."

gcloud run deploy jobs-agent \
  --source . \
  --region "$REGION" \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --set-env-vars "TOOLBOX_URL=$TOOLBOX_URL,GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_GENAI_USE_VERTEXAI=TRUE"

###############################################################################
# 🌐 Fetch Agent URL
###############################################################################

AGENT_URL=$(gcloud run services describe jobs-agent \
  --region "$REGION" \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --format='value(status.url)')

echo "✅ Agent URL: $AGENT_URL"

###############################################################################
# 🔐 IAM CONFIG
###############################################################################

echo "🔐 Updating IAM..."

gcloud run services update jobs-agent \
  --add-custom-audiences=jobs-agent \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --region "$REGION"

###############################################################################
# 🔑 Identity Token Example
###############################################################################

echo "🔑 Example identity token command:"

echo "gcloud auth print-identity-token \
  --impersonate-service-account way-back-home-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com \
  --audiences='jobs-agent' \
  --project '$GOOGLE_CLOUD_PROJECT'"

###############################################################################
# 🔎 Debug
###############################################################################

echo "🔎 Debug commands:"

echo "gcloud run services describe jobs-agent --region $REGION --project $GOOGLE_CLOUD_PROJECT"
echo "gcloud run services describe toolbox-service --region $REGION --project $GOOGLE_CLOUD_PROJECT"

echo "🎉 Setup completed successfully!"