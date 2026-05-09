import subprocess

def get_token_via_gcloud():
    target_sa = "way-back-home-sa@waybackhome-qxln4tprji8q9zklz8.iam.gserviceaccount.com"
    cmd = [
        "gcloud", "auth", "print-identity-token",
        f"--impersonate-service-account={target_sa}",
        "--audiences=jobs-agent"
    ]
    # shell=True helps find gcloud on Windows paths
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        raise Exception(f"Gcloud error: {result.stderr}")
    return result.stdout.strip()

if __name__ == "__main__":
    print(f"Bearer {get_token_via_gcloud()}")