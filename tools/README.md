# Tool Plugins

Drop a `.py` file in this directory to add a new data source. It will be auto-discovered and loaded at startup — no registration step required.

Each file should import `mcp` from `core.tool_registry` and use the `@mcp.tool()` decorator:

```python
from core.tool_registry import mcp

@mcp.tool(description="Recent transactions and account balances")
def get_finance(days: int = 30) -> list[dict]:
    ...
```

The `description` is what Claude reads to decide which tool to call — write it as a natural question.

## Samples

`tools/samples/` contains reference implementations for finance, health, climate, and HTTP-based sources. Copy and adapt them as a starting point — they are not loaded automatically (only files directly in `tools/` are discovered).

## Note on files in this directory

`tools/*.py` is gitignored (except `__init__.py`). Your plugins stay local and out of version control.
