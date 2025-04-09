# prowlercli/client.py
import requests
from prowlercli.config import load_token, load_base_url


# Wrapper for authenticated API requests
class APIClient:
    def __init__(self):
        self.token = load_token()  # Load JWT from
        self.base_url = load_base_url()  # Load API base URL from config

    def get(self, path, params=None):
        # Add authorization and content headers
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.api+json",
            'Content-Type': 'application/vnd.api+json'
        }
        # Make GET request
        response = requests.get(f"{self.base_url}{path}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def patch(self, path, json=None):
        # Add authorization and content headers
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.api+json",
            'Content-Type': 'application/vnd.api+json'
        }
        # Make PATCH request
        response = requests.patch(f"{self.base_url}{path}", headers=headers, json=json)
        response.raise_for_status()
        return response.json() if response.content else None