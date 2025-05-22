import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    tenant_id = os.getenv("AZURE_TENANT_ID")

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scope = ["https://graph.microsoft.com/.default"]

    app = ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority
    )

    result = app.acquire_token_for_client(scopes=scope)
    return result["access_token"]

def get_latest_emails(user_email, token, max_results=10):
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/mailFolders/inbox/messages?$top={max_results}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        raise Exception(f"Graph API error: {response.status_code} - {response.text}")
