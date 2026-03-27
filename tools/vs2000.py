# tools/vs2000.py — velo-supervisor-2000 tools (stubbed, API shape TBD)
# Implements: get_bikes()
# Access pattern: HTTP → velo-supervisor-2000 API
# Unblock by: confirming API endpoints and response schema

from core.tool_registry import mcp


@mcp.tool(description="Bike fleet status, component wear, and maintenance schedule")
def get_bikes() -> list[dict]:
    # TODO Phase B: implement once velo-supervisor-2000 API shape is confirmed
    return []
