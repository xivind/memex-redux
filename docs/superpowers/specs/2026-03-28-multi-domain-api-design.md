# Multi-Domain API Support

**Date:** 2026-03-28
**Status:** Approved

## Problem

The current codebase hardcodes a single external API domain (`velo_supervisor_url`) in
`config.json`, the `Config` model, and the status page. Adding a second domain (e.g. Yr)
requires touching multiple files and adding more hardcoded special-cases. This design
generalises external API support to N named domains.

---

## Design

### Config (`config.json`)

Replace the top-level `velo_supervisor_url` string with an `api_domains` dict. Keys are
display labels (shown as-is in the UI); values are base URLs.

```json
{
  "mariadb_host": "...",
  "mariadb_database": "...",
  "mariadb_user": "...",
  "mariadb_password": "...",
  "mariadb_port": 3306,
  "api_domains": {
    "Velo Supervisor 2000": "http://velo-supervisor:8003",
    "Yr": "http://yr-api:8004"
  },
  "server_port": 8002
}
```

`api_domains` defaults to `{}` — no domains configured is valid.

### Data model (`core/db_connection.py`)

`Config` drops `velo_supervisor_url: str = ""` and gains:

```python
api_domains: dict[str, str] = {}
```

### Health checks (`core/server.py`)

`api_status()` replaces the one-off `velo_connected` check with a loop:

```python
domain_status = {}
for name, url in config.api_domains.items():
    try:
        r = _requests.get(url, timeout=3)
        domain_status[name] = r.ok
    except Exception:
        domain_status[name] = False
```

The response field changes from `velo_connected: bool | None` to
`api_domains: dict[str, bool]` (empty dict when no domains are configured).

Connectivity is determined by probing the base URL directly (no `/health` path assumed).
A 200-range response means connected; any exception or non-OK status means disconnected.

### Frontend (`templates/status.html` + `static/app.js`)

The hardcoded `velo-label` and `stat-velo` elements are removed. The connections card
body keeps a static Database row and an empty `#connections-grid` div that JS populates:

```html
<div class="stat-grid" id="connections-grid">
  <span class="stat-label">Database</span>
  <span class="stat-value" id="stat-db">—</span>
</div>
```

`renderStatus()` in `app.js` replaces the `velo_connected` special-case with a loop
that appends one label+value pair per domain on each refresh:

```js
document.querySelectorAll(".api-domain-row").forEach(el => el.remove());

const grid = document.getElementById("connections-grid");
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

### Tool plugins (e.g. `tools/vs2000.py`)

Each plugin instantiates `HttpConnector` using its domain's base URL from config:

```python
from core.db_connection import config
from core.http_connector import HttpConnector

connector = HttpConnector(config.api_domains["Velo Supervisor 2000"])

@mcp.tool(description="...")
def get_bikes() -> list[dict]:
    return connector.get("/api/bikes")
```

Multiple tools per domain call different paths on the same `HttpConnector` instance.
One domain entry in `config.json` supports any number of tool endpoints.

---

## Files changed

| File | Change |
|---|---|
| `config.json` | Replace `velo_supervisor_url` with `api_domains` dict |
| `core/db_connection.py` | Replace `velo_supervisor_url` field with `api_domains: dict[str, str] = {}` |
| `core/server.py` | Replace one-off velo health check with domain loop; update response shape |
| `templates/status.html` | Remove hardcoded velo elements; add `id="connections-grid"` to stat-grid |
| `static/app.js` | Replace `velo_connected` rendering with dynamic domain loop |
| `tools/vs2000.py` | Update to use `config.api_domains["Velo Supervisor 2000"]` |

---

## Out of scope

- Per-domain timeouts (all use 3 s)
- Disabling individual domains without removing them from config
- Authentication for external APIs
