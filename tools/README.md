# Tool Plugins

Drop a `.py` file in this directory to add a new data source. It will be auto-discovered and loaded at startup.

Each file should import `mcp` from `core.tool_registry` and use the `@mcp.tool()` decorator.

See existing files (`finance.py`, `health.py`, `climate.py`, `bikes.py`) for examples.
