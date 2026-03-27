# core/http_connector.py — Base class for HTTP-based data sources
import time
import requests


class HttpConnector:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get(self, path: str, **kwargs) -> dict | list:
        url = f"{self.base_url}{path}"
        start = time.monotonic()
        response = requests.get(url, **kwargs)
        duration_ms = int((time.monotonic() - start) * 1000)
        response.raise_for_status()
        return response.json()
