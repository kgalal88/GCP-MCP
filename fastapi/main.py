import os

from fastapi import FastAPI
import requests
import google.auth
from google.auth.transport.requests import Request
from google.auth import impersonated_credentials
from generate_token import get_oidc_token
from fastapi import FastAPI, Request
import requests

app = FastAPI()

# Environment variables
AUDIENCE = os.getenv("API_URL")

# AUDIENCE = "https://toolbox-service-99546327658.us-central1.run.app"
API_URL = f"{AUDIENCE}/api/tool"

@app.post("/generate-token")
def generate_token(payload: dict):
    """
    Generates an impersonated identity token
    """
    token = get_oidc_token()
    return {"token": token}

@app.post("/search-jobs")
def search_jobs(payload: dict, request: Request):
    """
    Forwards incoming request headers + payload to Cloud Run
    """

    # Copy incoming headers
    incoming_headers = dict(request.headers)

    # Remove headers that should NOT be forwarded
    incoming_headers.pop("host", None)
    incoming_headers.pop("content-length", None)

    response = requests.post(
        API_URL + "/search-jobs/invoke",
        json=payload,
        headers=incoming_headers
    )

    return {
        "status_code": response.status_code,
        "response": (
            response.json()
            if "application/json" in response.headers.get("content-type", "")
            else response.text
        )
    }

@app.post("/search-jobs-by-description")
def search_jobs_by_description(payload: dict, request: Request):
    """
    Forwards incoming request headers + payload to Cloud Run
    """

    # Copy incoming headers
    incoming_headers = dict(request.headers)

    # Remove headers that should NOT be forwarded
    incoming_headers.pop("host", None)
    incoming_headers.pop("content-length", None)

    response = requests.post(
        API_URL + "/search-jobs-by-description/invoke",
        json=payload,
        headers=incoming_headers
    )

    return {
        "status_code": response.status_code,
        "response": (
            response.json()
            if "application/json" in response.headers.get("content-type", "")
            else response.text
        )
    }
