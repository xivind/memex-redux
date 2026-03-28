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

function statusBadge(connected, labelOk, labelErr) {
  if (connected === true)  return `<span class="status-dot ok"></span>${labelOk}`;
  if (connected === false) return `<span class="status-dot err"></span><span class="text-danger">${labelErr}</span>`;
  return `<span class="status-dot na"></span><span class="text-muted">—</span>`;
}

function renderStatus(data) {
  document.getElementById("stat-start").textContent = new Date(data.start_time).toLocaleString();
  document.getElementById("stat-uptime").textContent = fmtUptime(data.uptime_seconds);
  document.getElementById("stat-total").textContent = data.total_calls.toLocaleString();
  document.getElementById("stat-db").innerHTML = statusBadge(data.db_connected, "Connected", "Disconnected");

  const grid = document.getElementById("connections-grid");
  grid.querySelectorAll(".api-domain-row").forEach(el => el.remove());
  for (const [name, connected] of Object.entries(data.api_domains)) {
    const label = document.createElement("span");
    label.className = "stat-label api-domain-row";
    label.textContent = name;

    const value = document.createElement("span");
    value.className = "stat-value api-domain-row";
    value.innerHTML = statusBadge(connected, "Connected", "Disconnected");

    grid.append(label, value);
  }
}

function renderTools(tools, callCounts) {
  document.getElementById("tool-count").textContent = tools.length;
  const tbody = document.getElementById("tools-body");
  tbody.innerHTML = tools.map(t => {
    const count = callCounts[t.name] || 0;
    const countBadge = count > 0
      ? `<span class="badge bg-secondary rounded-pill">${count}</span>`
      : `<span class="text-muted">—</span>`;
    return `<tr>
      <td class="ps-3"><code>${t.name}</code></td>
      <td class="text-muted">${t.description}</td>
      <td class="text-end pe-3">${countBadge}</td>
    </tr>`;
  }).join("");
}

function renderActivity(calls) {
  const tbody = document.getElementById("activity-body");

  if (!calls.length) {
    tbody.innerHTML = '<tr><td colspan="5" class="text-muted text-center py-3 ps-3">No calls yet</td></tr>';
    document.getElementById("error-count").style.display = "none";
    return;
  }

  const errorCount = calls.filter(c => c.error).length;
  const errBadge = document.getElementById("error-count");
  if (errorCount > 0) {
    errBadge.textContent = `${errorCount} error${errorCount > 1 ? "s" : ""}`;
    errBadge.style.display = "";
  } else {
    errBadge.style.display = "none";
  }

  tbody.innerHTML = [...calls].reverse().map(c => {
    const result = c.error
      ? `<span class="text-danger small">${c.error}</span>`
      : `<span class="text-success">${c.row_count ?? "—"} rows</span>`;
    const rowClass = c.error ? "table-error" : "";
    return `<tr class="${rowClass}">
      <td class="ps-3 text-muted small">${fmtTime(c.timestamp)}</td>
      <td><code>${c.tool_name}</code></td>
      <td class="text-muted small">${JSON.stringify(c.params)}</td>
      <td class="text-muted small">${c.duration_ms}ms</td>
      <td class="pe-3">${result}</td>
    </tr>`;
  }).join("");
}

async function refresh() {
  const badge = document.getElementById("refresh-badge");
  try {
    const res = await fetch("/api/status");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    const callCounts = {};
    data.recent_calls.forEach(c => {
      callCounts[c.tool_name] = (callCounts[c.tool_name] || 0) + 1;
    });

    renderStatus(data);
    renderTools(data.tools, callCounts);
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
