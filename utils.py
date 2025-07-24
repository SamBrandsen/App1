import json
import os

SIGNUPS_FILE = "signups.json"

def load_signups():
    if os.path.exists(SIGNUPS_FILE):
        with open(SIGNUPS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_signups(signups):
    with open(SIGNUPS_FILE, "w") as f:
        json.dump(signups, f, indent=2)
