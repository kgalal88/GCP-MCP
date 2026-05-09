python3 -m uvicorn main:app --reload  

docker build -t fastapi-job-proxy .

docker run -p 8080:8080 `
-v "$env:APPDATA\gcloud\application_default_credentials.json:/tmp/adc.json" `
-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/adc.json `
fastapi-job-proxy

gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable iamcredentials.googleapis.com

gcloud iam service-accounts create fastapi-job-proxy --project=waybackhome-qxln4tprji8q9zklz8

gcloud iam service-accounts add-iam-policy-binding `
way-back-home-sa@waybackhome-qxln4tprji8q9zklz8.iam.gserviceaccount.com `
--member="serviceAccount:fastapi-job-proxy@waybackhome-qxln4tprji8q9zklz8.iam.gserviceaccount.com" `
--role="roles/iam.serviceAccountTokenCreator" `
--project=waybackhome-qxln4tprji8q9zklz8

gcloud run deploy fastapi-job-proxy `
--source . `
--region us-central1 `
--allow-unauthenticated `
--service-account fastapi-job-proxy@waybackhome-qxln4tprji8q9zklz8.iam.gserviceaccount.com `
--project=waybackhome-qxln4tprji8q9zklz8

gcloud run services update toolbox-service `
--ingress all `
--region=us-central1 `
--project=waybackhome-qxln4tprji8q9zklz8

gcloud run services list --project=waybackhome-qxln4tprji8q9zklz8