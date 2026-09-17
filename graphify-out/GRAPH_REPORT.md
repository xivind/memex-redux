# Graph Report - memex-redux  (2026-09-17)

## Corpus Check
- Corpus is ~7,923 words - fits in a single context window. You may not need a graph.

## Summary
- 278 nodes · 403 edges · 38 communities (22 shown, 8 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 32 edges (avg confidence: 0.92)
- Token cost: 138,814 input · 0 output

## Community Hubs (Navigation)
- Project Config & Stack
- Core Server & DB Connection
- Finance Budget Tool (Moneybags)
- HTTP Connector & Bathing Temps
- Tool Call Logging
- Health Data Tests (Polar)
- Status Page Frontend
- Server API Tests
- Strava Activity Tool
- System Architecture Diagram
- Status Page JS Rendering
- Tool Registry Tests
- DB Connection Tests
- VS2000 Bike Tool
- Air Pollution Tool
- Balance Tool
- Indoor Climate Tool
- Polar Training Tool
- Sleep Tool
- Transactions Tool
- Weight Tool
- Example Data Models
- Sample Test Fixtures
- Core Test Fixtures
- Container Creation Script
- Package Init
- HTTPX Dependency
- Jinja2 Dependency
- Pytest Dependency
- PyYAML Dependency

## God Nodes (most connected - your core abstractions)
1. `memex-redux (Project Description)` - 15 edges
2. `memex-redux MCP Server Skeleton` - 14 edges
3. `CallLog` - 10 edges
4. `Status Page (Bootstrap 5 UI)` - 9 edges
5. `HttpConnector` - 8 edges
6. `_reload_registry()` - 7 edges
7. `_budget_for_period()` - 6 edges
8. `_expenses_for_period()` - 6 edges
9. `Tool Plugin Auto-Discovery Pattern` - 6 edges
10. `Bootstrap 5 + Vanilla JS Frontend Policy` - 6 edges

## Surprising Connections (you probably didn't know these)
- `config.json Configuration Schema` --semantically_similar_to--> `Setup Instructions`  [INFERRED] [semantically similar]
  CLAUDE.md → README.md
- `Uvicorn` --semantically_similar_to--> `uvicorn (requirements.txt entry)`  [INFERRED] [semantically similar]
  CLAUDE.md → requirements.txt
- `memex-redux MCP Server Skeleton` --semantically_similar_to--> `memex-redux (Project Description)`  [INFERRED] [semantically similar]
  CLAUDE.md → README.md
- `Tool Plugin Auto-Discovery Pattern` --semantically_similar_to--> `Tool Plugin Example (get_finance)`  [INFERRED] [semantically similar]
  CLAUDE.md → README.md
- `Tool Plugin Auto-Discovery Pattern` --semantically_similar_to--> `tools/*.py Gitignore Policy`  [INFERRED] [semantically similar]
  CLAUDE.md → tools/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **memex-redux Technology Stack (CLAUDE.md)** — claude_fastapi, claude_uvicorn, claude_mcp_fastmcp, claude_peewee, claude_pymysql, claude_requests_lib, claude_pydantic, claude_bootstrap5, claude_uv [EXTRACTED 1.00]
- **Tool Plugin Auto-Discovery Convention (documented across 3 files)** — claude_tool_plugin_pattern, readme_tool_plugin_pattern, tools_readme_tool_plugin_pattern [INFERRED 0.85]
- **requirements.txt Declared Python Dependencies** — requirements_fastapi, requirements_uvicorn, requirements_mcp, requirements_peewee, requirements_pymysql, requirements_requests, requirements_pydantic, requirements_pyyaml, requirements_jinja2, requirements_pytest, requirements_httpx [EXTRACTED 1.00]
- **Claude Code to Tool Registry request pipeline** — docs_architecture_claude_code, docs_architecture_memex_redux, docs_architecture_mcp_endpoint, docs_architecture_tool_registry [EXTRACTED 1.00]
- **Plugin fan-out to SQL Database and External API** — docs_architecture_tool_registry, docs_architecture_plugin, docs_architecture_sql_database, docs_architecture_external_api [EXTRACTED 1.00]

## Communities (38 total, 8 thin omitted)

### Community 0 - "Project Config & Stack"
Cohesion: 0.07
Nodes (44): config.json Configuration Schema, Connecting a Claude Code Client, Docker Deployment & Healthcheck, FastAPI, Graphify Knowledge Graph Integration, Uvicorn-Only Logging Policy, MCP SDK / FastMCP, memex-redux MCP Server Skeleton (+36 more)

### Community 1 - "Core Server & DB Connection"
Cohesion: 0.14
Nodes (17): BaseModel, check_db_connection(), Config, _load_config(), api_status(), health(), lifespan(), status_page() (+9 more)

### Community 2 - "Finance Budget Tool (Moneybags)"
Cohesion: 0.27
Nodes (19): _budget_for_period(), _current_month_range(), _expenses_for_period(), get_budget_current_month(), get_budget_last_3_months(), get_budget_last_month(), get_budget_ytd(), get_expenses_current_month() (+11 more)

### Community 3 - "HTTP Connector & Bathing Temps"
Cohesion: 0.27
Nodes (8): HttpConnector, _mock_response(), test_get_raises_on_http_error(), test_get_returns_json(), test_get_strips_trailing_slash_from_base(), get_bathing_temperatures(), tool, search_bathing_spots()

### Community 4 - "Tool Call Logging"
Cohesion: 0.26
Nodes (6): Any, CallLog, test_append_and_get_all(), test_empty_log_returns_empty_list(), test_get_all_returns_copy(), test_maxlen_evicts_oldest()

### Community 5 - "Health Data Tests (Polar)"
Cohesion: 0.27
Nodes (9): _polar_activity(), _polar_cardio(), _polar_recharge(), _polar_sleep(), test_get_sleep_combines_sleep_and_recharge(), test_get_sleep_filters_by_days(), test_get_sleep_sleep_only_no_recharge(), test_get_training_combines_cardio_and_activity() (+1 more)

### Community 6 - "Status Page Frontend"
Cohesion: 0.24
Nodes (11): Bootstrap 5, Bootstrap 5 + Vanilla JS Frontend Policy, Bootstrap 5, Recent Activity Table, app.css Stylesheet Reference, app.js Script Reference, Bootstrap 5.3.3 CDN Link, Connections Card (+3 more)

### Community 8 - "Strava Activity Tool"
Cohesion: 0.44
Nodes (9): get_strava_activities_30d(), get_strava_activities_90d(), get_strava_summary_30d(), get_strava_summary_90d(), _load_gear(), datetime, tool, _query_strava_activities() (+1 more)

### Community 9 - "System Architecture Diagram"
Cohesion: 0.25
Nodes (8): Claude Code, External API, MCP Endpoint, memex-redux server, Auto-discovered plugin card (tools/*.py), Plugin extensibility (dashed ellipsis card), SQL Database, Tool Registry

### Community 10 - "Status Page JS Rendering"
Cohesion: 0.46
Nodes (7): fmtTime(), fmtUptime(), refresh(), renderActivity(), renderStatus(), renderTools(), statusBadge()

### Community 11 - "Tool Registry Tests"
Cohesion: 0.43
Nodes (7): Fresh import of tool_registry to reset module state., _reload_registry(), test_call_log_entry_on_error(), test_call_log_entry_on_success(), test_discover_tools_imports_py_files(), test_discover_tools_skips_underscore_files(), test_registered_tools_populated_on_decoration()

### Community 16 - "VS2000 Bike Tool"
Cohesion: 0.40
Nodes (3): test_get_vs2000_returns_list(), get_vs2000(), tool

### Community 17 - "Air Pollution Tool"
Cohesion: 0.60
Nodes (5): get_air_pollution_30d(), get_air_pollution_90d(), datetime, tool, _query_air_pollution()

### Community 18 - "Balance Tool"
Cohesion: 0.53
Nodes (5): get_balance_30d(), get_balance_90d(), date, tool, _query_balance()

### Community 19 - "Indoor Climate Tool"
Cohesion: 0.60
Nodes (5): get_indoor_climate_30d(), get_indoor_climate_90d(), datetime, tool, _query_indoor()

### Community 20 - "Polar Training Tool"
Cohesion: 0.53
Nodes (5): get_polar_training_30d(), get_polar_training_90d(), date, tool, _query_polar_training()

### Community 21 - "Sleep Tool"
Cohesion: 0.53
Nodes (5): get_sleep_30d(), get_sleep_90d(), date, tool, _query_sleep()

### Community 22 - "Transactions Tool"
Cohesion: 0.53
Nodes (5): get_transactions_30d(), get_transactions_90d(), date, tool, _query_transactions()

### Community 23 - "Weight Tool"
Cohesion: 0.53
Nodes (5): get_weight_30d(), get_weight_90d(), date, tool, _query_weight()

### Community 24 - "Example Data Models"
Cohesion: 0.60
Nodes (4): DailyMetric, Event, Meta, SensorReading

### Community 25 - "Sample Test Fixtures"
Cohesion: 0.50
Nodes (4): db_session(), _get_all_models(), fixture, SQLite in-memory DB with all tables created. Binds all models to test DB.

### Community 26 - "Core Test Fixtures"
Cohesion: 0.50
Nodes (3): no_db(), fixture, Prevent real DB calls during server tests.

## Knowledge Gaps
- **20 isolated node(s):** `create-container.sh script`, `memex-redux`, `Graphify Knowledge Graph Integration`, `Vannevar Bush's 1945 Memex Essay`, `Architecture Diagram (docs/architecture.svg)` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 79 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `memex-redux (Project Description)` connect `Project Config & Stack` to `Status Page Frontend`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `memex-redux (Project Description)` (e.g. with `memex-redux MCP Server Skeleton` and `tools/*.py Gitignore Policy`) actually correct?**
  _`memex-redux (Project Description)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `create-container.sh script`, `memex-redux`, `Graphify Knowledge Graph Integration` to the rest of the system?**
  _20 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project Config & Stack` be split into smaller, more focused modules?**
  _Cohesion score 0.07188160676532769 - nodes in this community are weakly interconnected._
- **Should `Core Server & DB Connection` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._