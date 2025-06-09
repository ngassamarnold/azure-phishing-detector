import requests
import hashlib
import hmac
import base64
import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
    x_headers = 'x-ms-date:' + date
    string_to_hash = method + '\n' + str(content_length) + '\n' + content_type + '\n' + x_headers + '\n' + resource
    bytes_to_hash = bytes(string_to_hash, encoding='utf-8')
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
    authorization = f"SharedKey {customer_id}:{encoded_hash}"
    return authorization

def send_email_to_sentinel(email_data):
    customer_id = os.getenv("SENTINEL_WORKSPACE_ID")
    shared_key = os.getenv("SENTINEL_SHARED_KEY")
    log_type = "PhishingEmail_CL"  # ou autre nom personnalisé
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    body = json.dumps(email_data)
    content_length = len(body)
    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)
    uri = f'https://{customer_id}.ods.opinsights.azure.com{resource}?api-version=2016-04-01'
    headers = {
        'Content-Type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }

    response = requests.post(uri, data=body, headers=headers)
    if response.status_code >= 200 and response.status_code <= 299:
        print("✅ Données envoyées à Microsoft Sentinel.")
    else:
        print(f"❌ Échec de l'envoi : {response.status_code} {response.text}")
