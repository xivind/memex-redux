# CLAUDE.md — memex-redux

> Personal data gateway MCP server for Claude Code.
> Exposes personal and home automation data via the Model Context Protocol (MCP).

---

## Project Overview

memex-redux is a **generic, extensible MCP server skeleton**. The core infrastructure
is data-source agnostic. Data sources are added as tool plugins in `tools/`.

The reference implementation ships with plugins for finance, health, climate, and bike data.

---

## Repository Structure

```
memex-redux/
├── core/
│   ├── server.py           # FastAPI app, MCP mount, lifespan
│   ├── tool_registry.py    # @tool decorator, auto-discovery of plugins
│   ├── db_connection.py    # Peewee initialisation and connection management
│   ├── http_connector.py   # Base class for HTTP-based data sources
│   └── call_log.py         # In-memory ring buffer (last 50 tool calls)
│
├── tools/                  # User plugins — one file per data domain
│   ├── README.md
│   ├── finance.py
│   ├── health.py
│   ├── climate.py
│   └── vs2000.py
│
├── models.py               # All Peewee model definitions
├── templates/
│   └── status.html         # Bootstrap 5 status UI
├── static/
│   ├── app.js              # All frontend JavaScript
│   └── app.css             # All frontend CSS
│
├── config.json             # DB credentials and API endpoint URLs
├── tools_config.yaml       # YAML-defined simple single-table tools
├── Dockerfile
├── create-container.sh
├── requirements.txt
└── uvicorn_log_config.ini
```

---

## Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI |
| ASGI server | Uvicorn |
| MCP SDK | `mcp` (official Anthropic Python SDK) — `FastMCP` |
| Database ORM | Peewee |
| Database driver | PyMySQL |
| HTTP client | requests |
| Config validation | pydantic |
| Frontend | Bootstrap 5 + vanilla JS |

---

## Architecture

Claude Code connects over **Streamable HTTP** (not SSE — deprecated as of 2025-03-26):

```
Claude Code
    │  Streamable HTTP
    ▼
FastAPI app  (port 8002)
    /mcp      → MCP protocol endpoint
    /         → Status web UI
    /health   → JSON health check (Docker HEALTHCHECK)
```

The MCP app is mounted onto the FastAPI app:

```python
mcp = FastMCP("memex-mcp", stateless_http=True)
app = FastAPI(lifespan=lambda a: mcp.session_manager.run())
app.mount("/mcp", mcp.streamable_http_app())
```

---

## Tool Plugins

### Auto-discovery

All `tools/*.py` files are auto-discovered and imported at startup by `core/tool_registry.py`.
No registration step is needed — drop a file in `tools/` and restart.

### Decorator

```python
from core.tool_registry import mcp

@mcp.tool(description="Natural language description Claude reads to pick this tool")
def get_my_data(days: int = 30) -> list[dict]:
    ...
```

### Two access patterns

**Database (Peewee → MariaDB):**
```python
@mcp.tool(description="Sleep quality and recovery data")
def get_sleep(days: int = 14) -> list[dict]:
    # Multi-table joins live here, invisible to Claude
    ...
```

**HTTP (requests → external API):**
```python
@mcp.tool(description="Bike fleet status and maintenance schedule")
def get_bikes() -> list[dict]:
    return http_connector.get("/api/bikes")
```

### YAML tools (no Python needed)

Simple single-table tools can be declared in `tools_config.yaml` instead of Python:

```yaml
tools:
  - name: get_weather
    description: "Current and recent outdoor weather"
    type: database
    table: yr_weather
    fields: [record_time, temperature, wind_speed, precipitation]
    default_days: 7
```

### Tool design principle

Tools represent **natural questions**, not database tables. The `description` is what
Claude reads to decide which tool to call. Write it as a question a human would ask.

---

## Frontend

- **Bootstrap 5** for all layout and components.
- **Vanilla JS only** — no frameworks, no build step.
- All JavaScript goes in `static/app.js`. No inline `<script>` tags.
- All CSS goes in `static/app.css`. No inline `<style>` tags.
- Templates live in `templates/`. Served by FastAPI's Jinja2 integration.
- The status page at `/` auto-refreshes every 30 seconds.

---

## Logging

All logging is handled by **uvicorn** via `uvicorn_log_config.ini`. Do not add a
separate Python `logging` configuration. Use `print()` only for temporary debugging
and remove before committing.

Log format:
```
%(asctime)s - %(levelname)s - %(message)s
```

What is logged:
- Server lifecycle (startup, shutdown, DB connection)
- Tool invocations (tool name, params, duration, row count or error)
- HTTP connector calls (URL, status code, latency)
- DB errors

---

## Configuration

`config.json` — all deployment-specific values. Never hardcode credentials.

```json
{
  "mariadb_host": "home-assistant",
  "mariadb_database": "MASTERDB",
  "mariadb_user": "mcp_readonly",
  "mariadb_password": "...",
  "mariadb_port": 3306,
  "velo_supervisor_url": "http://velo-supervisor:8003",
  "server_port": 8002
}
```

The MariaDB user must be a **dedicated read-only account** (`SELECT` only).

---

## Docker

```dockerfile
CMD ["uvicorn", "core.server:app", "--host", "0.0.0.0", "--port", "8002",
     "--log-config", "uvicorn_log_config.ini"]
```

Health check polls `/health`:
```dockerfile
HEALTHCHECK --interval=10m --timeout=10s \
  CMD curl -f http://localhost:8002/health || exit 1
```

---

## Connecting Claude Code

```bash
claude mcp add --transport http --scope user memex-redux http://<host>:8002/mcp
```

`--scope user` makes the server available across all Claude Code projects.

---

## Phase 1 Constraints

- All tools are **read-only**. No writes to the database or external APIs.
- The MariaDB user has `SELECT` privileges only.
- No authentication (home network assumption).
- No external log aggregation required — stdout only.
