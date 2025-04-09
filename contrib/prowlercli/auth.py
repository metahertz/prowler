# prowlercli/auth.py
import os
import json
import requests
from getpass import getpass
from prowlercli.config import CONFIG_PATH, save_config

# Prompt the user for credentials, API URL, log in, and store the config
def login():
    base_url = input("API Base URL (e.g. https://api.prowler.com): ").strip()
    email = input("Email: ")
    password = getpass("Password: ")  # Hide input for password

    # Prepare payload as per API spec
    payload = {
        "data": {
            "type": "tokens",
            "attributes": {
                "email": email,
                "password": password
            }
        }
    }

    headers = {
        'Content-Type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json'
    }

    # POST request to the /tokens endpoint
    response = requests.post(f"{base_url}/api/v1/tokens", json=payload, headers=headers)
    response.raise_for_status()  # Raise exception on error

    # Extract access token from response
    token = response.json()['data']['attributes']['access']
    save_config(token, base_url)  # Save token and base URL locally
    print("✅ Login successful.")