# core/server.py — FastAPI app, MCP mount, lifespan
import time
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.call_log import call_log
from core.db_connection import check_db_connection
from core.tool_registry import discover_tools, mcp, _registered_tools

_start_time = time.monotonic()
_start_dt = datetime.now().isoformat()

templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    discover_tools()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def status_page(request: Request):
    return templates.TemplateResponse(request, "status.html")


@app.get("/health")
async def health():
    return {"status": "ok", "uptime_seconds": time.monotonic() - _start_time}


@app.get("/api/status")
async def api_status():
    return {
        "uptime_seconds": int(time.monotonic() - _start_time),
        "start_time": _start_dt,
        "db_connected": check_db_connection(),
        "tools": _registered_tools,
        "recent_calls": call_log.get_all(),
    }


# Must be last: streamable_http_app() exposes an internal /mcp route.
# Mounting at / (after all other routes) lets /mcp reach it while keeping
# /, /health, and /api/status handled by FastAPI above.
app.mount("/", mcp.streamable_http_app())
