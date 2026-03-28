# Architecture SVG Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a static SVG architecture diagram at `docs/architecture.svg` and reference it from `README.md`, replacing the existing ASCII art.

**Architecture:** A hand-crafted SVG using absolute coordinates — no build tools, no external libraries. Top-down layout: Claude Code → memex-redux (with MCP Endpoint, Tool Registry, and plugin cards inside) → SQL Database and External APIs (stacked cards).

**Tech Stack:** SVG, README Markdown

---

## File Map

| File | Change |
|---|---|
| `docs/architecture.svg` | New file — the diagram |
| `README.md` | Remove ASCII art block; add `## Architecture` section with SVG image |

---

## Task 1: Create docs/architecture.svg

**Files:**
- Create: `docs/architecture.svg`

- [ ] **Step 1: Create the file**

Create `/home/xivind/code/memex-redux/docs/architecture.svg` with this exact content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="640" height="520" viewBox="0 0 640 520"
     font-family="system-ui, -apple-system, sans-serif">

  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8"
            refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>

  <!-- Claude Code -->
  <rect x="230" y="24" width="180" height="44" rx="6"
        fill="#f5f5f5" stroke="#555" stroke-width="1.5"/>
  <text x="320" y="51" text-anchor="middle"
        font-size="14" font-weight="600" fill="#222">Claude Code</text>

  <!-- Arrow: Claude Code → memex-redux -->
  <line x1="320" y1="68" x2="320" y2="113"
        stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="328" y="96" font-size="11" fill="#666">MCP / Streamable HTTP</text>

  <!-- memex-redux outer box -->
  <rect x="30" y="116" width="580" height="270" rx="10"
        fill="#eef0f8" stroke="#3a3a5c" stroke-width="1.5"/>
  <text x="52" y="136" font-size="12" font-weight="700"
        fill="#3a3a5c" letter-spacing="0.5">memex-redux</text>

  <!-- MCP Endpoint -->
  <rect x="220" y="142" width="200" height="36" rx="5"
        fill="#f5f5f5" stroke="#555" stroke-width="1.5"/>
  <text x="320" y="165" text-anchor="middle"
        font-size="13" fill="#222">MCP Endpoint</text>

  <!-- Arrow: MCP Endpoint → Tool Registry -->
  <line x1="320" y1="178" x2="320" y2="193"
        stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Tool Registry -->
  <rect x="220" y="196" width="200" height="36" rx="5"
        fill="#f5f5f5" stroke="#555" stroke-width="1.5"/>
  <text x="320" y="219" text-anchor="middle"
        font-size="13" fill="#222">Tool Registry</text>

  <!-- Arrow: Tool Registry → plugin cards (labeled with discovery pattern) -->
  <line x1="320" y1="232" x2="320" y2="258"
        stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="328" y="249" font-size="11" fill="#666"
        font-family="monospace">tools/*.py</text>

  <!-- Plugin cards (auto-discovered; dashed last card = extensibility) -->
  <rect x="133" y="262" width="86" height="36" rx="4"
        fill="white" stroke="#888" stroke-width="1"/>
  <text x="176" y="285" text-anchor="middle"
        font-size="11" fill="#444">plugin</text>

  <rect x="229" y="262" width="86" height="36" rx="4"
        fill="white" stroke="#888" stroke-width="1"/>
  <text x="272" y="285" text-anchor="middle"
        font-size="11" fill="#444">plugin</text>

  <rect x="325" y="262" width="86" height="36" rx="4"
        fill="white" stroke="#888" stroke-width="1"/>
  <text x="368" y="285" text-anchor="middle"
        font-size="11" fill="#444">plugin</text>

  <rect x="421" y="262" width="86" height="36" rx="4"
        fill="white" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="464" y="285" text-anchor="middle"
        font-size="14" fill="#aaa">…</text>

  <!-- Distribution bar + arrows to data sources -->
  <line x1="176" y1="302" x2="464" y2="302"
        stroke="#555" stroke-width="1.2"/>
  <line x1="176" y1="302" x2="176" y2="408"
        stroke="#555" stroke-width="1.2" marker-end="url(#arrow)"/>
  <line x1="464" y1="302" x2="464" y2="406"
        stroke="#555" stroke-width="1.2" marker-end="url(#arrow)"/>

  <!-- SQL Database -->
  <rect x="86" y="410" width="180" height="50" rx="6"
        fill="#f5f5f5" stroke="#555" stroke-width="1.5"/>
  <text x="176" y="440" text-anchor="middle"
        font-size="13" fill="#222">SQL Database</text>

  <!-- External APIs stacked cards (drawn back-to-front) -->
  <rect x="397" y="408" width="174" height="50" rx="6"
        fill="#e4e4ee" stroke="#aaa" stroke-width="1"/>
  <rect x="389" y="414" width="174" height="50" rx="6"
        fill="#eeeef8" stroke="#bbb" stroke-width="1"/>
  <rect x="379" y="420" width="174" height="50" rx="6"
        fill="#f5f5f5" stroke="#555" stroke-width="1.5"/>
  <text x="466" y="450" text-anchor="middle"
        font-size="13" fill="#222">External API</text>

</svg>
```

- [ ] **Step 2: Visually verify the diagram**

Open the file in a browser:

```bash
xdg-open /home/xivind/code/memex-redux/docs/architecture.svg
```

Check:
- Three tiers visible top-to-bottom: Claude Code → memex-redux box → data sources
- "memex-redux" label in top-left of the blue-tinted server box
- Inside the server box: MCP Endpoint → Tool Registry → four plugin cards
- Three solid plugin cards labeled "plugin", one dashed card labeled "…"
- "tools/*.py" label beside the arrow from Tool Registry to plugin cards
- Horizontal distribution bar below plugin cards, with two arrows exiting down
- Left arrow points to "SQL Database" box
- Right arrow points to a stack of three cards labeled "External API"
- "MCP / Streamable HTTP" label beside the arrow from Claude Code to memex-redux

If any element is missing, misaligned, or text is clipped, adjust the coordinate in question before committing. Common fixes:
- Text clipped at right edge: reduce `x` or use `text-anchor="end"`
- Box too small for text: increase `width` or `height`
- Arrow not touching box: adjust the `y2` endpoint value

- [ ] **Step 3: Commit**

```bash
git add docs/architecture.svg
git commit -m "feat: add architecture SVG diagram"
```

---

## Task 2: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Remove the ASCII art block from "What it does"**

In `README.md`, remove this block (lines 11–16):

```
```
Claude Code  ──(Streamable HTTP)──▶  memex-redux (port 8002)
                                          │
                                    ┌─────┴─────┐
                                 MariaDB     External APIs
```
```

Leave the surrounding text intact.

- [ ] **Step 2: Add an Architecture section**

After the `---` that follows the "What it does" section (after line 17) and before `## Stack`, insert:

```markdown
## Architecture

![Architecture](docs/architecture.svg)

---
```

The final order in the file should be:

```
## What it does
(text only, no ASCII art)

---

## Architecture

![Architecture](docs/architecture.svg)

---

## Stack
```

- [ ] **Step 3: Run existing tests to confirm no regressions**

```bash
python3 -m pytest tests/test_db_connection.py tests/test_vs2000.py -q
```

Expected: 6 passed. (README changes don't affect Python tests — this is a sanity check only.)

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: replace ASCII art with architecture SVG in README"
```
