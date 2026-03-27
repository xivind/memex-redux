# tests/test_server.py
from unittest.mock import patch
import pytest


@pytest.fixture
def client():
    with patch("core.db_connection.check_db_connection", return_value=True):
        from fastapi.testclient import TestClient
        from core.server import app
        with TestClient(app) as c:
            yield c


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert isinstance(data["uptime_seconds"], (int, float))


def test_api_status_shape(client):
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "uptime_seconds" in data
    assert "start_time" in data
    assert "db_connected" in data
    assert isinstance(data["tools"], list)
    assert isinstance(data["recent_calls"], list)


def test_api_status_db_connected_true(client):
    response = client.get("/api/status")
    assert response.json()["db_connected"] is True


def test_api_status_db_connected_false():
    with patch("core.db_connection.check_db_connection", return_value=False):
        from fastapi.testclient import TestClient
        import importlib, sys
        # Reload server to pick up fresh patch
        for key in list(sys.modules.keys()):
            if "server" in key and "core" in key:
                del sys.modules[key]
        from core.server import app
        with TestClient(app) as c:
            response = c.get("/api/status")
            assert response.json()["db_connected"] is False


def test_status_page_returns_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
