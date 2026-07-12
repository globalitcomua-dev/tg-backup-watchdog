from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["admin"])


ADMIN_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Backup Watchdog Admin</title>
  <style>
    :root {
      --bg:#edf4f7;
      --bg-accent:#d9eef2;
      --panel:rgba(255,255,255,.88);
      --panel-strong:#ffffff;
      --ink:#10212b;
      --muted:#59707e;
      --line:rgba(120,148,160,.24);
      --accent:#0b7a75;
      --accent-strong:#085f5b;
      --accent-soft:#dbf4f1;
      --ok:#228b5d;
      --warn:#c38a17;
      --bad:#c24646;
      --unknown:#567082;
      --shadow:0 18px 44px rgba(15, 35, 45, .10);
      --radius:22px;
    }
    * { box-sizing: border-box; }
    body {
      margin:0;
      color:var(--ink);
      font-family:"Segoe UI", "Segoe UI Variable", "Helvetica Neue", Arial, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(11,122,117,.20), transparent 26%),
        radial-gradient(circle at top right, rgba(33,114,188,.12), transparent 24%),
        linear-gradient(180deg, #f7fbfc 0%, var(--bg) 100%);
    }
    .shell { max-width:1380px; margin:0 auto; padding:28px 24px 40px; }
    .hero,.panel {
      background:var(--panel);
      border:1px solid var(--line);
      border-radius:var(--radius);
      box-shadow:var(--shadow);
      backdrop-filter:blur(12px);
    }
    .hero { padding:28px; margin-bottom:20px; overflow:hidden; position:relative; }
    .hero::after {
      content:"";
      position:absolute;
      inset:auto -80px -90px auto;
      width:240px;
      height:240px;
      border-radius:50%;
      background:radial-gradient(circle, rgba(11,122,117,.18), rgba(11,122,117,0));
      pointer-events:none;
    }
    .hero h1,.panel h2,.panel h3 { margin:0; }
    .hero-copy { max-width:840px; }
    .eyebrow {
      display:inline-flex;
      align-items:center;
      gap:8px;
      margin-bottom:12px;
      padding:7px 12px;
      border-radius:999px;
      background:rgba(255,255,255,.72);
      border:1px solid var(--line);
      color:var(--accent-strong);
      font-size:12px;
      font-weight:700;
      letter-spacing:.12em;
      text-transform:uppercase;
    }
    .hero h1 { font-size:42px; line-height:1.05; letter-spacing:-.03em; }
    .hero p,.hint,.muted { color:var(--muted); }
    .hero p { margin:12px 0 0; max-width:780px; font-size:16px; line-height:1.55; }
    .powered-by {
      margin-top:10px;
      font-size:13px;
      color:var(--accent-strong);
      font-weight:700;
      letter-spacing:.03em;
    }
    .stats,.toolbar,.grid,.panel,.form-grid,.panel-stack,.filter-bar { display:grid; gap:16px; }
    .stats { grid-template-columns:repeat(4, minmax(0, 1fr)); margin-top:22px; }
    .stat-card {
      padding:16px 18px;
      border-radius:18px;
      background:linear-gradient(180deg, rgba(255,255,255,.96), rgba(245,251,252,.84));
      border:1px solid var(--line);
    }
    .stat-card span {
      display:block;
      color:var(--muted);
      font-size:12px;
      font-weight:700;
      text-transform:uppercase;
      letter-spacing:.08em;
    }
    .stat-card strong { display:block; margin-top:6px; font-size:30px; letter-spacing:-.03em; }
    .stat-card small { display:block; margin-top:6px; color:var(--muted); font-size:13px; }
    .toolbar { grid-template-columns:minmax(280px, 1.35fr) repeat(3, minmax(140px, auto)); align-items:end; margin-top:20px; }
    .grid { grid-template-columns:minmax(0, 1.7fr) minmax(320px, .9fr); align-items:start; }
    .panel { padding:20px; }
    .panel-header {
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:12px;
      margin-bottom:14px;
    }
    .panel-title p { margin:8px 0 0; }
    .panel-stack { grid-template-columns:1fr; }
    .label { display:block; margin-bottom:7px; color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.08em; font-weight:700; }
    input,select,button {
      width:100%;
      padding:13px 14px;
      border-radius:14px;
      border:1px solid var(--line);
      background:var(--panel-strong);
      color:var(--ink);
      font:inherit;
    }
    input:focus,select:focus,button:focus {
      outline:none;
      border-color:rgba(11,122,117,.55);
      box-shadow:0 0 0 4px rgba(11,122,117,.12);
    }
    button {
      cursor:pointer;
      background:var(--accent);
      color:white;
      border-color:var(--accent);
      font-weight:700;
      transition:transform .12s ease, box-shadow .12s ease, background .12s ease;
    }
    button:hover { transform:translateY(-1px); box-shadow:0 8px 18px rgba(11,122,117,.18); }
    button.secondary { background:var(--panel-strong); color:var(--accent-strong); border-color:rgba(11,122,117,.32); }
    button.ghost { background:transparent; color:var(--muted); border-color:var(--line); }
    .form-grid { grid-template-columns:1fr 1fr; }
    .filter-bar { grid-template-columns:minmax(180px, 1fr) 180px 180px; margin-bottom:12px; }
    table { width:100%; border-collapse:collapse; font-size:14px; }
    th,td { text-align:left; padding:12px 8px; border-bottom:1px solid var(--line); vertical-align:top; }
    th { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.08em; }
    tbody tr:hover { background:rgba(255,255,255,.45); }
    .badge { display:inline-flex; align-items:center; gap:6px; padding:5px 10px; border-radius:999px; font-size:12px; font-weight:800; color:white; }
    .status-ok,.status-success { background:var(--ok); }
    .status-warning { background:var(--warn); }
    .status-failed,.status-missing { background:var(--bad); }
    .status-unknown { background:var(--unknown); }
    .mono { font-family:Consolas, "Courier New", monospace; }
    .job-main { font-size:17px; font-weight:800; letter-spacing:-.02em; }
    .job-meta { margin-top:4px; font-size:13px; color:var(--muted); }
    .host-meta { margin-top:2px; font-size:12px; color:#8398a3; }
    .engine-chip {
      display:inline-flex;
      align-items:center;
      gap:6px;
      margin-top:8px;
      padding:4px 9px;
      border-radius:999px;
      background:var(--accent-soft);
      color:var(--accent-strong);
      font-size:12px;
      font-weight:700;
    }
    .actions { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
    .actions button { width:auto; }
    .notice {
      min-height:24px;
      color:var(--accent-strong);
      font-size:14px;
      display:flex;
      align-items:center;
      gap:8px;
      margin-top:12px;
    }
    .danger { background:var(--panel-strong); color:var(--bad); border-color:rgba(194,70,70,.4); }
    .detail-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px 18px; }
    .detail-grid div { font-size:14px; }
    .detail-grid strong { display:block; margin-bottom:5px; font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); }
    pre {
      white-space:pre-wrap;
      word-break:break-word;
      background:rgba(245,250,251,.82);
      border:1px solid var(--line);
      border-radius:16px;
      padding:14px;
      margin:0;
      font-size:13px;
      max-height:320px;
      overflow:auto;
    }
    .sync-dot {
      width:10px;
      height:10px;
      border-radius:50%;
      background:var(--ok);
      box-shadow:0 0 0 0 rgba(34,139,93,.6);
      animation:pulse 1.8s infinite;
    }
    .inline-meta { display:flex; flex-wrap:wrap; gap:10px; color:var(--muted); font-size:13px; }
    .empty-state {
      padding:20px 12px;
      text-align:center;
      color:var(--muted);
      background:rgba(255,255,255,.42);
      border:1px dashed var(--line);
      border-radius:18px;
    }
    .icon {
      width:16px;
      height:16px;
      display:inline-block;
      vertical-align:-3px;
      fill:currentColor;
    }
    .title-icon {
      width:18px;
      height:18px;
      fill:currentColor;
    }
    @keyframes pulse {
      0% { box-shadow:0 0 0 0 rgba(34,139,93,.35); }
      70% { box-shadow:0 0 0 10px rgba(34,139,93,0); }
      100% { box-shadow:0 0 0 0 rgba(34,139,93,0); }
    }
    @media (max-width:1120px) {
      .grid,.toolbar,.stats,.filter-bar,.form-grid { grid-template-columns:1fr; }
      .panel-header { flex-direction:column; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <div class="hero-copy">
        <div class="eyebrow"><svg class="title-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l7 4v6c0 5.24-3.44 9.97-7 11-3.56-1.03-7-5.76-7-11V6l7-4zm0 4.18L7 8.73V12c0 3.97 2.39 7.9 5 8.93 2.61-1.03 5-4.96 5-8.93V8.73l-5-2.55zm-1 3.82h2v4h-2V10zm0 5h2v2h-2v-2z"/></svg>Operations Console</div>
        <h1>Backup Watchdog</h1>
        <p>Register monitored jobs, watch live backup health, and promote fresh Telegram/API reports into tracked jobs without shell access.</p>
        <div class="powered-by">Powered by Dmytro Shylenko</div>
      </div>
      <div class="stats">
        <div class="stat-card"><span>Tracked Jobs</span><strong id="stat-tracked">0</strong><small id="stat-tracked-note">No jobs loaded yet</small></div>
        <div class="stat-card"><span>Need Attention</span><strong id="stat-attention">0</strong><small id="stat-attention-note">Warnings and missing backups</small></div>
        <div class="stat-card"><span>Untracked Runs</span><strong id="stat-untracked">0</strong><small id="stat-untracked-note">Recent reports waiting for promotion</small></div>
        <div class="stat-card"><span>Live Sync</span><strong id="stat-refresh">30s</strong><small id="stat-refresh-note">Auto refresh enabled</small></div>
      </div>
      <div class="toolbar">
        <div>
          <label class="label" for="token">Admin API Token</label>
          <input id="token" placeholder="Paste admin Bearer token">
        </div>
        <div>
          <label class="label" for="auto-refresh-interval">Auto Refresh</label>
          <select id="auto-refresh-interval">
            <option value="15">Every 15s</option>
            <option value="30" selected>Every 30s</option>
            <option value="60">Every 60s</option>
            <option value="120">Every 2m</option>
            <option value="0">Paused</option>
          </select>
        </div>
        <button id="save-token" class="secondary">Save Token</button>
        <button id="refresh-all">Sync Now</button>
      </div>
      <div id="notice" class="notice"></div>
    </section>
    <section class="grid">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <h2>Tracked States</h2>
            <p class="hint">Company/job name is the primary label. Host is kept secondary so the table stays easier to scan.</p>
          </div>
          <div class="inline-meta">
            <span><span class="sync-dot"></span> Auto sync active</span>
            <span id="last-refresh-label">Waiting for first sync</span>
          </div>
        </div>
        <div class="filter-bar">
          <div>
            <label class="label" for="state-search">Search</label>
            <input id="state-search" placeholder="Find company, host, or engine">
          </div>
          <div>
            <label class="label" for="status-filter">Status</label>
            <select id="status-filter">
              <option value="all">All statuses</option>
              <option value="missing">Missing</option>
              <option value="failed">Failed</option>
              <option value="warning">Warning</option>
              <option value="ok">OK</option>
              <option value="unknown">Unknown</option>
            </select>
          </div>
          <div>
            <label class="label" for="engine-filter">Engine</label>
            <select id="engine-filter">
              <option value="all">All engines</option>
            </select>
          </div>
        </div>
        <table>
          <thead><tr><th>Company / Job</th><th>Status</th><th>SLA</th><th>Last Run</th><th>Changed</th><th>Action</th></tr></thead>
          <tbody id="states-body"></tbody>
        </table>
      </div>
      <div class="panel-stack">
        <div class="panel">
          <h2 id="form-title">Create Job</h2>
          <p class="hint">Register a backup job so the scheduler can detect missing runs and state changes.</p>
          <form id="job-form">
            <input type="hidden" id="job-id">
            <div class="form-grid">
              <div><label class="label" for="host">Host</label><input id="host" required></div>
              <div><label class="label" for="job">Company / Job Name</label><input id="job" required></div>
              <div><label class="label" for="engine">Engine</label><input id="engine" value="unknown" required></div>
              <div><label class="label" for="expected-hours">Every Hours</label><input id="expected-hours" type="number" min="1" value="24" required></div>
              <div><label class="label" for="deadline">Deadline</label><input id="deadline" placeholder="03:00"></div>
              <div><label class="label" for="enabled">Enabled</label><select id="enabled"><option value="true">Enabled</option><option value="false">Disabled</option></select></div>
            </div>
            <div class="actions">
              <button type="submit">Save Job</button>
              <button type="button" id="reset-form" class="secondary">Reset</button>
            </div>
          </form>
        </div>
        <div class="panel">
          <h3>Suggested Next Extensions</h3>
          <div class="detail-grid">
            <div><strong>Quiet Hours</strong>Mute repeat alerts per job until a chosen time window expires.</div>
            <div><strong>Status History</strong>Show the last 10 state transitions so you can see flapping jobs.</div>
            <div><strong>Ownership</strong>Add owner/contact fields per job for faster incident routing.</div>
            <div><strong>Tags</strong>Filter by client, environment, or backup type without renaming jobs.</div>
          </div>
        </div>
      </div>
    </section>
    <section class="panel" style="margin-top:20px;">
      <div class="panel-header">
        <div class="panel-title">
          <h2>Untracked Recent Runs</h2>
          <p class="hint">Fresh reports seen by the system but not yet promoted into monitored jobs.</p>
        </div>
      </div>
      <table>
        <thead><tr><th>Job</th><th>Status</th><th>When</th><th>Errors</th><th>Action</th></tr></thead>
        <tbody id="untracked-body"></tbody>
      </table>
    </section>
    <section class="panel" style="margin-top:20px;">
      <h2>State Details</h2>
      <p class="hint">Click a tracked state to inspect the latest parsed backup data.</p>
      <div id="state-detail" class="muted">Select a tracked job to view more details.</div>
    </section>
  </div>
  <script>
    const tokenInput = document.getElementById("token");
    const notice = document.getElementById("notice");
    const statesBody = document.getElementById("states-body");
    const untrackedBody = document.getElementById("untracked-body");
    const stateDetail = document.getElementById("state-detail");
    const form = document.getElementById("job-form");
    const formTitle = document.getElementById("form-title");
    const jobIdInput = document.getElementById("job-id");
    const stateSearchInput = document.getElementById("state-search");
    const statusFilter = document.getElementById("status-filter");
    const engineFilter = document.getElementById("engine-filter");
    const autoRefreshInterval = document.getElementById("auto-refresh-interval");
    const lastRefreshLabel = document.getElementById("last-refresh-label");
    const statTracked = document.getElementById("stat-tracked");
    const statTrackedNote = document.getElementById("stat-tracked-note");
    const statAttention = document.getElementById("stat-attention");
    const statAttentionNote = document.getElementById("stat-attention-note");
    const statUntracked = document.getElementById("stat-untracked");
    const statRefresh = document.getElementById("stat-refresh");
    const statRefreshNote = document.getElementById("stat-refresh-note");
    const fields = {
      host: document.getElementById("host"),
      job: document.getElementById("job"),
      engine: document.getElementById("engine"),
      expectedHours: document.getElementById("expected-hours"),
      deadline: document.getElementById("deadline"),
      enabled: document.getElementById("enabled"),
    };
    let jobsCache = [];
    let statesCache = [];
    let untrackedCache = [];
    let selectedStateJobId = null;
    let refreshTimer = null;
    tokenInput.value = localStorage.getItem("backup_watchdog_admin_token") || "";
    autoRefreshInterval.value = localStorage.getItem("backup_watchdog_refresh_interval") || "30";
    function icon(name) {
      const icons = {
        monitor: '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-6v2h3v2H7v-2h3v-2H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2zm0 2v9h16V7H4z"/></svg>',
        sync: '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 6V3L8 7l4 4V8c2.76 0 5 2.24 5 5a5 5 0 0 1-8.66 3.54l-1.42 1.42A7 7 0 0 0 19 13c0-3.87-3.13-7-7-7zm-5 5a5 5 0 0 1 8.66-3.54l1.42-1.42A7 7 0 0 0 5 11c0 3.87 3.13 7 7 7v3l4-4-4-4v3c-2.76 0-5-2.24-5-5z"/></svg>',
        spark: '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M13 2l1.8 5.2L20 9l-5.2 1.8L13 16l-1.8-5.2L6 9l5.2-1.8L13 2zm-7 11l1.2 3.8L11 18l-3.8 1.2L6 23l-1.2-3.8L1 18l3.8-1.2L6 13zm12 1l.9 2.6L21 17l-2.1.4L18 20l-.9-2.6L15 17l2.1-.4L18 14z"/></svg>',
      };
      return icons[name] || "";
    }
    function escapeHtml(value) {
      return String(value ?? "").replace(/[&<>\"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
    }
    function setNotice(message, isError = false) {
      notice.innerHTML = `${isError ? icon("spark") : icon("sync")}<span>${escapeHtml(message)}</span>`;
      notice.style.color = isError ? "#c24646" : "#085f5b";
    }
    function statusBadge(status) { return `<span class="badge status-${escapeHtml(status)}">${escapeHtml(status)}</span>`; }
    function getHeaders() {
      const token = tokenInput.value.trim();
      if (!token) throw new Error("Admin API token is required.");
      return { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" };
    }
    async function apiFetch(path, options = {}) {
      const response = await fetch(path, { ...options, headers: { ...getHeaders(), ...(options.headers || {}) } });
      if (!response.ok) throw new Error(await response.text() || `Request failed: ${response.status}`);
      return response.json();
    }
    function resetForm() {
      form.reset();
      jobIdInput.value = "";
      fields.engine.value = "unknown";
      fields.expectedHours.value = "24";
      fields.enabled.value = "true";
      formTitle.textContent = "Create Job";
    }
    function fillForm(job) {
      jobIdInput.value = job.id || "";
      fields.host.value = job.host;
      fields.job.value = job.job;
      fields.engine.value = job.engine;
      fields.expectedHours.value = job.expected_every_hours;
      fields.deadline.value = job.deadline || "";
      fields.enabled.value = String(job.enabled);
      formTitle.textContent = job.id ? `Edit Job #${job.id}` : "Create Job";
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    function formatDateTime(value) {
      if (!value) return "-";
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return value;
      return date.toLocaleString();
    }
    function updateRefreshCadenceLabel() {
      const seconds = Number(autoRefreshInterval.value);
      statRefresh.textContent = seconds ? `${seconds}s` : "Paused";
      statRefreshNote.textContent = seconds ? "Auto refresh enabled" : "Background syncing paused";
    }
    function scheduleAutoRefresh() {
      localStorage.setItem("backup_watchdog_refresh_interval", autoRefreshInterval.value);
      updateRefreshCadenceLabel();
      if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
      }
      const seconds = Number(autoRefreshInterval.value);
      if (!seconds) {
        setNotice("Auto refresh paused. Manual sync still available.");
        return;
      }
      refreshTimer = setInterval(() => {
        refreshAll({ silent: true });
      }, seconds * 1000);
    }
    function updateStats(states, runs) {
      const needsAttention = states.filter((item) => !["ok", "success"].includes(item.status)).length;
      statTracked.textContent = String(states.length);
      statTrackedNote.textContent = states.length ? `${states.filter((item) => item.enabled !== false).length} enabled jobs` : "No jobs loaded yet";
      statAttention.textContent = String(needsAttention);
      statAttentionNote.textContent = needsAttention ? "Review missing, warning, and failed jobs" : "Everything looks green";
      statUntracked.textContent = String(runs.length);
    }
    function populateEngineFilter(states, runs) {
      const selected = engineFilter.value || "all";
      const engines = [...new Set([...states, ...runs].map((item) => item.engine || "unknown"))].sort();
      engineFilter.innerHTML = '<option value="all">All engines</option>' + engines.map((engine) => `<option value="${escapeHtml(engine)}">${escapeHtml(engine)}</option>`).join("");
      engineFilter.value = engines.includes(selected) ? selected : "all";
    }
    function renderDetail(detail) {
      if (!detail) {
        stateDetail.innerHTML = "Select a tracked job to view more details.";
        return;
      }
      const raw = detail.raw_json ? JSON.stringify(detail.raw_json, null, 2) : "No raw JSON captured.";
      stateDetail.innerHTML = `
        <div class="detail-grid">
          <div><strong>Company / Job</strong>${escapeHtml(detail.job)}</div>
          <div><strong>Host</strong>${escapeHtml(detail.host)}</div>
          <div><strong>Engine</strong>${escapeHtml(detail.engine)}</div>
          <div><strong>Status</strong>${statusBadge(detail.status)}</div>
          <div><strong>Last Backup Status</strong>${escapeHtml(detail.last_backup_status || "-")}</div>
          <div><strong>Expected Every Hours</strong>${escapeHtml(detail.expected_every_hours)}</div>
          <div><strong>Deadline</strong>${escapeHtml(detail.deadline || "-")}</div>
          <div><strong>Enabled</strong>${escapeHtml(detail.enabled)}</div>
          <div><strong>Last Run At</strong>${escapeHtml(formatDateTime(detail.last_run_at))}</div>
          <div><strong>Run Created At</strong>${escapeHtml(formatDateTime(detail.latest_run_created_at))}</div>
          <div><strong>Age Hours</strong>${escapeHtml(detail.age_hours ?? "-")}</div>
          <div><strong>Warnings/Errors</strong>${escapeHtml(detail.error_count ?? "-")}</div>
          <div><strong>Duration Seconds</strong>${escapeHtml(detail.duration_seconds ?? "-")}</div>
          <div><strong>Snapshot</strong>${escapeHtml(detail.snapshot_id || "-")}</div>
          <div><strong>Destination</strong>${escapeHtml(detail.destination || "-")}</div>
          <div><strong>Backup Type</strong>${escapeHtml(detail.backup_type || "-")}</div>
          <div style="grid-column:1 / -1;"><strong>Message</strong><pre>${escapeHtml(detail.message || "No message")}</pre></div>
          <div style="grid-column:1 / -1;"><strong>Raw JSON</strong><pre>${escapeHtml(raw)}</pre></div>
        </div>
      `;
    }
    async function deleteJob(jobId) {
      await apiFetch(`/api/v1/jobs/${jobId}`, { method: "DELETE" });
      setNotice(`Job #${jobId} deleted.`);
      resetForm();
      renderDetail(null);
      await refreshAll();
    }
    async function deleteRun(runId) {
      await apiFetch(`/api/v1/runs/${runId}`, { method: "DELETE" });
      setNotice(`Run #${runId} deleted.`);
      await refreshAll();
    }
    async function renderStates(states) {
      statesBody.innerHTML = "";
      if (!states.length) {
        statesBody.innerHTML = `<tr><td colspan="6"><div class="empty-state">No tracked jobs yet.</div></td></tr>`;
        return;
      }
      const normalizedSearch = stateSearchInput.value.trim().toLowerCase();
      const filteredStates = states
        .filter((state) => {
          const statusMatch = statusFilter.value === "all" || state.status === statusFilter.value;
          const engineMatch = engineFilter.value === "all" || (state.engine || "unknown") === engineFilter.value;
          const haystack = `${state.job} ${state.host} ${state.engine}`.toLowerCase();
          const textMatch = !normalizedSearch || haystack.includes(normalizedSearch);
          return statusMatch && engineMatch && textMatch;
        })
        .sort((left, right) => {
          const weight = { missing: 0, failed: 1, warning: 2, unknown: 3, ok: 4, success: 4 };
          return (weight[left.status] ?? 9) - (weight[right.status] ?? 9);
        });
      if (!filteredStates.length) {
        statesBody.innerHTML = `<tr><td colspan="6"><div class="empty-state">Nothing matches the current filters.</div></td></tr>`;
        return;
      }
      for (const state of filteredStates) {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>
            <div class="job-main">${escapeHtml(state.job)}</div>
            <div class="job-meta">Tracked backup job</div>
            <div class="host-meta">Host: ${escapeHtml(state.host)}</div>
            <div class="engine-chip">${icon("monitor")}${escapeHtml(state.engine)}</div>
          </td>
          <td>${statusBadge(state.status)}</td>
          <td>${escapeHtml(state.expected_every_hours)}h<br><span class="muted">${escapeHtml(state.deadline || "no deadline")}</span></td>
          <td>${escapeHtml(formatDateTime(state.last_run_at || "never"))}<br><span class="muted">age: ${escapeHtml(state.age_hours ?? "-")}h</span></td>
          <td>${escapeHtml(formatDateTime(state.last_changed_at || "-"))}<br><span class="muted">notified: ${escapeHtml(formatDateTime(state.last_notified_at || "-"))}</span></td>
          <td>
            <div class="actions">
              <button type="button" class="secondary edit-btn">Edit</button>
              <button type="button" class="secondary detail-btn">Details</button>
              <button type="button" class="danger delete-btn">Delete</button>
            </div>
          </td>
        `;
        row.querySelector(".edit-btn").addEventListener("click", () => {
          const job = jobsCache.find((item) => item.host === state.host && item.job === state.job);
          if (job) fillForm(job);
        });
        row.querySelector(".detail-btn").addEventListener("click", async () => {
          selectedStateJobId = state.job_id;
          const detail = await apiFetch(`/api/v1/states/${state.job_id}`);
          renderDetail(detail);
        });
        row.querySelector(".delete-btn").addEventListener("click", async () => {
          if (confirm(`Delete tracked job ${state.host}/${state.job}?`)) {
            await deleteJob(state.job_id);
          }
        });
        statesBody.appendChild(row);
      }
    }
    function renderUntracked(runs) {
      untrackedBody.innerHTML = "";
      if (!runs.length) {
        untrackedBody.innerHTML = `<tr><td colspan="5"><div class="empty-state">No untracked runs right now.</div></td></tr>`;
        return;
      }
      for (const run of runs) {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td><strong>${escapeHtml(run.job)}</strong><br><span class="host-meta">Host: ${escapeHtml(run.host)}</span><br><span class="engine-chip">${icon("monitor")}${escapeHtml(run.engine || "unknown")}</span></td>
          <td>${statusBadge(run.status)}</td>
          <td>${escapeHtml(formatDateTime(run.finished_at || run.created_at))}</td>
          <td>${escapeHtml(run.error_count ?? "-")}</td>
          <td>
            <div class="actions">
              <button type="button" class="secondary track-btn">Track</button>
              <button type="button" class="danger delete-btn">Delete</button>
            </div>
          </td>
        `;
        row.querySelector(".track-btn").addEventListener("click", () => fillForm({
          host: run.host, job: run.job, engine: run.engine, expected_every_hours: 24, deadline: "", enabled: true,
        }));
        row.querySelector(".delete-btn").addEventListener("click", async () => {
          if (confirm(`Delete untracked run #${run.id} (${run.host}/${run.job})?`)) {
            await deleteRun(run.id);
          }
        });
        untrackedBody.appendChild(row);
      }
    }
    async function refreshAll(options = {}) {
      try {
        if (!options.silent) setNotice("Refreshing data...");
        const [jobs, states, untracked] = await Promise.all([
          apiFetch("/api/v1/jobs"),
          apiFetch("/api/v1/states"),
          apiFetch("/api/v1/runs/untracked"),
        ]);
        jobsCache = jobs;
        statesCache = states;
        untrackedCache = untracked;
        updateStats(statesCache, untrackedCache);
        populateEngineFilter(statesCache, untrackedCache);
        await renderStates(statesCache);
        renderUntracked(untrackedCache);
        if (selectedStateJobId) {
          const stillExists = statesCache.some((state) => state.job_id === selectedStateJobId);
          if (stillExists) {
            const detail = await apiFetch(`/api/v1/states/${selectedStateJobId}`);
            renderDetail(detail);
          } else {
            selectedStateJobId = null;
            renderDetail(null);
          }
        }
        lastRefreshLabel.textContent = `Last synced: ${new Date().toLocaleTimeString()}`;
        if (!options.silent) setNotice("Data refreshed.");
      } catch (error) {
        setNotice(error.message, true);
      }
    }
    document.getElementById("save-token").addEventListener("click", () => {
      localStorage.setItem("backup_watchdog_admin_token", tokenInput.value.trim());
      setNotice("Admin token saved in browser storage.");
    });
    document.getElementById("refresh-all").addEventListener("click", refreshAll);
    document.getElementById("reset-form").addEventListener("click", resetForm);
    autoRefreshInterval.addEventListener("change", scheduleAutoRefresh);
    stateSearchInput.addEventListener("input", () => renderStates(statesCache));
    statusFilter.addEventListener("change", () => renderStates(statesCache));
    engineFilter.addEventListener("change", () => renderStates(statesCache));
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = {
        host: fields.host.value.trim(),
        job: fields.job.value.trim(),
        engine: fields.engine.value.trim(),
        expected_every_hours: Number(fields.expectedHours.value),
        deadline: fields.deadline.value.trim() || null,
        enabled: fields.enabled.value === "true",
      };
      try {
        const jobId = jobIdInput.value.trim();
        await apiFetch(jobId ? `/api/v1/jobs/${jobId}` : "/api/v1/jobs", {
          method: jobId ? "PUT" : "POST",
          body: JSON.stringify(payload),
        });
        setNotice(jobId ? "Job updated." : "Job created.");
        resetForm();
        await refreshAll();
      } catch (error) {
        setNotice(error.message, true);
      }
    });
    resetForm();
    updateRefreshCadenceLabel();
    scheduleAutoRefresh();
    refreshAll();
  </script>
</body>
</html>
"""


@router.get("/admin", response_class=HTMLResponse)
def admin_page():
    return ADMIN_HTML
