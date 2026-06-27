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
    :root { --bg:#f5efe3; --panel:#fffaf1; --ink:#21302f; --muted:#687574; --line:#d8cfbf; --accent:#0f766e; --accent2:#115e59; --ok:#2f855a; --warn:#b7791f; --bad:#c53030; --unknown:#4a5568; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: Georgia, "Times New Roman", serif; color:var(--ink); background:radial-gradient(circle at top left, rgba(15,118,110,.12), transparent 28%), linear-gradient(180deg,#f8f2e8 0%, var(--bg) 100%); }
    .shell { max-width:1200px; margin:0 auto; padding:24px; }
    .hero,.panel { background:var(--panel); border:1px solid var(--line); border-radius:18px; box-shadow:0 10px 30px rgba(33,48,47,.06); }
    .hero { padding:24px; margin-bottom:20px; }
    .hero h1,.panel h2 { margin:0 0 10px; }
    .hero h1 { font-size:36px; line-height:1; }
    .hero p,.hint,.muted { color:var(--muted); }
    .toolbar,.grid,.panel,.form-grid { display:grid; gap:16px; }
    .toolbar { grid-template-columns:1.3fr auto auto; align-items:end; margin-top:18px; }
    .grid { grid-template-columns:1.35fr 1fr; align-items:start; }
    .panel { padding:18px; }
    .label { display:block; margin-bottom:6px; color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.08em; }
    input,select,button { width:100%; padding:12px 14px; border-radius:12px; border:1px solid var(--line); background:white; color:var(--ink); font:inherit; }
    button { cursor:pointer; background:var(--accent); color:white; border-color:var(--accent); font-weight:700; }
    button.secondary { background:white; color:var(--accent2); border-color:var(--accent); }
    .form-grid { grid-template-columns:1fr 1fr; }
    table { width:100%; border-collapse:collapse; font-size:14px; }
    th,td { text-align:left; padding:10px 8px; border-bottom:1px solid var(--line); vertical-align:top; }
    th { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.08em; }
    .badge { display:inline-block; padding:4px 9px; border-radius:999px; font-size:12px; font-weight:700; color:white; }
    .status-ok,.status-success { background:var(--ok); }
    .status-warning { background:var(--warn); }
    .status-failed,.status-missing { background:var(--bad); }
    .status-unknown { background:var(--unknown); }
    .mono { font-family:Consolas, monospace; }
    .actions { display:flex; gap:8px; margin-top:12px; }
    .actions button { width:auto; }
    .notice { min-height:24px; color:var(--accent2); font-size:14px; }
    .danger { background:white; color:var(--bad); border-color:var(--bad); }
    .detail-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px 18px; }
    .detail-grid div { font-size:14px; }
    .detail-grid strong { display:block; margin-bottom:4px; font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); }
    pre { white-space:pre-wrap; word-break:break-word; background:white; border:1px solid var(--line); border-radius:12px; padding:12px; margin:0; font-size:13px; }
    @media (max-width:960px) { .grid,.toolbar,.form-grid { grid-template-columns:1fr; } }
  </style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <h1>Backup Watchdog</h1>
      <p>Register monitored jobs, review current states, and promote fresh Telegram/API reports into tracked jobs without shell access.</p>
      <div class="toolbar">
        <div>
          <label class="label" for="token">API Token</label>
          <input id="token" placeholder="Paste Bearer token">
        </div>
        <button id="save-token" class="secondary">Save Token</button>
        <button id="refresh-all">Refresh Data</button>
      </div>
      <div id="notice" class="notice"></div>
    </section>
    <section class="grid">
      <div class="panel">
        <h2>Tracked States</h2>
        <p class="hint">These jobs are actively monitored by the scheduler.</p>
        <table>
          <thead><tr><th>Job</th><th>Status</th><th>Expected</th><th>Last Run</th><th>Changed</th><th>Action</th></tr></thead>
          <tbody id="states-body"></tbody>
        </table>
      </div>
      <div class="panel">
        <h2 id="form-title">Create Job</h2>
        <p class="hint">Register a backup job so the scheduler can detect missing runs and state changes.</p>
        <form id="job-form">
          <input type="hidden" id="job-id">
          <div class="form-grid">
            <div><label class="label" for="host">Host</label><input id="host" required></div>
            <div><label class="label" for="job">Job</label><input id="job" required></div>
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
    </section>
    <section class="panel" style="margin-top:20px;">
      <h2>Untracked Recent Runs</h2>
      <p class="hint">Reports seen by the system but not yet promoted into monitored jobs.</p>
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
    const fields = {
      host: document.getElementById("host"),
      job: document.getElementById("job"),
      engine: document.getElementById("engine"),
      expectedHours: document.getElementById("expected-hours"),
      deadline: document.getElementById("deadline"),
      enabled: document.getElementById("enabled"),
    };
    tokenInput.value = localStorage.getItem("backup_watchdog_token") || "";
    function setNotice(message, isError = false) { notice.textContent = message; notice.style.color = isError ? "#c53030" : "#115e59"; }
    function statusBadge(status) { return `<span class="badge status-${status}">${status}</span>`; }
    function getHeaders() {
      const token = tokenInput.value.trim();
      if (!token) throw new Error("API token is required.");
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
    function renderDetail(detail) {
      if (!detail) {
        stateDetail.innerHTML = "Select a tracked job to view more details.";
        return;
      }
      const raw = detail.raw_json ? JSON.stringify(detail.raw_json, null, 2) : "No raw JSON captured.";
      stateDetail.innerHTML = `
        <div class="detail-grid">
          <div><strong>Host</strong>${detail.host}</div>
          <div><strong>Job</strong>${detail.job}</div>
          <div><strong>Engine</strong>${detail.engine}</div>
          <div><strong>Status</strong>${statusBadge(detail.status)}</div>
          <div><strong>Last Backup Status</strong>${detail.last_backup_status || "-"}</div>
          <div><strong>Expected Every Hours</strong>${detail.expected_every_hours}</div>
          <div><strong>Deadline</strong>${detail.deadline || "-"}</div>
          <div><strong>Enabled</strong>${detail.enabled}</div>
          <div><strong>Last Run At</strong>${detail.last_run_at || "-"}</div>
          <div><strong>Run Created At</strong>${detail.latest_run_created_at || "-"}</div>
          <div><strong>Age Hours</strong>${detail.age_hours ?? "-"}</div>
          <div><strong>Warnings/Errors</strong>${detail.error_count ?? "-"}</div>
          <div><strong>Duration Seconds</strong>${detail.duration_seconds ?? "-"}</div>
          <div><strong>Snapshot</strong>${detail.snapshot_id || "-"}</div>
          <div><strong>Destination</strong>${detail.destination || "-"}</div>
          <div><strong>Backup Type</strong>${detail.backup_type || "-"}</div>
          <div style="grid-column:1 / -1;"><strong>Message</strong><pre>${detail.message || "No message"}</pre></div>
          <div style="grid-column:1 / -1;"><strong>Raw JSON</strong><pre>${raw}</pre></div>
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
        statesBody.innerHTML = `<tr><td colspan="6" class="muted">No tracked jobs yet.</td></tr>`;
        return;
      }
      const jobs = await apiFetch("/api/v1/jobs");
      for (const state of states) {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td><strong>${state.host}</strong><br><span class="mono muted">${state.job}</span><br><span class="muted">${state.engine}</span></td>
          <td>${statusBadge(state.status)}</td>
          <td>${state.expected_every_hours}h<br><span class="muted">${state.deadline || "no deadline"}</span></td>
          <td>${state.last_run_at || "never"}<br><span class="muted">age: ${state.age_hours ?? "-"}</span></td>
          <td>${state.last_changed_at || "-"}<br><span class="muted">notified: ${state.last_notified_at || "-"}</span></td>
          <td>
            <div class="actions">
              <button type="button" class="secondary edit-btn">Edit</button>
              <button type="button" class="secondary detail-btn">Details</button>
              <button type="button" class="danger delete-btn">Delete</button>
            </div>
          </td>
        `;
        row.querySelector(".edit-btn").addEventListener("click", () => {
          const job = jobs.find((item) => item.host === state.host && item.job === state.job);
          if (job) fillForm(job);
        });
        row.querySelector(".detail-btn").addEventListener("click", async () => {
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
        untrackedBody.innerHTML = `<tr><td colspan="5" class="muted">No untracked runs right now.</td></tr>`;
        return;
      }
      for (const run of runs) {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td><strong>${run.host}</strong><br><span class="mono muted">${run.job}</span></td>
          <td>${statusBadge(run.status)}</td>
          <td>${run.finished_at || run.created_at}</td>
          <td>${run.error_count ?? "-"}</td>
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
    async function refreshAll() {
      try {
        setNotice("Refreshing data...");
        const [states, untracked] = await Promise.all([apiFetch("/api/v1/states"), apiFetch("/api/v1/runs/untracked")]);
        await renderStates(states);
        renderUntracked(untracked);
        setNotice("Data refreshed.");
      } catch (error) {
        setNotice(error.message, true);
      }
    }
    document.getElementById("save-token").addEventListener("click", () => {
      localStorage.setItem("backup_watchdog_token", tokenInput.value.trim());
      setNotice("Token saved in browser storage.");
    });
    document.getElementById("refresh-all").addEventListener("click", refreshAll);
    document.getElementById("reset-form").addEventListener("click", resetForm);
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
  </script>
</body>
</html>
"""


@router.get("/admin", response_class=HTMLResponse)
def admin_page():
    return ADMIN_HTML
