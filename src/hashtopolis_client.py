# src/hashtopolis_client.py
import requests
import os

class HashtopolisClient:
    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url.rstrip("/") if base_url else None
        self.api_key = api_key

    def create_task(self, payload):
        # Example: implement per your server's API; this is a placeholder
        url = f"{self.base_url}/tasks/create"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        r = requests.post(url, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()
