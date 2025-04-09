# prowlercli/config.py
import os
import json

# Define where the config is saved
CONFIG_PATH = os.path.expanduser("~/.prowlercli/config.json")

# Save access token and API base URL to config file
def save_config(token, base_url):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)  # Ensure directory exists
    with open(CONFIG_PATH, 'w') as f:
        json.dump({"access_token": token, "base_url": base_url}, f)

# Load base URL from config file
def load_base_url():
    if not os.path.exists(CONFIG_PATH):
        raise RuntimeError("Not authenticated. Run `prowler login` first.")
    with open(CONFIG_PATH) as f:
        return json.load(f).get("base_url")
    
# Load access token from config file
def load_token():
    if not os.path.exists(CONFIG_PATH):
        raise RuntimeError("Not authenticated. Run `prowler login` first.")
    with open(CONFIG_PATH) as f:
        return json.load(f).get("access_token")