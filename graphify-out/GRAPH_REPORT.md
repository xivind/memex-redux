# Graph Report - memex-redux  (2026-10-27)

## Corpus Check
- 3 files · ~7,809 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 271 nodes · 378 edges · 37 communities (24 shown, 13 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.86)
- Token cost: 63,525 input · 0 output

## Community Hubs (Navigation)
- Architecture & Configuration Docs
- Core Server & DB Connection
- Finance Budget Tool (Moneybags)
- Server Runtime & MCP Stack
- HTTP Connector & Bathing Temps
- Tool Call Logging
- Health Data Tests (Polar)
- Server API Tests
- Strava Activity Tool
- System Architecture Diagram
- Status Page JS Rendering
- Status Page Frontend
- Tool Registry Tests
- DB Connection Tests
- VS2000 Bike Tool
- Air Pollution Tool
- Indoor Climate Tool
- Outdoor Climate Tool
- Polar Training Tool
- Sleep Tool
- Transactions Tool
- Weight Tool
- Example Data Models
- Sample Test Fixtures
- Core Test Fixtures
- Tool Plugin Policy
- Container Creation Script
- graphify Rules
- Package Init

## God Nodes (most connected - your core abstractions)
1. `CallLog` - 10 edges
2. `HttpConnector` - 8 edges
3. `_reload_registry()` - 7 edges
4. `Status Page (Bootstrap 5 UI)` - 7 edges
5. `_budget_for_period()` - 6 edges
6. `_expenses_for_period()` - 6 edges
7. `Tool Plugins (tools/)` - 6 edges
8. `config.json` - 6 edges
9. `_query_strava_activities()` - 5 edges
10. `_query_strava_summary()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `claude mcp add Client Connection` --semantically_similar_to--> `.mcp.json Project Connection`  [INFERRED] [semantically similar]
  README.md → CLAUDE.md
- `test_append_and_get_all()` --calls--> `CallLog`  [EXTRACTED]
  tests/test_call_log.py → core/call_log.py
- `test_empty_log_returns_empty_list()` --calls--> `CallLog`  [EXTRACTED]
  tests/test_call_log.py → core/call_log.py
- `test_get_all_returns_copy()` --calls--> `CallLog`  [EXTRACTED]
  tests/test_call_log.py → core/call_log.py
- `test_maxlen_evicts_oldest()` --calls--> `CallLog`  [EXTRACTED]
  tests/test_call_log.py → core/call_log.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Claude Code to Tool Registry request pipeline** — docs_architecture_claude_code, docs_architecture_memex_redux, docs_architecture_mcp_endpoint, docs_architecture_tool_registry [EXTRACTED 1.00]
- **Plugin fan-out to SQL Database and External API** — docs_architecture_tool_registry, docs_architecture_plugin, docs_architecture_sql_database, docs_architecture_external_api [EXTRACTED 1.00]
- **memex-redux Core Infrastructure Modules** — claude_fastapi_app, claude_tool_registry, claude_db_connection, claude_http_connector, claude_call_log [EXTRACTED 1.00]
- **Read-only Trusted-network Security Model** — claude_read_only_tools, claude_readonly_mariadb_account, claude_no_authentication, readme_gitignored_user_files [INFERRED 0.85]
- **Tool Plugin Authoring and Discovery Flow** — claude_tool_plugins, claude_tool_registry, claude_mcp_tool_decorator, claude_tools_as_natural_questions, claude_fastmcp [INFERRED 0.85]

## Communities (37 total, 13 thin omitted)

### Community 0 - "Architecture & Configuration Docs"
Cohesion: 0.10
Nodes (27): config.json, Database Access Pattern (Peewee to MariaDB), DB Connection (Peewee init), Generic Extensible MCP Server Skeleton, HTTP Access Pattern (requests to external API), HttpConnector Base Class, @mcp.tool Decorator, memex-redux MCP Server (+19 more)

### Community 1 - "Core Server & DB Connection"
Cohesion: 0.14
Nodes (17): BaseModel, check_db_connection(), Config, _load_config(), api_status(), health(), lifespan(), status_page() (+9 more)

### Community 2 - "Finance Budget Tool (Moneybags)"
Cohesion: 0.27
Nodes (19): _budget_for_period(), _current_month_range(), _expenses_for_period(), get_budget_current_month(), get_budget_last_3_months(), get_budget_last_month(), get_budget_ytd(), get_expenses_current_month() (+11 more)

### Community 3 - "Server Runtime & MCP Stack"
Cohesion: 0.17
Nodes (13): Call Log Ring Buffer, Docker HEALTHCHECK, FastAPI App (core/server.py), FastMCP (mcp SDK), Frontend Conventions (Bootstrap 5 + Vanilla JS), /health Endpoint, /mcp Endpoint, .mcp.json Project Connection (+5 more)

### Community 4 - "HTTP Connector & Bathing Temps"
Cohesion: 0.27
Nodes (8): HttpConnector, _mock_response(), test_get_raises_on_http_error(), test_get_returns_json(), test_get_strips_trailing_slash_from_base(), get_bathing_temperatures(), tool, search_bathing_spots()

### Community 5 - "Tool Call Logging"
Cohesion: 0.26
Nodes (6): Any, CallLog, test_append_and_get_all(), test_empty_log_returns_empty_list(), test_get_all_returns_copy(), test_maxlen_evicts_oldest()

### Community 6 - "Health Data Tests (Polar)"
Cohesion: 0.27
Nodes (9): _polar_activity(), _polar_cardio(), _polar_recharge(), _polar_sleep(), test_get_sleep_combines_sleep_and_recharge(), test_get_sleep_filters_by_days(), test_get_sleep_sleep_only_no_recharge(), test_get_training_combines_cardio_and_activity() (+1 more)

### Community 8 - "Strava Activity Tool"
Cohesion: 0.44
Nodes (9): get_strava_activities_30d(), get_strava_activities_90d(), get_strava_summary_30d(), get_strava_summary_90d(), _load_gear(), datetime, tool, _query_strava_activities() (+1 more)

### Community 9 - "System Architecture Diagram"
Cohesion: 0.25
Nodes (8): Claude Code, External API, MCP Endpoint, memex-redux server, Auto-discovered plugin card (tools/*.py), Plugin extensibility (dashed ellipsis card), SQL Database, Tool Registry

### Community 10 - "Status Page JS Rendering"
Cohesion: 0.46
Nodes (7): fmtTime(), fmtUptime(), refresh(), renderActivity(), renderStatus(), renderTools(), statusBadge()

### Community 11 - "Status Page Frontend"
Cohesion: 0.25
Nodes (8): Recent Activity Table, app.css Stylesheet Reference, app.js Script Reference, Bootstrap 5.3.3 CDN Link, Connections Card, Status Page (Bootstrap 5 UI), Server Stats Card, Registered Tools Table

### Community 12 - "Tool Registry Tests"
Cohesion: 0.43
Nodes (7): Fresh import of tool_registry to reset module state., _reload_registry(), test_call_log_entry_on_error(), test_call_log_entry_on_success(), test_discover_tools_imports_py_files(), test_discover_tools_skips_underscore_files(), test_registered_tools_populated_on_decoration()

### Community 17 - "VS2000 Bike Tool"
Cohesion: 0.40
Nodes (3): test_get_vs2000_returns_list(), get_vs2000(), tool

### Community 18 - "Air Pollution Tool"
Cohesion: 0.60
Nodes (5): get_air_pollution_30d(), get_air_pollution_90d(), datetime, tool, _query_air_pollution()

### Community 19 - "Indoor Climate Tool"
Cohesion: 0.60
Nodes (5): get_indoor_climate_30d(), get_indoor_climate_90d(), datetime, tool, _query_indoor()

### Community 20 - "Outdoor Climate Tool"
Cohesion: 0.60
Nodes (5): get_outdoor_climate_30d(), get_outdoor_climate_90d(), datetime, tool, _query_outdoor()

### Community 21 - "Polar Training Tool"
Cohesion: 0.53
Nodes (5): get_polar_training_30d(), get_polar_training_90d(), date, tool, _query_polar_training()

### Community 22 - "Sleep Tool"
Cohesion: 0.53
Nodes (5): get_sleep_30d(), get_sleep_90d(), date, tool, _query_sleep()

### Community 23 - "Transactions Tool"
Cohesion: 0.53
Nodes (5): get_transactions_30d(), get_transactions_90d(), date, tool, _query_transactions()

### Community 24 - "Weight Tool"
Cohesion: 0.53
Nodes (5): get_weight_30d(), get_weight_90d(), date, tool, _query_weight()

### Community 25 - "Example Data Models"
Cohesion: 0.60
Nodes (4): DailyMetric, Event, Meta, SensorReading

### Community 26 - "Sample Test Fixtures"
Cohesion: 0.50
Nodes (4): db_session(), _get_all_models(), fixture, SQLite in-memory DB with all tables created. Binds all models to test DB.

### Community 27 - "Core Test Fixtures"
Cohesion: 0.50
Nodes (3): no_db(), fixture, Prevent real DB calls during server tests.

### Community 28 - "Tool Plugin Policy"
Cohesion: 0.67
Nodes (3): tools/*.py Gitignore Policy, tools/samples Reference Implementations, Tool Plugin Auto-Discovery (tools/README)

## Knowledge Gaps
- **17 isolated node(s):** `create-container.sh script`, `memex-redux`, `tools/samples Reference Implementations`, `Recent Activity Table`, `app.css Stylesheet Reference` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 80 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `create-container.sh script`, `memex-redux`, `tools/samples Reference Implementations` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Architecture & Configuration Docs` be split into smaller, more focused modules?**
  _Cohesion score 0.09971509971509972 - nodes in this community are weakly interconnected._
- **Should `Core Server & DB Connection` be split into smaller, more focused modules?**
  _Cohesion score 0.13852813852813853 - nodes in this community are weakly interconnected._