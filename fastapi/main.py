import os

from fastapi import FastAPI, Depends
import requests
import google.auth
from google.auth.transport.requests import Request
from google.auth import impersonated_credentials
from generate_token import get_oidc_token
from fastapi import FastAPI, Request
import requests
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


app = FastAPI()
security = HTTPBearer()

# Environment variables
API_URL = os.getenv("API_URL", "https://toolbox-service-99546327658.us-central1.run.app/api/tool")

AGENT_API_URL = os.getenv("AGENT_API_URL", "https://jobs-agent-99546327658.us-central1.run.app")

@app.post("/generate-token")
def generate_token(payload: dict):
    """
    Generates an impersonated identity token
    """
    if(payload.get("client_id") == None or payload.get("client_id") != os.getenv("AUDIENCE", "jobs-agent")):
        return {"error": "Invalid or missing client_id in payload"}

    token = get_oidc_token()
    return {"token": token}

@app.post("/search-jobs")
def search_jobs(payload: dict, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
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
def search_jobs_by_description(payload: dict, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
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

@app.post("/add-job")
def add_job(payload: dict, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Forwards incoming request headers + payload to Cloud Run
    """

    # Copy incoming headers
    incoming_headers = dict(request.headers)

    # Remove headers that should NOT be forwarded
    incoming_headers.pop("host", None)
    incoming_headers.pop("content-length", None)

    response = requests.post(
        API_URL + "/add-job/invoke",
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

@app.get("/get-agent-sessions")
def get_agent_sessions(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Forwards incoming request headers + payload to Cloud Run
    """

    # Copy incoming headers
    incoming_headers = dict(request.headers)

    # Remove headers that should NOT be forwarded
    incoming_headers.pop("host", None)
    incoming_headers.pop("content-length", None)

    response = requests.get(
        AGENT_API_URL + "/apps/jobs_agent/users/user/sessions",
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

@app.post("/create-agent-session")
def create_agent_session(payload: dict, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Forwards incoming request headers + payload to Cloud Run
    """

    # Copy incoming headers
    incoming_headers = dict(request.headers)

    # Remove headers that should NOT be forwarded
    incoming_headers.pop("host", None)
    incoming_headers.pop("content-length", None)

    response = requests.post(
        AGENT_API_URL + "/apps/jobs_agent/users/user/sessions",
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

def extract_response(response_json):

    final_text = None
    function_name = None

    for item in response_json:

        content = item.get("content", {})
        parts = content.get("parts", [])

        for part in parts:

            # Extract tool/function name
            if "functionCall" in part:
                function_name = part["functionCall"].get("name")

            # Extract final model text
            if "text" in part:
                final_text = part["text"]

    return {
        "tool_name": function_name,
        "message": final_text
    }

@app.post("/run-agent")
def run_agent(payload: dict, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Forwards incoming request headers + payload to Cloud Run
    """

    # Copy incoming headers
    incoming_headers = dict(request.headers)

    # Remove headers that should NOT be forwarded
    incoming_headers.pop("host", None)
    incoming_headers.pop("content-length", None)

    response = requests.post(
        AGENT_API_URL + "/run",
        json=payload,
        headers=incoming_headers
    )

    response_json = response.json()
    return {
        "status_code": response.status_code,
        "response": extract_response(response_json)
    }
