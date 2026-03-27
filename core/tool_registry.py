# core/tool_registry.py — FastMCP instance, auto-discovery of tool plugins
import functools
import importlib
import time
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from core.call_log import call_log

mcp = FastMCP("memex-mcp", stateless_http=True)

_registered_tools: list[dict] = []

_original_tool = mcp.tool


def _logged_tool(description: str = "", **decorator_kwargs):
    def decorator(func):
        _registered_tools.append({"name": func.__name__, "description": description})

        @functools.wraps(func)
        def wrapper(**call_kwargs):
            start = time.monotonic()
            try:
                result = func(**call_kwargs)
                duration_ms = int((time.monotonic() - start) * 1000)
                call_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "tool_name": func.__name__,
                    "params": call_kwargs,
                    "duration_ms": duration_ms,
                    "row_count": len(result) if isinstance(result, list) else None,
                    "error": None,
                })
                return result
            except Exception as e:
                duration_ms = int((time.monotonic() - start) * 1000)
                call_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "tool_name": func.__name__,
                    "params": call_kwargs,
                    "duration_ms": duration_ms,
                    "row_count": None,
                    "error": str(e),
                })
                raise

        return _original_tool(description=description, **decorator_kwargs)(wrapper)

    return decorator


mcp.tool = _logged_tool


def discover_tools() -> None:
    tools_dir = Path(__file__).parent.parent / "tools"
    for path in sorted(tools_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        importlib.import_module(f"tools.{path.stem}")
