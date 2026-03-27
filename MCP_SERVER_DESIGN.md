# memex-redux — Design Document

> *"As we may think"* — Vannevar Bush, 1945

> **memex-redux** is a personal assistant data gateway for Claude Code, named as a homage to Vannevar Bush's visionary 1945 article in which he imagined the Memex — a device that would store, retrieve and link all of a person's knowledge and experience. We feel this MCP server, giving an AI assistant seamless access to the accumulated data of your daily life, is a direct realisation of that idea.

> Designed to be a reusable open-source skeleton that others can adapt for their own data sources.

---

## Overview

**memex-redux** exposes personal and home automation data to Claude Code via the Model Context Protocol. It is built as a **generic, extensible skeleton** — the core infrastructure is data-source agnostic, and individual data sources are added as tool plugins. The reference implementation ships with plugins for finance, health, climate, and bike data.

The server runs as a Docker container alongside other home automation services and is registered once in Claude Code. From that point on, Claude can query any registered data source naturally in conversation.

---

## Transport

**Streamable HTTP** is used as the MCP transport. SSE (Server-Sent Events) is the older transport and is now deprecated in the MCP specification as of 2025-03-26. All new implementations should use Streamable HTTP.

Claude Code connects with a single command:

```bash
claude mcp add --transport http --scope user homelab http://<your-host>:8002/mcp
```

The `--scope user` flag makes the server available across all Claude Code projects, not just the current one. Replace `<your-host>` with the hostname or IP of the machine running the container.

---

## Key Libraries

### `mcp` — Official MCP Python SDK

Anthropic publishes an official Python SDK for the Model Context Protocol:

```
pip install mcp
```

It includes `mcp.server.fastmcp.FastMCP`, which integrates directly with FastAPI and handles all protocol-level concerns — tool registration, handshake, session management, and Streamable HTTP transport. Tools are defined with a simple decorator:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("homelab-mcp", stateless_http=True)

@mcp.tool(description="Recent transactions from your bank account")
def get_transactions(days: int = 30) -> list[dict]:
    ...
```

The MCP app mounts onto the main FastAPI app at `/mcp`:

```python
from fastapi import FastAPI

app = FastAPI(lifespan=lambda a: mcp.session_manager.run())
app.mount("/mcp", mcp.streamable_http_app())
```

All other FastAPI routes (`/`, `/health`) sit alongside it on the same app instance. No separate process or port is needed.

### Other core dependencies

| Package | Purpose |
|---|---|
| `fastapi` | Web framework — MCP transport + status UI + health endpoint |
| `uvicorn` | ASGI server |
| `peewee` | ORM for all MariaDB data sources |
| `PyMySQL` | MariaDB driver (used by Peewee) |
| `requests` | HTTP connector for external API data sources |
| `pydantic` | Configuration validation |

---

## Architecture

```
Claude Code
    │
    │  Streamable HTTP  (claude mcp add --transport http)
    ▼
┌─────────────────────────────────────────────────────────┐
│                    MCP Server                           │
│             FastAPI · port 8002                         │
│                                                         │
│  /mcp        Streamable HTTP endpoint (MCP protocol)   │
│  /           Status web UI (Bootstrap 5)               │
│  /health     JSON health check (Docker health check)   │
│                                                         │
│  ── Core infrastructure ────────────────────────────   │
│  Tool registry     Discovers and routes tool calls      │
│  Call log          In-memory ring buffer (last 50)      │
│  Connectors        Peewee DB pool · HTTP base class     │
│                                                         │
│  ── Tool plugins (swappable) ───────────────────────   │
│  finance.py        Peewee → MariaDB                     │
│  health.py         Peewee → MariaDB                     │
│  climate.py        Peewee → MariaDB                     │
│  bikes.py          HTTP → velo-supervisor-2000 API      │
└─────────────────────────────────────────────────────────┘
    │                                    │
    ▼                                    ▼
MariaDB (MASTERDB)             velo-supervisor-2000
balance, transactions,         REST API
supersaver, strava,
polar, fitbit,
vindstyrka, yr_weather, nilu
```

---

## Repository Structure

```
memex-redux/
│
├── core/                         # Skeleton — generic, not modified by users
│   ├── server.py                 # FastAPI app, MCP mount, lifespan
│   ├── tool_registry.py          # @tool decorator, auto-discovery of plugins
│   ├── db_connection.py          # Peewee initialisation and connection management
│   ├── http_connector.py         # Base class for HTTP-based data sources
│   └── call_log.py               # In-memory ring buffer for recent tool calls
│
├── tools/                        # User plugins — add your data sources here
│   ├── README.md                 # Instructions for adding new tools
│   ├── finance.py                # Reference: multi-table finance queries
│   ├── health.py                 # Reference: multi-table health queries
│   ├── climate.py                # Reference: climate/sensor queries
│   └── bikes.py                  # Reference: HTTP connector example
│
├── models.py                     # Peewee model definitions (one per deployment)
├── templates/
│   └── status.html               # Bootstrap 5 status web UI
├── static/                       # CSS and JS for status UI
│
├── config.json                   # DB credentials and HTTP endpoint URLs
├── tools_config.yaml             # YAML-defined simple single-table tools
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── uvicorn_log_config.ini        # Logging configuration
├── CLAUDE.md                     # Guidance for Claude Code working in this repo
└── README.md                     # Setup guide for new users
```

---

## Tool Design Principles

### Tools represent natural questions, not database tables

The unit of a tool is the natural question Claude would ask, not the underlying table schema. This means:

- Some tools map to a single table (when table = natural question)
- Some tools combine multiple tables with join logic baked in
- Claude never needs to know or reason about the table structure

The tool's `description` parameter is what Claude reads to decide which tool to call. Descriptions are written as natural language questions, not schema names.

### Two access patterns

**Database tools** (Peewee → MariaDB):
```python
@mcp.tool(description="Sleep quality and recovery data combining sleep stages and nightly recharge")
def get_sleep(days: int = 14) -> list[dict]:
    # Joins polar_sleep_daily + polar_nightly_recharge
    # Multi-table logic lives here, invisible to Claude
    ...
```

**HTTP tools** (requests → external API):
```python
@mcp.tool(description="Bike fleet status, component wear, and maintenance schedule")
def get_bikes() -> list[dict]:
    return http_connector.get("/api/bikes")
```

### Tool granularity — reference implementation

| Tool | Tables / source | Natural question answered |
|---|---|---|
| `get_transactions` | `transactions` | What have I been spending money on? |
| `get_financial_overview` | `balance` + `transactions` + `supersaver` | What is my current financial position? |
| `get_training` | `strava` | What athletic activities have I done? |
| `get_sleep` | `polar_sleep_daily` + `polar_nightly_recharge` | How have I been sleeping? |
| `get_recovery_and_load` | `polar_nightly_recharge` + `polar_cardio_load` + `strava` | Am I recovering well vs training load? |
| `get_weight` | `fitbit` | How has my weight changed? |
| `get_indoor_climate` | `vindstyrka` | What is the indoor air quality? |
| `get_outdoor_conditions` | `yr_weather` + `nilu` | What are current outdoor conditions including air quality? |
| `get_bikes` | velo-supervisor-2000 API | What is the status of my bikes and components? |

### Cross-domain queries

For questions that span domains (e.g. "on days I run over 15km, how does my sleep compare?"), Claude makes multiple tool calls and reasons across the results. This works well natively and requires no special implementation.

---

## Adding a New Data Source

### Option A — YAML (simple single-table sources, no Python needed)

Add an entry to `tools_config.yaml`:

```yaml
tools:
  - name: get_weather
    description: "Current and recent outdoor weather including temperature, wind and precipitation"
    type: database
    table: yr_weather
    fields: [record_time, temperature, wind_speed, precipitation]
    default_days: 7
    filters:
      - name: days
        type: int
        default: 7
```

### Option B — Python plugin (multi-table, computed, or HTTP sources)

Create a file in `tools/` and use the `@mcp.tool` decorator. The tool registry auto-discovers all `tools/*.py` files on startup.

```python
# tools/my_data.py
from core.tool_registry import mcp
from models import MyModel

@mcp.tool(description="Description Claude reads to decide when to call this tool")
def get_my_data(days: int = 30) -> list[dict]:
    results = (MyModel
               .select()
               .where(MyModel.record_time >= some_date)
               .order_by(MyModel.record_time.desc())
               .limit(100))
    return [{"field": r.field, ...} for r in results]
```

---

## Read-Only Design (Phase 1)

All tools in Phase 1 are strictly read-only. The MariaDB user configured in `config.json` should have `SELECT` privileges only. No tool writes to the database or triggers side effects.

Write tools (MQTT commands, container restarts, sync triggers) are planned for Phase 2 and will be implemented as a separate `ActionTools` class, registered alongside read tools without structural changes to the server.

---

## Status Web UI

The status page at `/` is a lightweight Bootstrap 5 single-page interface providing an at-a-glance view of server health. It is served by the same FastAPI app as the MCP endpoint — no separate process needed.

**Panels:**

- **Server status** — uptime, start time, DB connection (live check), external API reachability
- **Registered tools** — live list of all tools with their descriptions (serves as runtime documentation)
- **Recent activity** — last 50 tool calls from the in-memory ring buffer, showing timestamp, tool name, parameters, duration and success/fail
- **Active connections** — number of currently connected Claude Code SSE clients

The ring buffer holds only metadata (tool name, parameters, duration, row count or error message). Actual query results are not stored in the ring buffer.

The page auto-refreshes every 30 seconds.

---

## Logging

Logging uses **uvicorn's built-in logging** configured via `uvicorn_log_config.ini`. All output goes to stdout following the standard format used across the project:

```
%(asctime)s - %(levelname)s - %(message)s
```

This keeps the server portable — no external log aggregation infrastructure is required. Users who run Loki/Promtail or similar can pick up stdout from the Docker container as normal, but it is not a dependency.

**What is logged:**

- Server lifecycle — startup, shutdown, DB connection established or failed
- Tool invocations — tool name, parameters, duration, row count or error
- HTTP connector calls — URL, status code, latency
- Client connections — connect and disconnect events
- DB errors — Peewee exceptions and connection timeouts

Example log lines:
```
25-Mar-26 14:32:01 - INFO  - Tool called: get_health | params: {domain: sleep, days: 14} | 87ms | 14 rows
25-Mar-26 14:32:45 - INFO  - Tool called: get_finance | params: {days: 30} | 43ms | 28 rows
25-Mar-26 14:33:10 - ERROR - Tool failed: get_bikes | Connection timeout | 5001ms
```

---

## Configuration

`config.json` holds all deployment-specific values. It follows the same pattern used throughout the project:

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

The MariaDB user should be a dedicated read-only account — not the root user.

---

## Docker Deployment

The server follows the same Docker patterns used by all other services in the project.

**`Dockerfile`** — standard Python image, copies source, runs uvicorn:
```dockerfile
CMD ["uvicorn", "core.server:app", "--host", "0.0.0.0", "--port", "8002", \
     "--log-config", "uvicorn_log_config.ini"]
```

**`create-container-mcp.sh`**:
```bash
docker run -d \
  --name=memex-redux \
  -e TZ=Europe/Oslo \
  -e CONFIG_FILE=config.json \
  --restart unless-stopped \
  -p 8002:8002 \
  memex-redux
```

**Docker health check** — polls `/health` endpoint:
```dockerfile
HEALTHCHECK --interval=10m --timeout=10s \
  CMD curl -f http://localhost:8002/health || exit 1
```

---

## Connecting Claude Code

Register the server once per user:

```bash
claude mcp add --transport http --scope user homelab http://<host>:8002/mcp
```

Verify the connection:

```bash
claude mcp list
claude mcp get homelab
```

From that point on, Claude Code can use all registered tools in any session without further configuration.

---

## Phase 2 — Planned Extensions

The following are out of scope for Phase 1 but are accounted for in the design. They will be implemented as a separate `ActionTools` class registered alongside read tools, with no structural changes to the server core.

### Write — database

Direct writes to MariaDB via Peewee, following the same ORM patterns as the read tools. This enables Claude to record data on your behalf — for example logging a manual activity, annotating a transaction, or updating a record. All write tools will require explicit confirmation in the tool description to make their side effects clear to Claude before it calls them.

| Tool | Table | Example use |
|---|---|---|
| `write_transaction` | `transactions` | Log a cash purchase not captured by the bank sync |
| `write_activity` | `strava` | Record a manual activity |
| `annotate_record` | various | Add a comment or tag to an existing record |

### Write — external APIs

API calls to external services that trigger real-world side effects. These use the same `HttpConnector` base class as the read HTTP tools, but issue `POST`/`PUT`/`PATCH` requests.

| Tool | Target | Example use |
|---|---|---|
| `update_bike_component` | velo-supervisor-2000 API | Log a component replacement or maintenance action |
| `reset_component_distance` | velo-supervisor-2000 API | Reset distance counter after a service |
| `add_bike_note` | velo-supervisor-2000 API | Record a note against a bike or component |

### Action tools — home automation

Tools that trigger behaviour rather than store data.

| Capability | Implementation approach |
|---|---|
| Send MQTT commands | HTTP POST to `mqtt-publisher` endpoint |
| Restart containers | Portainer API |
| Trigger data sync | HTTP POST to relevant sync service |
| Additional channels | Claude Code channels (Discord, Telegram, others) connecting to the same `/mcp` endpoint |

---

## Open Questions

- **Authentication** — the server currently runs without auth, appropriate for a home network. If exposed externally, a bearer token header can be added to both the server and the `claude mcp add` command (`--header "Authorization: Bearer <token>"`).
- **velo-supervisor-2000 API shape** — the exact endpoints need to be confirmed before implementing `bikes.py`.
