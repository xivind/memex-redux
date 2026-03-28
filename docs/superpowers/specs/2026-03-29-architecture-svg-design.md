# Architecture SVG Design

**Date:** 2026-03-29
**Status:** Approved

## Goal

A static SVG architecture diagram saved at `docs/architecture.svg` and referenced from `README.md`. Conceptual level only — no port numbers, no domain-specific plugin names, no technology version details.

---

## Layout

Top-down, three tiers.

### Tier 1 — Consumer

A single box: **Claude Code**

### Tier 2 — Server

A large rounded rect: **memex-redux**

Labeled edge connecting Tier 1 to Tier 2: **MCP / Streamable HTTP**

#### Internal structure (top to bottom inside the server box)

1. **MCP Endpoint** — receives incoming tool calls
2. Downward arrow
3. **Tool Registry** — routes calls to the registered plugin
4. Downward arrow
5. **tools/*.py** — a horizontal row of three small cards with a `…` card to the right, representing auto-discovered plugins. All cards share the same generic label to communicate interchangeability and extensibility.

### Tier 3 — Data sources

Two boxes connected by arrows from the plugin row:

- **Left:** `SQL Database` — plain rounded rect
- **Right:** `External APIs` — stacked card visual (three slightly offset rectangles), generic label on the top card. Represents N configured domains from `api_domains`.

---

## Style

- Monochrome or minimal colour palette consistent with a technical reference diagram
- Rounded rectangles throughout
- No port numbers, IP addresses, technology version strings
- No domain-specific plugin names (Finance, Health, etc.)
- Font: system sans-serif
- Arrows: simple directional, labelled only where the protocol adds meaningful context (the MCP edge)

---

## Deliverables

| File | Change |
|---|---|
| `docs/architecture.svg` | New file — the diagram |
| `README.md` | Add `![Architecture](docs/architecture.svg)` in an appropriate section |
