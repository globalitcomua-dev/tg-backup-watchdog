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
      --bg: #f6f8f7;
      --bg-accent: #eef7f1;
      --panel: #ffffff;
      --panel-soft: #fbfcfb;
      --ink: #111111;
      --muted: #66737b;
      --line: #dce6df;
      --accent: #39d130;
      --accent-strong: #1f8f24;
      --accent-soft: #ebfbeb;
      --ok: #1f9d57;
      --warn: #c68d11;
      --bad: #e45555;
      --unknown: #7e8b92;
      --shadow: 0 20px 46px rgba(17, 17, 17, .08);
      --radius: 24px;
    }
    * { box-sizing: border-box; }
    html, body { min-width: 1200px; }
    body {
      margin: 0;
      color: var(--ink);
      font-family: "Segoe UI", "Segoe UI Variable", Arial, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(57, 209, 48, .09), transparent 28%),
        radial-gradient(circle at top right, rgba(57, 209, 48, .06), transparent 22%),
        linear-gradient(180deg, #fbfcfb 0%, var(--bg) 100%);
    }
    button, input, select, textarea { font: inherit; }
    .shell {
      max-width: 1520px;
      margin: 0 auto;
      padding: 28px 24px 36px;
    }
    .hero, .panel, .modal-card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }
    .hero {
      padding: 28px;
      position: relative;
      overflow: hidden;
    }
    .hero::after {
      content: "";
      position: absolute;
      inset: auto -80px -80px auto;
      width: 220px;
      height: 220px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(57, 209, 48, .18), rgba(57, 209, 48, 0));
      pointer-events: none;
    }
    .hero-top, .toolbar, .panel-head, .title-line, .footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    .hero-copy { max-width: 920px; }
    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      background: var(--panel-soft);
      border: 1px solid var(--line);
      color: var(--accent-strong);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .12em;
      text-transform: uppercase;
    }
    h1, h2, h3, p { margin: 0; }
    .hero h1 {
      margin-top: 14px;
      font-size: 54px;
      line-height: 1.02;
      letter-spacing: -.04em;
    }
    .hero-subtitle {
      margin-top: 12px;
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 16px;
      line-height: 1.45;
      color: var(--muted);
    }
    .hero-actions { display: flex; gap: 12px; align-items: center; }
    .stats {
      margin-top: 24px;
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 16px;
    }
    .stat-card {
      padding: 18px;
      border-radius: 20px;
      border: 1px solid var(--line);
      background: linear-gradient(180deg, #ffffff 0%, #f9fbfa 100%);
    }
    .stat-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    .stat-value {
      display: block;
      margin-top: 8px;
      font-size: 34px;
      font-weight: 800;
      letter-spacing: -.04em;
    }
    .stat-note {
      display: block;
      margin-top: 8px;
      color: var(--muted);
      font-size: 13px;
    }
    .toolbar {
      margin-top: 20px;
      align-items: end;
      flex-wrap: wrap;
    }
    .toolbar-group {
      flex: 1 1 480px;
      display: grid;
      grid-template-columns: minmax(320px, 1.2fr) minmax(180px, .35fr);
      gap: 14px;
    }
    .toolbar-actions {
      display: flex;
      gap: 12px;
      align-items: center;
    }
    .field-block { min-width: 0; }
    .label {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    input, select, textarea, button {
      width: 100%;
      padding: 13px 14px;
      border-radius: 15px;
      border: 1px solid var(--line);
      background: #fff;
      color: var(--ink);
      min-width: 0;
    }
    textarea {
      resize: vertical;
      min-height: 96px;
    }
    input:focus, select:focus, textarea:focus, button:focus {
      outline: none;
      border-color: rgba(57, 209, 48, .6);
      box-shadow: 0 0 0 4px rgba(57, 209, 48, .12);
    }
    button {
      cursor: pointer;
      background: var(--accent);
      border-color: var(--accent);
      color: #ffffff;
      font-weight: 800;
      transition: transform .12s ease, box-shadow .12s ease, background .12s ease;
      white-space: nowrap;
    }
    button:hover { transform: translateY(-1px); box-shadow: 0 10px 22px rgba(57, 209, 48, .18); }
    button.secondary {
      background: #fff;
      color: var(--ink);
      border-color: #bfd8c3;
      box-shadow: none;
    }
    button.ghost {
      background: transparent;
      color: var(--muted);
      border-color: var(--line);
      box-shadow: none;
    }
    button.danger {
      background: #fff;
      color: var(--bad);
      border-color: #f0c0c0;
      box-shadow: none;
    }
    .notice {
      min-height: 24px;
      margin-top: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--accent-strong);
      font-size: 14px;
    }
    .page-stack {
      display: grid;
      gap: 20px;
      margin-top: 20px;
    }
    .panel {
      padding: 20px;
    }
    .panel-head {
      margin-bottom: 16px;
      align-items: start;
    }
    .panel-title {
      display: grid;
      gap: 8px;
    }
    .title-line h2 {
      font-size: 22px;
      letter-spacing: -.03em;
    }
    .inline-meta {
      display: flex;
      align-items: center;
      gap: 12px;
      color: var(--muted);
      font-size: 13px;
    }
    .panel-actions {
      display: flex;
      gap: 10px;
      align-items: center;
    }
    .hint-row {
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--muted);
      font-size: 14px;
      min-height: 22px;
    }
    .filter-bar {
      display: grid;
      grid-template-columns: minmax(280px, 1fr) 180px 180px;
      gap: 14px;
      margin-bottom: 14px;
    }
    .table-wrap {
      border: 1px solid var(--line);
      border-radius: 20px;
      overflow: hidden;
      background: #fff;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
      font-size: 14px;
    }
    th, td {
      padding: 16px 14px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }
    th {
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .08em;
      background: #fcfdfc;
    }
    tbody tr:hover { background: #fbfdfb; }
    tbody tr:last-child td { border-bottom: none; }
    .job-main {
      font-size: 18px;
      font-weight: 800;
      letter-spacing: -.03em;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .meta-row {
      margin-top: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .meta-pill, .engine-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      min-height: 28px;
      padding: 0 10px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #fff;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }
    .engine-chip {
      background: var(--accent-soft);
      color: #0f6e2c;
      border-color: #cbefcb;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 40px;
      padding: 6px 10px;
      border-radius: 999px;
      color: white;
      font-size: 12px;
      font-weight: 800;
      text-transform: lowercase;
    }
    .status-ok, .status-success { background: var(--ok); }
    .status-warning { background: var(--warn); }
    .status-failed, .status-missing { background: var(--bad); }
    .status-unknown { background: var(--unknown); }
    .metric-stack {
      display: grid;
      gap: 4px;
      color: var(--ink);
      white-space: nowrap;
    }
    .metric-sub { color: var(--muted); }
    .actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: nowrap;
      white-space: nowrap;
    }
    .actions button {
      width: auto;
      min-width: 0;
      padding: 11px 16px;
      flex: 0 0 auto;
    }
    .empty-state {
      padding: 28px 18px;
      text-align: center;
      color: var(--muted);
      background: #fbfcfb;
    }
    .detail-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }
    .detail-card {
      padding: 14px;
      border-radius: 18px;
      border: 1px solid var(--line);
      background: var(--panel-soft);
      min-width: 0;
    }
    .detail-card strong {
      display: block;
      margin-bottom: 6px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    .detail-card.full { grid-column: 1 / -1; }
    pre {
      margin: 0;
      padding: 14px;
      border-radius: 16px;
      border: 1px solid var(--line);
      background: #fff;
      white-space: pre-wrap;
      word-break: break-word;
      max-height: 320px;
      overflow: auto;
      font-size: 13px;
    }
    .footer {
      justify-content: center;
      margin-top: 24px;
      padding: 12px 0 0;
      color: var(--ink);
      font-size: 15px;
      font-weight: 800;
      letter-spacing: .04em;
    }
    .icon {
      width: 16px;
      height: 16px;
      display: inline-block;
      vertical-align: -3px;
      fill: currentColor;
    }
    .title-icon {
      width: 18px;
      height: 18px;
      fill: currentColor;
    }
    .info {
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 22px;
      height: 22px;
      padding: 0;
      border-radius: 50%;
      border: 1px solid var(--line);
      background: #fff;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      box-shadow: none;
      flex: 0 0 auto;
    }
    .info:hover { transform: none; box-shadow: none; }
    .info::after {
      content: attr(data-tooltip);
      position: absolute;
      left: 50%;
      bottom: calc(100% + 10px);
      transform: translateX(-50%);
      width: max-content;
      max-width: 320px;
      padding: 10px 12px;
      border-radius: 12px;
      background: #111111;
      color: #ffffff;
      font-size: 12px;
      line-height: 1.4;
      text-transform: none;
      letter-spacing: normal;
      font-weight: 600;
      white-space: normal;
      box-shadow: 0 12px 30px rgba(17, 17, 17, .2);
      opacity: 0;
      pointer-events: none;
      transition: opacity .12s ease, transform .12s ease;
    }
    .info:hover::after, .info:focus-visible::after {
      opacity: 1;
      transform: translateX(-50%) translateY(-2px);
    }
    .sync-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--ok);
      box-shadow: 0 0 0 0 rgba(31, 157, 87, .5);
      animation: pulse 1.8s infinite;
      flex: 0 0 auto;
    }
    .modal {
      position: fixed;
      inset: 0;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      background: rgba(17, 17, 17, .38);
      z-index: 40;
    }
    .modal.open { display: flex; }
    .modal-card {
      width: min(1120px, 100%);
      max-height: min(92vh, 1100px);
      overflow: auto;
      padding: 22px;
    }
    .modal-head {
      display: flex;
      align-items: start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 18px;
    }
    .modal-copy {
      display: grid;
      gap: 8px;
    }
    .modal-copy p {
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }
    .modal-close {
      width: auto;
      padding: 10px 14px;
    }
    .modal-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.4fr) minmax(360px, .9fr);
      gap: 18px;
    }
    .stack {
      display: grid;
      gap: 18px;
    }
    .subpanel {
      border: 1px solid var(--line);
      border-radius: 20px;
      padding: 18px;
      background: var(--panel-soft);
    }
    .subpanel h3 {
      margin-bottom: 12px;
      font-size: 18px;
      letter-spacing: -.02em;
    }
    .form-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    .form-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 16px;
    }
    .form-actions button {
      width: auto;
      min-width: 132px;
    }
    .producer-note {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }
    .token-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto auto;
      gap: 10px;
      align-items: end;
    }
    .token-row button {
      width: auto;
      min-width: 120px;
    }
    .producer-table td, .producer-table th { padding: 14px 12px; }
    .producer-table .actions { justify-content: flex-end; }
    .hidden { display: none !important; }
    @keyframes pulse {
      0% { box-shadow: 0 0 0 0 rgba(31, 157, 87, .35); }
      70% { box-shadow: 0 0 0 10px rgba(31, 157, 87, 0); }
      100% { box-shadow: 0 0 0 0 rgba(31, 157, 87, 0); }
    }
    @media (max-width: 1340px) {
      html, body { min-width: 1100px; }
      .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .detail-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .modal-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <div class="hero-top">
        <div class="hero-copy">
          <div class="eyebrow"><svg class="title-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l7 4v6c0 5.24-3.44 9.97-7 11-3.56-1.03-7-5.76-7-11V6l7-4zm0 4.18L7 8.73V12c0 3.97 2.39 7.9 5 8.93 2.61-1.03 5-4.96 5-8.93V8.73l-5-2.55zm-1 3.82h2v4h-2V10zm0 5h2v2h-2v-2z"/></svg>Operations Console</div>
          <h1>Backup Watchdog</h1>
          <div class="hero-subtitle">
            <span>Backup monitoring console for jobs, live state, and producer-managed report intake.</span>
            <button type="button" class="info" data-tooltip="The admin console manages tracked jobs, report producers, and the latest parsed backup state without requiring direct shell access to the host.">i</button>
          </div>
        </div>
        <div class="hero-actions">
          <button type="button" id="open-producers" class="secondary">Producers</button>
          <button type="button" id="open-create-job">+ Job</button>
        </div>
      </div>
      <div class="stats">
        <div class="stat-card">
          <div class="stat-head">Tracked Jobs <button type="button" class="info" data-tooltip="How many jobs are registered in the watchdog and participate in SLA checks.">i</button></div>
          <strong id="stat-tracked" class="stat-value">0</strong>
          <small id="stat-tracked-note" class="stat-note">No jobs loaded yet</small>
        </div>
        <div class="stat-card">
          <div class="stat-head">Need Attention <button type="button" class="info" data-tooltip="Jobs that are currently missing, warning, failed, or otherwise not green.">i</button></div>
          <strong id="stat-attention" class="stat-value">0</strong>
          <small id="stat-attention-note" class="stat-note">Everything looks green</small>
        </div>
        <div class="stat-card">
          <div class="stat-head">Untracked Runs <button type="button" class="info" data-tooltip="Recent reports that were parsed successfully but do not yet map to a tracked job definition.">i</button></div>
          <strong id="stat-untracked" class="stat-value">0</strong>
          <small id="stat-untracked-note" class="stat-note">No recent untracked reports</small>
        </div>
        <div class="stat-card">
          <div class="stat-head">Live Sync <button type="button" class="info" data-tooltip="Current auto-refresh cadence for the admin console.">i</button></div>
          <strong id="stat-refresh" class="stat-value">30s</strong>
          <small id="stat-refresh-note" class="stat-note">Auto refresh enabled</small>
        </div>
      </div>
      <div class="toolbar">
        <div class="toolbar-group">
          <div class="field-block">
            <label class="label" for="token">Admin API Token <button type="button" class="info" data-tooltip="Used only by the browser admin console and administrative API calls. Never place producer tokens here.">i</button></label>
            <input id="token" placeholder="Paste admin Bearer token">
          </div>
          <div class="field-block">
            <label class="label" for="auto-refresh-interval">Auto Refresh</label>
            <select id="auto-refresh-interval">
              <option value="15">Every 15s</option>
              <option value="30" selected>Every 30s</option>
              <option value="60">Every 60s</option>
              <option value="120">Every 2m</option>
              <option value="0">Paused</option>
            </select>
          </div>
        </div>
        <div class="toolbar-actions">
          <button id="save-token" class="secondary">Save Token</button>
          <button id="refresh-all">Sync Now</button>
        </div>
      </div>
      <div id="notice" class="notice"></div>
    </section>

    <div class="page-stack">
      <section class="panel">
        <div class="panel-head">
          <div class="panel-title">
            <div class="title-line">
              <h2>Tracked States</h2>
              <button type="button" class="info" data-tooltip="The company or job name is primary. Host and engine remain visible as compact metadata without cluttering the table.">i</button>
            </div>
            <div class="hint-row">
              <span class="sync-dot"></span>
              <span id="last-refresh-label">Waiting for first sync</span>
            </div>
          </div>
          <div class="panel-actions">
            <button type="button" id="header-open-create-job">+ Add Job</button>
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
        <div class="table-wrap">
          <table>
            <colgroup>
              <col style="width:28%">
              <col style="width:10%">
              <col style="width:10%">
              <col style="width:16%">
              <col style="width:16%">
              <col style="width:20%">
            </colgroup>
            <thead>
              <tr>
                <th>Company / Job</th>
                <th>Status</th>
                <th>SLA</th>
                <th>Last Run</th>
                <th>Changed</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="states-body"></tbody>
          </table>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <div class="panel-title">
            <div class="title-line">
              <h2>Untracked Recent Runs</h2>
              <button type="button" class="info" data-tooltip="Fresh reports that were ingested but are not yet linked to a tracked job definition.">i</button>
            </div>
          </div>
        </div>
        <div class="table-wrap">
          <table>
            <colgroup>
              <col style="width:34%">
              <col style="width:12%">
              <col style="width:18%">
              <col style="width:10%">
              <col style="width:26%">
            </colgroup>
            <thead>
              <tr>
                <th>Job</th>
                <th>Status</th>
                <th>When</th>
                <th>Errors</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="untracked-body"></tbody>
          </table>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <div class="panel-title">
            <div class="title-line">
              <h2>State Details</h2>
              <button type="button" class="info" data-tooltip="Select a tracked job to inspect the latest parsed backup details and raw payload.">i</button>
            </div>
          </div>
        </div>
        <div id="state-detail" class="hint-row">Select a tracked job to view more details.</div>
      </section>
    </div>

    <footer class="footer">Powered by Dmytro Shylenko</footer>
  </div>

  <div id="job-modal" class="modal" aria-hidden="true">
    <div class="modal-card">
      <div class="modal-head">
        <div class="modal-copy">
          <h2 id="form-title">Create Job</h2>
          <p>Register a tracked job or update an existing one. This modal is also opened directly from untracked reports.</p>
        </div>
        <button type="button" class="secondary modal-close" data-close-modal="job-modal">Close</button>
      </div>
      <div class="subpanel">
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
          <div class="form-actions">
            <button type="submit">Save Job</button>
            <button type="button" id="reset-form" class="secondary">Reset</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div id="producer-modal" class="modal" aria-hidden="true">
    <div class="modal-card">
      <div class="modal-head">
        <div class="modal-copy">
          <h2 id="producer-form-title">Manage Producers</h2>
          <p>Create report producers, rotate their tokens, and restrict each one to specific hosts and jobs.</p>
        </div>
        <button type="button" class="secondary modal-close" data-close-modal="producer-modal">Close</button>
      </div>
      <div class="modal-grid">
        <div class="stack">
          <div class="subpanel">
            <h3>Registered Producers</h3>
            <div class="table-wrap">
              <table class="producer-table">
                <colgroup>
                  <col style="width:21%">
                  <col style="width:19%">
                  <col style="width:19%">
                  <col style="width:12%">
                  <col style="width:13%">
                  <col style="width:16%">
                </colgroup>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Hosts</th>
                    <th>Jobs</th>
                    <th>Status</th>
                    <th>Updated</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody id="producers-body"></tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="stack">
          <div class="subpanel">
            <h3 id="producer-panel-title">Create Producer</h3>
            <p class="producer-note">Existing token values are not shown back from the server. To change one, generate or enter a new token and save the producer again.</p>
            <form id="producer-form">
              <input type="hidden" id="producer-id">
              <div class="form-grid">
                <div><label class="label" for="producer-name">Producer Name</label><input id="producer-name" required></div>
                <div><label class="label" for="producer-enabled">Enabled</label><select id="producer-enabled"><option value="true">Enabled</option><option value="false">Disabled</option></select></div>
              </div>
              <div style="margin-top:14px;">
                <label class="label" for="producer-token">Producer Token</label>
                <div class="token-row">
                  <input id="producer-token" placeholder="Generate or paste a producer token">
                  <button type="button" id="generate-producer-token" class="secondary">Generate</button>
                  <button type="button" id="copy-producer-token" class="secondary">Copy</button>
                </div>
              </div>
              <div class="form-grid" style="margin-top:14px;">
                <div><label class="label" for="producer-hosts">Allowed Hosts</label><input id="producer-hosts" placeholder="TopFace, BiColor"></div>
                <div><label class="label" for="producer-jobs">Allowed Jobs</label><input id="producer-jobs" placeholder="TopFace, BiColor-daily"></div>
              </div>
              <div style="margin-top:14px;">
                <label class="label" for="producer-description">Description</label>
                <textarea id="producer-description" placeholder="What this producer is used for"></textarea>
              </div>
              <div class="form-actions">
                <button type="submit">Save Producer</button>
                <button type="button" id="reset-producer-form" class="secondary">Reset</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const tokenInput = document.getElementById("token");
    const notice = document.getElementById("notice");
    const statesBody = document.getElementById("states-body");
    const untrackedBody = document.getElementById("untracked-body");
    const producersBody = document.getElementById("producers-body");
    const stateDetail = document.getElementById("state-detail");
    const form = document.getElementById("job-form");
    const formTitle = document.getElementById("form-title");
    const jobIdInput = document.getElementById("job-id");
    const producerForm = document.getElementById("producer-form");
    const producerIdInput = document.getElementById("producer-id");
    const producerPanelTitle = document.getElementById("producer-panel-title");
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
    const statUntrackedNote = document.getElementById("stat-untracked-note");
    const statRefresh = document.getElementById("stat-refresh");
    const statRefreshNote = document.getElementById("stat-refresh-note");
    const jobModal = document.getElementById("job-modal");
    const producerModal = document.getElementById("producer-modal");
    const producerFields = {
      producerName: document.getElementById("producer-name"),
      producerEnabled: document.getElementById("producer-enabled"),
      producerToken: document.getElementById("producer-token"),
      producerHosts: document.getElementById("producer-hosts"),
      producerJobs: document.getElementById("producer-jobs"),
      producerDescription: document.getElementById("producer-description"),
    };
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
    let producersCache = [];
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
      return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
    }

    function setNotice(message, isError = false) {
      notice.innerHTML = `${isError ? icon("spark") : icon("sync")}<span>${escapeHtml(message)}</span>`;
      notice.style.color = isError ? "#d64d4d" : "#1f8f24";
    }

    function openModal(modal) {
      modal.classList.add("open");
      modal.setAttribute("aria-hidden", "false");
    }

    function closeModal(modal) {
      modal.classList.remove("open");
      modal.setAttribute("aria-hidden", "true");
    }

    function statusBadge(status) {
      return `<span class="badge status-${escapeHtml(status)}">${escapeHtml(status)}</span>`;
    }

    function getHeaders() {
      const token = tokenInput.value.trim();
      if (!token) throw new Error("Admin API token is required.");
      return { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" };
    }

    async function apiFetch(path, options = {}) {
      const response = await fetch(path, { ...options, headers: { ...getHeaders(), ...(options.headers || {}) } });
      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `Request failed: ${response.status}`);
      }
      return response.json();
    }

    function formatDateTime(value) {
      if (!value) return "-";
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return value;
      return date.toLocaleString();
    }

    function formatDateParts(value) {
      if (!value) {
        return { date: "-", time: "-", raw: "-" };
      }
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) {
        return { date: value, time: "", raw: value };
      }
      return {
        date: date.toLocaleDateString(),
        time: date.toLocaleTimeString(),
        raw: date.toLocaleString(),
      };
    }

    function parseCsvList(value) {
      return value
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);
    }

    function renderCsvList(values) {
      return (values || []).length ? escapeHtml(values.join(", ")) : "Any";
    }

    function generateTokenValue() {
      const bytes = new Uint8Array(24);
      crypto.getRandomValues(bytes);
      const hex = Array.from(bytes, (item) => item.toString(16).padStart(2, "0")).join("");
      return `bw_prod_${hex}`;
    }

    async function copyText(value, successMessage) {
      if (!value) {
        setNotice("Nothing to copy yet.", true);
        return;
      }
      await navigator.clipboard.writeText(value);
      setNotice(successMessage);
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
      fields.host.value = job.host || "";
      fields.job.value = job.job || "";
      fields.engine.value = job.engine || "unknown";
      fields.expectedHours.value = job.expected_every_hours || 24;
      fields.deadline.value = job.deadline || "";
      fields.enabled.value = String(job.enabled ?? true);
      formTitle.textContent = job.id ? `Edit Job #${job.id}` : "Create Job";
      openModal(jobModal);
    }

    function resetProducerForm() {
      producerForm.reset();
      producerIdInput.value = "";
      producerPanelTitle.textContent = "Create Producer";
      producerFields.producerEnabled.value = "true";
      producerFields.producerToken.value = "";
    }

    function fillProducerForm(producer) {
      producerIdInput.value = producer.id;
      producerFields.producerName.value = producer.producer_name || "";
      producerFields.producerEnabled.value = String(producer.enabled);
      producerFields.producerToken.value = "";
      producerFields.producerHosts.value = (producer.allowed_hosts || []).join(", ");
      producerFields.producerJobs.value = (producer.allowed_jobs || []).join(", ");
      producerFields.producerDescription.value = producer.description || "";
      producerPanelTitle.textContent = `Edit Producer #${producer.id}`;
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
      const enabledCount = states.filter((item) => item.enabled !== false).length;
      statTracked.textContent = String(states.length);
      statTrackedNote.textContent = states.length ? `${enabledCount} enabled jobs` : "No jobs loaded yet";
      statAttention.textContent = String(needsAttention);
      statAttentionNote.textContent = needsAttention ? "Review non-green states" : "Everything looks green";
      statUntracked.textContent = String(runs.length);
      statUntrackedNote.textContent = runs.length ? "Recent reports waiting for promotion" : "No recent untracked reports";
    }

    function populateEngineFilter(states, runs) {
      const selected = engineFilter.value || "all";
      const engines = [...new Set([...states, ...runs].map((item) => item.engine || "unknown"))].sort();
      engineFilter.innerHTML = '<option value="all">All engines</option>' + engines.map((engine) => `<option value="${escapeHtml(engine)}">${escapeHtml(engine)}</option>`).join("");
      engineFilter.value = engines.includes(selected) ? selected : "all";
    }

    function renderDetail(detail) {
      if (!detail) {
        stateDetail.textContent = "Select a tracked job to view more details.";
        return;
      }
      const raw = detail.raw_json ? JSON.stringify(detail.raw_json, null, 2) : "No raw JSON captured.";
      stateDetail.innerHTML = `
        <div class="detail-grid">
          <div class="detail-card"><strong>Company / Job</strong>${escapeHtml(detail.job)}</div>
          <div class="detail-card"><strong>Host</strong>${escapeHtml(detail.host)}</div>
          <div class="detail-card"><strong>Engine</strong>${escapeHtml(detail.engine)}</div>
          <div class="detail-card"><strong>Status</strong>${statusBadge(detail.status)}</div>
          <div class="detail-card"><strong>Last Backup Status</strong>${escapeHtml(detail.last_backup_status || "-")}</div>
          <div class="detail-card"><strong>Expected Every Hours</strong>${escapeHtml(detail.expected_every_hours)}</div>
          <div class="detail-card"><strong>Deadline</strong>${escapeHtml(detail.deadline || "-")}</div>
          <div class="detail-card"><strong>Enabled</strong>${escapeHtml(detail.enabled)}</div>
          <div class="detail-card"><strong>Last Run At</strong>${escapeHtml(formatDateTime(detail.last_run_at))}</div>
          <div class="detail-card"><strong>Run Created At</strong>${escapeHtml(formatDateTime(detail.latest_run_created_at))}</div>
          <div class="detail-card"><strong>Age Hours</strong>${escapeHtml(detail.age_hours ?? "-")}</div>
          <div class="detail-card"><strong>Warnings / Errors</strong>${escapeHtml(detail.error_count ?? "-")}</div>
          <div class="detail-card"><strong>Duration Seconds</strong>${escapeHtml(detail.duration_seconds ?? "-")}</div>
          <div class="detail-card"><strong>Snapshot</strong>${escapeHtml(detail.snapshot_id || "-")}</div>
          <div class="detail-card"><strong>Destination</strong>${escapeHtml(detail.destination || "-")}</div>
          <div class="detail-card"><strong>Backup Type</strong>${escapeHtml(detail.backup_type || "-")}</div>
          <div class="detail-card full"><strong>Message</strong><pre>${escapeHtml(detail.message || "No message")}</pre></div>
          <div class="detail-card full"><strong>Raw JSON</strong><pre>${escapeHtml(raw)}</pre></div>
        </div>
      `;
    }

    async function deleteJob(jobId) {
      await apiFetch(`/api/v1/jobs/${jobId}`, { method: "DELETE" });
      setNotice(`Job #${jobId} deleted.`);
      closeModal(jobModal);
      resetForm();
      renderDetail(null);
      await refreshAll();
    }

    async function deleteRun(runId) {
      await apiFetch(`/api/v1/runs/${runId}`, { method: "DELETE" });
      setNotice(`Run #${runId} deleted.`);
      await refreshAll();
    }

    async function deleteProducer(producerId) {
      await apiFetch(`/api/v1/producers/${producerId}`, { method: "DELETE" });
      setNotice(`Producer #${producerId} deleted.`);
      resetProducerForm();
      await refreshProducers();
    }

    async function refreshProducers() {
      producersCache = await apiFetch("/api/v1/producers");
      renderProducers(producersCache);
    }

    function renderProducers(producers) {
      producersBody.innerHTML = "";
      if (!producers.length) {
        producersBody.innerHTML = `<tr><td colspan="6"><div class="empty-state">No producers created yet.</div></td></tr>`;
        return;
      }
      for (const producer of producers) {
        const updated = formatDateParts(producer.updated_at);
        const row = document.createElement("tr");
        row.innerHTML = `
          <td><strong>${escapeHtml(producer.producer_name)}</strong></td>
          <td>${renderCsvList(producer.allowed_hosts)}</td>
          <td>${renderCsvList(producer.allowed_jobs)}</td>
          <td>${statusBadge(producer.enabled ? "ok" : "warning")}</td>
          <td><div class="metric-stack"><span>${escapeHtml(updated.date)}</span><span class="metric-sub">${escapeHtml(updated.time)}</span></div></td>
          <td>
            <div class="actions">
              <button type="button" class="secondary producer-edit-btn">Edit</button>
              <button type="button" class="danger producer-delete-btn">Delete</button>
            </div>
          </td>
        `;
        row.querySelector(".producer-edit-btn").addEventListener("click", () => fillProducerForm(producer));
        row.querySelector(".producer-delete-btn").addEventListener("click", async () => {
          if (confirm(`Delete producer ${producer.producer_name}?`)) {
            await deleteProducer(producer.id);
          }
        });
        producersBody.appendChild(row);
      }
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
        const lastRun = formatDateParts(state.last_run_at);
        const changed = formatDateParts(state.last_changed_at);
        const notified = formatDateParts(state.last_notified_at);
        row.innerHTML = `
          <td>
            <div class="job-main">${escapeHtml(state.job)}</div>
            <div class="meta-row">
              <span class="meta-pill">${escapeHtml(state.host)}</span>
              <span class="engine-chip">${icon("monitor")}${escapeHtml(state.engine || "unknown")}</span>
              <button type="button" class="info" data-tooltip="Tracked backup job on host ${escapeHtml(state.host)}.">i</button>
            </div>
          </td>
          <td>${statusBadge(state.status)}</td>
          <td>
            <div class="metric-stack">
              <span>${escapeHtml(state.expected_every_hours)}h</span>
              <span class="metric-sub">${escapeHtml(state.deadline || "no deadline")}</span>
            </div>
          </td>
          <td>
            <div class="metric-stack">
              <span>${escapeHtml(lastRun.date)}</span>
              <span>${escapeHtml(lastRun.time)}</span>
              <span class="metric-sub">age: ${escapeHtml(state.age_hours ?? "-")}h</span>
            </div>
          </td>
          <td>
            <div class="metric-stack">
              <span>${escapeHtml(changed.date)}</span>
              <span>${escapeHtml(changed.time)}</span>
              <span class="metric-sub">notified: ${state.last_notified_at ? `${escapeHtml(notified.date)} ${escapeHtml(notified.time)}` : "-"}</span>
            </div>
          </td>
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
        const when = formatDateParts(run.finished_at || run.created_at);
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>
            <div class="job-main">${escapeHtml(run.job)}</div>
            <div class="meta-row">
              <span class="meta-pill">${escapeHtml(run.host)}</span>
              <span class="engine-chip">${icon("monitor")}${escapeHtml(run.engine || "unknown")}</span>
            </div>
          </td>
          <td>${statusBadge(run.status)}</td>
          <td><div class="metric-stack"><span>${escapeHtml(when.date)}</span><span>${escapeHtml(when.time)}</span></div></td>
          <td>${escapeHtml(run.error_count ?? "-")}</td>
          <td>
            <div class="actions">
              <button type="button" class="secondary track-btn">+ Add Job</button>
              <button type="button" class="danger delete-btn">Delete</button>
            </div>
          </td>
        `;
        row.querySelector(".track-btn").addEventListener("click", () => fillForm({
          host: run.host,
          job: run.job,
          engine: run.engine,
          expected_every_hours: 24,
          deadline: "",
          enabled: true,
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

    async function openProducerModal() {
      openModal(producerModal);
      resetProducerForm();
      try {
        await refreshProducers();
      } catch (error) {
        setNotice(error.message, true);
      }
    }

    document.getElementById("save-token").addEventListener("click", () => {
      localStorage.setItem("backup_watchdog_admin_token", tokenInput.value.trim());
      setNotice("Admin token saved in browser storage.");
    });

    document.getElementById("refresh-all").addEventListener("click", () => refreshAll());
    document.getElementById("open-producers").addEventListener("click", openProducerModal);
    document.getElementById("open-create-job").addEventListener("click", () => {
      resetForm();
      openModal(jobModal);
    });
    document.getElementById("header-open-create-job").addEventListener("click", () => {
      resetForm();
      openModal(jobModal);
    });

    document.querySelectorAll("[data-close-modal]").forEach((button) => {
      button.addEventListener("click", () => {
        closeModal(document.getElementById(button.dataset.closeModal));
      });
    });

    [jobModal, producerModal].forEach((modal) => {
      modal.addEventListener("click", (event) => {
        if (event.target === modal) {
          closeModal(modal);
        }
      });
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeModal(jobModal);
        closeModal(producerModal);
      }
    });

    document.getElementById("reset-form").addEventListener("click", resetForm);
    document.getElementById("reset-producer-form").addEventListener("click", resetProducerForm);
    document.getElementById("generate-producer-token").addEventListener("click", () => {
      producerFields.producerToken.value = generateTokenValue();
      setNotice("Producer token generated locally. Save the producer to register it.");
    });
    document.getElementById("copy-producer-token").addEventListener("click", async () => {
      await copyText(producerFields.producerToken.value.trim(), "Producer token copied.");
    });

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
        closeModal(jobModal);
        resetForm();
        await refreshAll();
      } catch (error) {
        setNotice(error.message, true);
      }
    });

    producerForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const producerId = producerIdInput.value.trim();
      const token = producerFields.producerToken.value.trim();
      const payload = {
        producer_name: producerFields.producerName.value.trim(),
        allowed_hosts: parseCsvList(producerFields.producerHosts.value),
        allowed_jobs: parseCsvList(producerFields.producerJobs.value),
        description: producerFields.producerDescription.value.trim() || null,
        enabled: producerFields.producerEnabled.value === "true",
      };

      if (!producerId || token) {
        payload.token = token;
      }

      if (!producerId && !token) {
        setNotice("Producer token is required when creating a producer.", true);
        return;
      }

      try {
        await apiFetch(producerId ? `/api/v1/producers/${producerId}` : "/api/v1/producers", {
          method: producerId ? "PUT" : "POST",
          body: JSON.stringify(payload),
        });
        setNotice(producerId ? "Producer updated." : "Producer created.");
        await refreshProducers();
        resetProducerForm();
      } catch (error) {
        setNotice(error.message, true);
      }
    });

    resetForm();
    resetProducerForm();
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
