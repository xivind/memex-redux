# memex-redux

A generic, extensible MCP server for Claude Code. Connect your own databases and APIs to Claude as tools — named as a homage to Vannevar Bush's 1945 essay envisioning a device for storing and linking all of a person's knowledge and experience.

---

## What it does

memex-redux runs a local HTTP server that exposes your personal data sources as [MCP tools](https://modelcontextprotocol.io). Claude Code connects to it and can then query your data directly in conversation — finance, health, climate, home automation, or anything else you want to hook up.

```
Claude Code  ──(Streamable HTTP)──▶  memex-redux (port 8002)
                                          │
                                    ┌─────┴─────┐
                                 MariaDB     External APIs
```

Tools are Python plugins in `tools/`. Drop a file there, restart the server, and Claude can use it. No registration step required.

---

## Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI |
| ASGI server | Uvicorn |
| MCP SDK | `mcp` (Anthropic) — `FastMCP`, Streamable HTTP |
| Database ORM | Peewee |
| Database | MariaDB (read-only account) |
| HTTP client | requests |
| Frontend | Bootstrap 5 + vanilla JS |

---

## Repository structure

```
memex-redux/
├── core/
│   ├── server.py           # FastAPI app, MCP mount, lifespan
│   ├── tool_registry.py    # @tool decorator, auto-discovery of plugins
│   ├── db_connection.py    # Peewee initialisation
│   ├── http_connector.py   # Base class for HTTP data sources
│   └── call_log.py         # In-memory ring buffer (last 50 tool calls)
│
├── tools/                  # Your tool plugins — one file per data domain
│   └── README.md
│
├── models.example.py       # Template — copy to models.py and adapt
├── config.example.json     # Template — copy to config.json and fill in
├── templates/
│   └── status.html         # Bootstrap 5 status UI
├── static/
│   ├── app.js
│   └── app.css
├── Dockerfile
├── create-container.sh
└── requirements.txt
```

> `config.json` and `models.py` are gitignored — they contain your credentials and schema. Use the `.example` files as starting points.

---

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/xivind/memex-redux
cd memex-redux
pip install -r requirements.txt
```

### 2. Configure

```bash
cp config.example.json config.json
```

Edit `config.json` with your MariaDB connection details and any API endpoints you need:

```json
{
  "mariadb_host": "your-db-host",
  "mariadb_database": "your_database",
  "mariadb_user": "mcp_readonly",
  "mariadb_password": "your_password",
  "mariadb_port": 3306,
  "server_port": 8002
}
```

The MariaDB user should be a dedicated read-only account (`SELECT` privileges only).

### 3. Define your database models

```bash
cp models.example.py models.py
```

Edit `models.py` to define Peewee models matching your database tables. See the example file for common patterns (simple tables, no primary key, composite primary key).

### 4. Add tool plugins

Create a file in `tools/`, import `mcp` from `core.tool_registry`, and decorate your functions:

```python
from core.tool_registry import mcp

@mcp.tool(description="Recent transactions and account balances")
def get_finance(days: int = 30) -> list[dict]:
    from models import Transaction
    cutoff = datetime.now() - timedelta(days=days)
    rows = Transaction.select().where(Transaction.record_time >= cutoff)
    return [{"date": r.record_time, "amount": r.amount} for r in rows]
```

The `description` is what Claude reads to decide which tool to call — write it as a natural question.

### 5. Run

```bash
uvicorn core.server:app --host 0.0.0.0 --port 8002 --log-config uvicorn_log_config.ini
```

Or with Docker:

```bash
./create-container.sh
```

A status page is available at `http://localhost:8002/` showing registered tools and recent calls.

---

## Connecting Claude Code

```bash
claude mcp add --transport http --scope user memex-redux http://<host>:8002/mcp
```

`--scope user` makes the server available across all your Claude Code projects. After that, Claude will automatically use your tools when relevant.

---

## HTTP-based tools

For data sources behind an API rather than a database, subclass `HttpConnector`:

```python
from core.http_connector import HttpConnector
from core.tool_registry import mcp

connector = HttpConnector(base_url="http://my-service:8003")

@mcp.tool(description="Bike fleet status and maintenance schedule")
def get_bikes() -> list[dict]:
    return connector.get("/api/bikes")
```

---

## Constraints

- All tools are **read-only** by design. The database account has `SELECT` only.
- No authentication — assumes a trusted home network.
- Logging goes to stdout via uvicorn. No separate log config needed.
