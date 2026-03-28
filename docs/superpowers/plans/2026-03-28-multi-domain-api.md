# Multi-Domain API Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the single hardcoded `velo_supervisor_url` with a generic `api_domains` dict that supports N named external API domains, each with one status indicator on the status page.

**Architecture:** `config.json` gains an `api_domains: {name: base_url}` dict. The `Config` pydantic model mirrors this. `server.py` loops over configured domains and probes each base URL for connectivity. The frontend renders one status row per domain dynamically from the API response.

**Tech Stack:** FastAPI, Pydantic v2, requests, Bootstrap 5 + vanilla JS

---

## File Map

| File | Change |
|---|---|
| `config.json` | Replace `velo_supervisor_url` with `api_domains: {}` |
| `core/db_connection.py` | Replace `velo_supervisor_url: str = ""` with `api_domains: dict[str, str] = {}` |
| `core/server.py` | Replace one-off velo check with domain loop; `velo_connected` → `api_domains` in response |
| `templates/status.html` | Remove hardcoded velo elements; add `id="connections-grid"` to stat-grid div |
| `static/app.js` | Replace `velo_connected` special-case with dynamic domain loop |
| `tools/vs2000.py` | Update config reference from `velo_supervisor_url` to `api_domains` key |
| `tests/test_db_connection.py` | Update `_make_config()` helper; add test for `api_domains` field |
| `tests/test_server.py` | Update shape test; add domain connectivity tests |

---

## Task 1: Update Config model and config.json

**Files:**
- Modify: `core/db_connection.py`
- Modify: `config.json`
- Test: `tests/test_db_connection.py`

- [ ] **Step 1: Write a failing test for `api_domains`**

Add to `tests/test_db_connection.py`:

```python
def test_config_loads_api_domains():
    cfg_json = json.dumps({
        "mariadb_host": "testhost",
        "mariadb_database": "testdb",
        "mariadb_user": "user",
        "mariadb_password": "pass",
        "mariadb_port": 3306,
        "api_domains": {
            "Velo Supervisor 2000": "http://vs:8003",
            "Yr": "http://yr:8004",
        },
        "server_port": 8002,
    })
    with patch("builtins.open", mock_open(read_data=cfg_json)):
        from importlib import reload
        import core.db_connection as db_mod
        reload(db_mod)
        assert db_mod.config.api_domains == {
            "Velo Supervisor 2000": "http://vs:8003",
            "Yr": "http://yr:8004",
        }
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
python3 -m pytest tests/test_db_connection.py::test_config_loads_api_domains -v
```

Expected: FAIL — `Config` has no `api_domains` field.

- [ ] **Step 3: Update `_make_config()` in `tests/test_db_connection.py`**

Replace the `_make_config` helper so all tests use the new schema:

```python
def _make_config(**overrides):
    base = {
        "mariadb_host": "testhost",
        "mariadb_database": "testdb",
        "mariadb_user": "user",
        "mariadb_password": "pass",
        "mariadb_port": 3306,
        "api_domains": {},
        "server_port": 8002,
    }
    base.update(overrides)
    return json.dumps(base)
```

- [ ] **Step 4: Replace the `velo_supervisor_url` field in `core/db_connection.py`**

In the `Config` class, replace:

```python
velo_supervisor_url: str = ""
```

with:

```python
api_domains: dict[str, str] = {}
```

- [ ] **Step 5: Update `config.json`**

Replace:

```json
"velo_supervisor_url": "http://velo-supervisor:8003",
```

with:

```json
"api_domains": {
  "Velo Supervisor 2000": "http://velo-supervisor:8003"
},
```

- [ ] **Step 6: Run all db_connection tests**

```bash
python3 -m pytest tests/test_db_connection.py -v
```

Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add core/db_connection.py config.json tests/test_db_connection.py
git commit -m "feat: replace velo_supervisor_url with api_domains dict in Config"
```

---

## Task 2: Update server health check endpoint

**Files:**
- Modify: `core/server.py`
- Test: `tests/test_server.py`

- [ ] **Step 1: Write failing tests**

Replace the existing `test_api_status_shape` and add two new domain connectivity tests in `tests/test_server.py`. The final content of the file (after the existing `client` fixture and `test_health_returns_ok`) should be:

```python
# tests/test_server.py
from unittest.mock import patch, MagicMock
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
    assert "api_domains" in data
    assert "velo_connected" not in data
    assert isinstance(data["api_domains"], dict)
    assert isinstance(data["tools"], list)
    assert isinstance(data["recent_calls"], list)


def test_api_status_db_connected_true(client):
    response = client.get("/api/status")
    assert response.json()["db_connected"] is True


def test_api_status_db_connected_false():
    with patch("core.db_connection.check_db_connection", return_value=False):
        from fastapi.testclient import TestClient
        import importlib, sys
        for key in list(sys.modules.keys()):
            if "server" in key and "core" in key:
                del sys.modules[key]
        from core.server import app
        with TestClient(app) as c:
            response = c.get("/api/status")
            assert response.json()["db_connected"] is False


def test_api_status_domain_connected():
    mock_response = MagicMock()
    mock_response.ok = True
    from core.server import app
    with patch("core.server._requests.get", return_value=mock_response), \
         patch("core.server.config") as mock_config, \
         patch("core.server.check_db_connection", return_value=True):
        mock_config.api_domains = {"Test API": "http://test:9000"}
        from fastapi.testclient import TestClient
        with TestClient(app) as c:
            response = c.get("/api/status")
            data = response.json()
            assert data["api_domains"] == {"Test API": True}


def test_api_status_domain_disconnected():
    from core.server import app
    with patch("core.server._requests.get", side_effect=Exception("connection refused")), \
         patch("core.server.config") as mock_config, \
         patch("core.server.check_db_connection", return_value=True):
        mock_config.api_domains = {"Test API": "http://test:9000"}
        from fastapi.testclient import TestClient
        with TestClient(app) as c:
            response = c.get("/api/status")
            data = response.json()
            assert data["api_domains"] == {"Test API": False}


def test_status_page_returns_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
```

- [ ] **Step 2: Run tests to verify the new ones fail**

```bash
python3 -m pytest tests/test_server.py::test_api_status_shape tests/test_server.py::test_api_status_domain_connected tests/test_server.py::test_api_status_domain_disconnected -v
```

Expected: `test_api_status_shape` FAIL (`velo_connected` still in response, `api_domains` missing); connectivity tests FAIL.

- [ ] **Step 3: Update `api_status()` in `core/server.py`**

Replace the entire `api_status` function:

```python
@app.get("/api/status")
def api_status():
    domain_status = {}
    for name, url in config.api_domains.items():
        try:
            r = _requests.get(url, timeout=3)
            domain_status[name] = r.ok
        except Exception:
            domain_status[name] = False

    return {
        "uptime_seconds": int(time.monotonic() - _start_time),
        "start_time": _start_dt,
        "db_connected": check_db_connection(),
        "api_domains": domain_status,
        "total_calls": call_log.total_count,
        "tools": _registered_tools,
        "recent_calls": call_log.get_all(),
    }
```

Also remove the unused `config` import alias — the existing import line is:

```python
from core.db_connection import check_db_connection, config
```

This stays as-is (both are still used).

- [ ] **Step 4: Run all server tests**

```bash
python3 -m pytest tests/test_server.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add core/server.py tests/test_server.py
git commit -m "feat: replace velo health check with generic api_domains loop in server"
```

---

## Task 3: Update frontend

**Files:**
- Modify: `templates/status.html`
- Modify: `static/app.js`

No automated tests for frontend JS. Run the full test suite at the end to confirm no regressions.

- [ ] **Step 1: Update `templates/status.html`**

In the Connections card body, replace:

```html
<div class="card-body">
  <div class="stat-grid">
    <span class="stat-label">Database</span>
    <span class="stat-value" id="stat-db">—</span>
    <span class="stat-label" id="velo-label" style="display:none">External API</span>
    <span class="stat-value" id="stat-velo" style="display:none">—</span>
  </div>
</div>
```

with:

```html
<div class="card-body">
  <div class="stat-grid" id="connections-grid">
    <span class="stat-label">Database</span>
    <span class="stat-value" id="stat-db">—</span>
  </div>
</div>
```

- [ ] **Step 2: Update `renderStatus()` in `static/app.js`**

Replace this block in `renderStatus`:

```js
const veloLabel = document.getElementById("velo-label");
const veloVal   = document.getElementById("stat-velo");
if (data.velo_connected !== null && data.velo_connected !== undefined) {
  veloLabel.style.display = "";
  veloVal.style.display   = "";
  veloVal.innerHTML = statusBadge(data.velo_connected, "Connected", "Disconnected");
}
```

with:

```js
const grid = document.getElementById("connections-grid");
document.querySelectorAll(".api-domain-row").forEach(el => el.remove());
for (const [name, connected] of Object.entries(data.api_domains)) {
  const label = document.createElement("span");
  label.className = "stat-label api-domain-row";
  label.textContent = name;

  const value = document.createElement("span");
  value.className = "stat-value api-domain-row";
  value.innerHTML = statusBadge(connected, "Connected", "Disconnected");

  grid.append(label, value);
}
```

- [ ] **Step 3: Run full test suite to confirm no regressions**

```bash
python3 -m pytest -v
```

Expected: all PASS (frontend changes don't affect Python tests).

- [ ] **Step 4: Commit**

```bash
git add templates/status.html static/app.js
git commit -m "feat: render api_domains dynamically on status page"
```

---

## Task 4: Update tools/vs2000.py

**Files:**
- Modify: `tools/vs2000.py`
- Test: `tests/test_vs2000.py`

- [ ] **Step 1: Update `tools/vs2000.py` to reference the new config key**

Replace the entire file:

```python
# tools/vs2000.py — Velo Supervisor 2000 tools (stubbed, API shape TBD)
# Unblock by: confirming velo-supervisor-2000 API endpoints and response schema

from core.db_connection import config
from core.http_connector import HttpConnector
from core.tool_registry import mcp


@mcp.tool(description="Velo Supervisor 2000 API: bike fleet status, component wear, and maintenance schedule")
def get_vs2000() -> list[dict]:
    # TODO Phase B: implement once velo-supervisor-2000 API shape is confirmed
    # Usage pattern once unblocked:
    #   connector = HttpConnector(config.api_domains["Velo Supervisor 2000"])
    #   return connector.get("/api/bikes")
    return []
```

- [ ] **Step 2: Run vs2000 tests**

```bash
python3 -m pytest tests/test_vs2000.py -v
```

Expected: all PASS.

- [ ] **Step 3: Run full test suite**

```bash
python3 -m pytest -v
```

Expected: all PASS.

- [ ] **Step 4: Commit**

```bash
git add tools/vs2000.py
git commit -m "chore: update vs2000 to reference api_domains config pattern"
```
