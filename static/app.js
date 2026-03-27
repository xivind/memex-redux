// static/app.js — Status page: fetch /api/status, render panels, auto-refresh

const REFRESH_MS = 30_000;

function fmtUptime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return [h, m, s].map(v => String(v).padStart(2, "0")).join(":");
}

function fmtTime(iso) {
  return new Date(iso).toLocaleTimeString();
}

function renderStatus(data) {
  document.getElementById("stat-start").textContent = new Date(data.start_time).toLocaleString();
  document.getElementById("stat-uptime").textContent = fmtUptime(data.uptime_seconds);

  const dbEl = document.getElementById("stat-db");
  dbEl.innerHTML = data.db_connected
    ? '<span class="badge bg-success">Connected</span>'
    : '<span class="badge bg-danger">Disconnected</span>';
}

function renderTools(tools) {
  document.getElementById("tool-count").textContent = tools.length;
  const tbody = document.getElementById("tools-body");
  tbody.innerHTML = tools.map(t => `
    <tr>
      <td><code>${t.name}</code></td>
      <td class="text-muted">${t.description}</td>
    </tr>`).join("");
}

function renderActivity(calls) {
  const tbody = document.getElementById("activity-body");
  if (!calls.length) {
    tbody.innerHTML = '<tr><td colspan="5" class="text-muted text-center py-3">No calls yet</td></tr>';
    return;
  }
  tbody.innerHTML = [...calls].reverse().map(c => {
    const result = c.error
      ? `<span class="text-danger">${c.error}</span>`
      : `<span class="text-success">${c.row_count ?? "—"} rows</span>`;
    return `<tr>
      <td class="text-muted small">${fmtTime(c.timestamp)}</td>
      <td><code>${c.tool_name}</code></td>
      <td class="text-muted small">${JSON.stringify(c.params)}</td>
      <td class="text-muted small">${c.duration_ms}ms</td>
      <td>${result}</td>
    </tr>`;
  }).join("");
}

async function refresh() {
  const badge = document.getElementById("refresh-badge");
  try {
    const res = await fetch("/api/status");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderStatus(data);
    renderTools(data.tools);
    renderActivity(data.recent_calls);
    badge.className = "badge bg-success";
    badge.textContent = `Updated ${new Date().toLocaleTimeString()}`;
  } catch (err) {
    badge.className = "badge bg-danger";
    badge.textContent = "Fetch failed";
  }
}

refresh();
setInterval(refresh, REFRESH_MS);
