# core/http_connector.py — Base class for HTTP-based data sources
import requests


class HttpConnector:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get(self, path: str, **kwargs) -> dict | list:
        url = f"{self.base_url}{path}"
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        return response.json()
