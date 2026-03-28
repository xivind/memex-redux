# tools/vs2000.py — Velo Supervisor 2000 tools (stubbed, API shape TBD)
# Unblock by: confirming velo-supervisor-2000 API endpoints and response schema

from core.tool_registry import mcp


@mcp.tool(description="Velo Supervisor 2000 API: bike fleet status, component wear, and maintenance schedule")
def get_vs2000() -> list[dict]:
    # TODO Phase B: implement once velo-supervisor-2000 API shape is confirmed
    return []
