/**
 * AutoForm Pro Max - Matrix Live Stream Terminal & Form Logs Explorer (Audit Trail)
 */

import { store } from '../store.js';

export class TerminalModule {
  constructor() {
    this.container = document.getElementById('view-terminal');
    this.viewMode = 'explorer'; // 'explorer' | 'stream'
    this.selectedFormSlug = 'sushi_survey';
    this.statusFilter = 'all';
    this.searchQuery = '';
    this.autoScroll = true;
    this.liveLogs = [];
    this.logSummary = { totalLogs: 0, byForm: {}, byStatus: {} };
    this.selectedEntry = null;
    this.pollTimer = null;
    
    // Fetch initial logs from backend
    this.fetchBackendLogs();
  }

  async fetchBackendLogs() {
    try {
      const url = `/api/logs?form=${encodeURIComponent(this.selectedFormSlug)}&status=${encodeURIComponent(this.statusFilter)}&limit=300`;
      const resp = await fetch(url);
      if (resp.ok) {
        const data = await resp.json();
        this.liveLogs = data.logs || [];
        this.logSummary = data.summary || this.logSummary;
        this.renderLogTable();
        this.updateKPIs();
      }
    } catch (e) {
      console.log("Using cached log stream");
    }
  }

  startPolling() {
    if (this.pollTimer) clearInterval(this.pollTimer);
    this.pollTimer = setInterval(() => {
      if (store.getState().activeTab === 'terminal') {
        this.fetchBackendLogs();
      }
    }, 2500);
  }

  render() {
    const state = store.getState();
    const streamLogs = state.logs;

    this.container.innerHTML = `
      <!-- Header Bar: View Mode Switcher + Live KPIs -->
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
        <div>
          <div style="display: flex; align-items: center; gap: 0.65rem;">
            <h2 style="font-family: var(--font-display); font-size: 1.3rem; font-weight: 700; color: var(--text-primary);">
              Form Execution Logs & Audit Trail
            </h2>
            <span class="badge badge-cyan" style="font-size: 0.7rem;"><span class="pulse-dot" style="width: 6px; height: 6px;"></span> LIVE DB LOGS</span>
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted);">
            บันทึกประวัติการยิง Request แยกตามแต่ละฟอร์ม ตรวจสอบ HTTP Status, Latency, Persona และ Payload ละเอียดย้อนหลัง
          </p>
        </div>

        <div style="display: flex; align-items: center; gap: 0.5rem; background: var(--bg-surface-2); padding: 0.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
          <button class="btn btn-sm ${this.viewMode === 'explorer' ? 'btn-primary' : 'btn-ghost'}" id="btn-mode-explorer" style="font-size: 0.75rem; padding: 0.35rem 0.75rem;">
            📋 Form Logs Explorer
          </button>
          <button class="btn btn-sm ${this.viewMode === 'stream' ? 'btn-primary' : 'btn-ghost'}" id="btn-mode-stream" style="font-size: 0.75rem; padding: 0.35rem 0.75rem;">
            ⚡ Live Terminal Stream
          </button>
        </div>
      </div>

      <!-- VIEW 1: Form Logs Explorer (Audit Trail) -->
      <div id="logs-view-explorer" style="display: ${this.viewMode === 'explorer' ? 'flex' : 'none'}; flex-direction: column; gap: 1rem;">
        
        <!-- Form Selector Chips -->
        <div class="logs-form-chips" style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
          <button class="form-chip ${this.selectedFormSlug === 'all' ? 'active' : ''}" data-form-slug="all">
            🌐 All Forms Combined
          </button>
          <button class="form-chip ${this.selectedFormSlug === 'sushi_survey' ? 'active' : ''}" data-form-slug="sushi_survey">
            🍣 ซูชิสายพาน (7Ps & พฤติกรรม)
          </button>
          <button class="form-chip ${this.selectedFormSlug === 'seagames_survey' ? 'active' : ''}" data-form-slug="seagames_survey">
            🏅 SEA Games 33
          </button>
          <button class="form-chip ${this.selectedFormSlug === 'fda_expo' ? 'active' : ''}" data-form-slug="fda_expo">
            💊 FDA Expo 2026
          </button>
          <button class="form-chip ${this.selectedFormSlug === 'registration_890' ? 'active' : ''}" data-form-slug="registration_890">
            📋 Batch 890 Records
          </button>
          <button class="form-chip ${this.selectedFormSlug === 'mall_survey' ? 'active' : ''}" data-form-slug="mall_survey">
            🏬 ความพึงพอใจศูนย์การค้า
          </button>
          <button class="form-chip ${this.selectedFormSlug === 'satisfaction_survey' ? 'active' : ''}" data-form-slug="satisfaction_survey">
            🌟 ความพึงพอใจผู้ใช้บริการ
          </button>
        </div>

        <!-- Filter & Search Toolbar -->
        <div class="card" style="padding: 0.85rem 1.25rem;">
          <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem;">
            
            <!-- Left: Status Filters -->
            <div style="display: flex; align-items: center; gap: 0.4rem;">
              <span style="font-size: 0.75rem; color: var(--text-dim); margin-right: 0.25rem;">STATUS:</span>
              <button class="btn btn-sm btn-ghost log-status-filter ${this.statusFilter === 'all' ? 'active' : ''}" data-status="all" style="font-size: 0.72rem; padding: 0.2rem 0.55rem;">
                ALL
              </button>
              <button class="btn btn-sm btn-ghost log-status-filter ${this.statusFilter === 'SUCCESS' ? 'active' : ''}" data-status="SUCCESS" style="font-size: 0.72rem; padding: 0.2rem 0.55rem; color: #34d399;">
                ✅ 200 OK
              </button>
              <button class="btn btn-sm btn-ghost log-status-filter ${this.statusFilter === 'RATE_LIMITED' ? 'active' : ''}" data-status="RATE_LIMITED" style="font-size: 0.72rem; padding: 0.2rem 0.55rem; color: #fbbf24;">
                ⚠️ 429 Retry
              </button>
              <button class="btn btn-sm btn-ghost log-status-filter ${this.statusFilter === 'FAILED' ? 'active' : ''}" data-status="FAILED" style="font-size: 0.72rem; padding: 0.2rem 0.55rem; color: #fb7185;">
                ❌ Errors
              </button>
            </div>

            <!-- Right: Search & Actions -->
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <div class="form-input-wrapper" style="width: 260px;">
                <input type="text" id="log-search-input" class="form-input" style="padding: 0.35rem 0.65rem; font-size: 0.78rem;" placeholder="Search logs (persona, batch, time)..." value="${this.searchQuery}">
              </div>
              <button class="btn btn-secondary btn-sm" id="btn-refresh-logs" title="Fetch fresh logs from disk">
                <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                Sync Logs
              </button>
              <button class="btn btn-primary btn-sm" id="btn-download-log-file">
                <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                Export .JSONL
              </button>
            </div>
          </div>
        </div>

        <!-- Log Entries Table & Detail Drawer Split View -->
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1rem;">
          
          <!-- Table Card -->
          <div class="card" style="padding: 0;">
            <div class="table-container" style="max-height: 520px; overflow-y: auto;">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Form Target</th>
                    <th>Persona / Respondent</th>
                    <th>Engine</th>
                    <th>Status</th>
                    <th>Latency</th>
                    <th>Details</th>
                  </tr>
                </thead>
                <tbody id="logs-table-body">
                  ${this.renderTableRows(this.liveLogs)}
                </tbody>
              </table>
            </div>
          </div>

          <!-- Log Detail Inspector Drawer -->
          <div class="card card-glow-indigo" style="padding: 1.25rem; display: flex; flex-direction: column; gap: 0.75rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border-subtle); padding-bottom: 0.65rem;">
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.1rem;">🔍</span>
                <h3 style="font-size: 0.95rem; font-weight: 700; color: var(--text-primary);">Payload & Timing Inspector</h3>
              </div>
              <span id="log-detail-badge" class="badge badge-indigo">Click a row to inspect</span>
            </div>

            <div id="log-detail-content" style="font-size: 0.78rem; display: flex; flex-direction: column; gap: 0.6rem;">
              <div style="color: var(--text-dim); text-align: center; padding: 2rem 1rem;">
                Select any log record from the table to view the full verified Google Form payload, token parameters, and latency metrics.
              </div>
            </div>
          </div>

        </div>

      </div>

      <!-- VIEW 2: Live Terminal Stream -->
      <div id="logs-view-stream" class="terminal-window" style="display: ${this.viewMode === 'stream' ? 'block' : 'none'};">
        <div class="terminal-header">
          <div class="terminal-controls">
            <div class="term-dot red"></div>
            <div class="term-dot yellow"></div>
            <div class="term-dot green"></div>
            <span class="terminal-title" style="margin-left: 0.5rem;">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              root@autoform-engine: ~/dispatch-stream [ASYNC-COROUTINES]
            </span>
          </div>

          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <label style="display: flex; align-items: center; gap: 0.35rem; font-size: 0.72rem; color: var(--text-muted); cursor: pointer;">
              <input type="checkbox" checked id="toggle-autoscroll">
              <span>Auto-scroll</span>
            </label>
            <button class="btn btn-secondary btn-sm" id="btn-clear-terminal" style="font-size: 0.7rem; padding: 0.25rem 0.6rem;">
              Clear
            </button>
          </div>
        </div>

        <div class="terminal-body" id="terminal-log-body">
          ${this.renderStreamLines(streamLogs)}
        </div>
      </div>
    `;

    this.bindEvents();
    this.startPolling();
    this.scrollToBottom();
  }

  renderTableRows(logs) {
    if (!logs || logs.length === 0) {
      return `<tr><td colspan="7">
        <div class="empty-state">
          <div class="empty-state-icon">📭</div>
          <div class="empty-state-title">ยังไม่มีข้อมูล Log</div>
          <div class="empty-state-desc">ยังไม่พบบันทึกการส่งสำหรับ <strong>${this.selectedFormSlug}</strong> ที่มีสถานะ <strong>${this.statusFilter}</strong> — ลอง Launch Campaign ก่อนครับ</div>
          <div class="empty-state-action">
            <button class="btn btn-secondary btn-sm" onclick="window.app.switchTab('dispatcher')">→ ไปที่ Dispatcher Runner</button>
          </div>
        </div>
      </td></tr>`;
    }

    const query = this.searchQuery.toLowerCase();
    const filtered = logs.filter(l => {
      if (!query) return true;
      return (
        (l.persona && l.persona.toLowerCase().includes(query)) ||
        (l.formName && l.formName.toLowerCase().includes(query)) ||
        (l.timestamp && l.timestamp.includes(query)) ||
        (l.details && l.details.toLowerCase().includes(query)) ||
        (l.id && l.id.toLowerCase().includes(query))
      );
    });

    return filtered.map(l => {
      const is200 = l.httpCode === 200 || l.status === 'SUCCESS';
      const is429 = l.httpCode === 429 || l.status === 'RATE_LIMITED';
      const badgeClass = is200 ? 'badge-success' : (is429 ? 'badge-warning' : 'badge-danger');
      const badgeText = is200 ? '200 OK' : (is429 ? '429 RETRY' : `ERR ${l.httpCode || 500}`);

      return `
        <tr class="log-row-item" data-log-id="${l.id}" style="cursor: pointer;">
          <td style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-dim);">${l.timestamp || '-'}</td>
          <td style="font-weight: 600; color: var(--text-primary); font-size: 0.75rem;">${l.formName || l.formSlug || 'Google Form'}</td>
          <td style="color: var(--accent-cyan); font-weight: 500;">${l.persona || 'Respondent'}</td>
          <td><span class="badge badge-indigo" style="font-size: 0.65rem;">${l.engine || 'HTTPX'}</span></td>
          <td><span class="badge ${badgeClass}" style="font-size: 0.65rem;">${badgeText}</span></td>
          <td style="font-family: var(--font-mono); color: #a5b4fc; font-size: 0.72rem;">${l.latencyMs || 250}ms</td>
          <td style="font-size: 0.72rem; color: var(--text-muted); max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${l.details || 'Submitted verified response'}</td>
        </tr>
      `;
    }).join('');
  }

  renderStreamLines(logs) {
    if (!logs || logs.length === 0) {
      return `<div style="color: var(--text-dim); text-align: center; padding: 2rem;">No stream events.</div>`;
    }
    return logs.map(l => `
      <div class="log-line">
        <span class="log-time">[${l.time}]</span>
        <span class="log-badge ${l.type}">${l.type.toUpperCase()}</span>
        <span class="log-msg">${l.msg}</span>
      </div>
    `).join('');
  }

  renderLogTable() {
    const tbody = document.getElementById('logs-table-body');
    if (tbody) {
      tbody.innerHTML = this.renderTableRows(this.liveLogs);
      this.bindRowClicks();
    }
  }

  updateKPIs() {
    // Update summary counters if elements exist
  }

  inspectLog(logEntry) {
    this.selectedEntry = logEntry;
    const badge = document.getElementById('log-detail-badge');
    const content = document.getElementById('log-detail-content');
    if (!badge || !content) return;

    badge.className = (logEntry.httpCode === 200 || logEntry.status === 'SUCCESS') ? 'badge badge-success' : 'badge badge-danger';
    badge.textContent = `ID: ${logEntry.id}`;

    content.innerHTML = `
      <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
        <span style="color: var(--text-dim);">Timestamp:</span>
        <span style="font-family: var(--font-mono); color: var(--text-primary); font-weight: 600;">${logEntry.timestamp}</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
        <span style="color: var(--text-dim);">Form Target:</span>
        <span style="color: var(--accent-cyan); font-weight: 600;">${logEntry.formName}</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
        <span style="color: var(--text-dim);">Persona Archetype:</span>
        <span style="color: #34d399; font-weight: 600;">${logEntry.persona}</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
        <span style="color: var(--text-dim);">Delivery Latency:</span>
        <span style="font-family: var(--font-mono); color: #c084fc; font-weight: 600;">${logEntry.latencyMs} ms (${logEntry.engine})</span>
      </div>

      <div style="margin-top: 0.4rem;">
        <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase;">Submitted Answers & Tokens Payload:</span>
        <pre style="background: var(--bg-space); padding: 0.75rem; border-radius: var(--radius-md); border: 1px solid var(--border-subtle); color: #38bdf8; font-family: var(--font-mono); font-size: 0.72rem; max-height: 220px; overflow-y: auto; margin-top: 0.25rem;">${JSON.stringify(logEntry.payload || { details: logEntry.details, status: logEntry.status, persona: logEntry.persona }, null, 2)}</pre>
      </div>
    `;
  }

  updateLogs(logs) {
    const body = document.getElementById('terminal-log-body');
    if (!body) return;
    body.innerHTML = this.renderStreamLines(logs);
    if (this.autoScroll) {
      this.scrollToBottom();
    }
  }

  scrollToBottom() {
    const body = document.getElementById('terminal-log-body');
    if (body) {
      body.scrollTop = body.scrollHeight;
    }
  }

  bindRowClicks() {
    this.container.querySelectorAll('.log-row-item').forEach(row => {
      row.addEventListener('click', () => {
        const logId = row.getAttribute('data-log-id');
        const found = this.liveLogs.find(l => l.id === logId);
        if (found) {
          this.inspectLog(found);
          this.container.querySelectorAll('.log-row-item').forEach(r => r.style.background = '');
          row.style.background = 'rgba(99, 102, 241, 0.15)';
        }
      });
    });
  }

  bindEvents() {
    // Mode Switchers
    const btnExp = this.container.querySelector('#btn-mode-explorer');
    const btnStream = this.container.querySelector('#btn-mode-stream');
    const viewExp = this.container.querySelector('#logs-view-explorer');
    const viewStream = this.container.querySelector('#logs-view-stream');

    if (btnExp && btnStream) {
      btnExp.addEventListener('click', () => {
        this.viewMode = 'explorer';
        btnExp.className = 'btn btn-sm btn-primary';
        btnStream.className = 'btn btn-sm btn-ghost';
        if (viewExp) viewExp.style.display = 'flex';
        if (viewStream) viewStream.style.display = 'none';
        this.fetchBackendLogs();
      });

      btnStream.addEventListener('click', () => {
        this.viewMode = 'stream';
        btnStream.className = 'btn btn-sm btn-primary';
        btnExp.className = 'btn btn-sm btn-ghost';
        if (viewExp) viewExp.style.display = 'none';
        if (viewStream) viewStream.style.display = 'block';
        this.scrollToBottom();
      });
    }

    // Form Chips
    this.container.querySelectorAll('.form-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        this.container.querySelectorAll('.form-chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        this.selectedFormSlug = chip.getAttribute('data-form-slug');
        this.fetchBackendLogs();
      });
    });

    // Status Filters
    this.container.querySelectorAll('.log-status-filter').forEach(btn => {
      btn.addEventListener('click', () => {
        this.container.querySelectorAll('.log-status-filter').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.statusFilter = btn.getAttribute('data-status');
        this.fetchBackendLogs();
      });
    });

    // Search Input
    const searchIn = this.container.querySelector('#log-search-input');
    if (searchIn) {
      searchIn.addEventListener('input', (e) => {
        this.searchQuery = e.target.value;
        this.renderLogTable();
      });
    }

    // Sync Button
    const btnSync = this.container.querySelector('#btn-refresh-logs');
    if (btnSync) {
      btnSync.addEventListener('click', () => {
        this.fetchBackendLogs();
        store.addLog("ok", `Synced logs from disk for [${this.selectedFormSlug}]`);
      });
    }

    // Download Log File Button
    const btnDown = this.container.querySelector('#btn-download-log-file');
    if (btnDown) {
      btnDown.addEventListener('click', () => {
        const url = `/api/download-log?form=${encodeURIComponent(this.selectedFormSlug)}&format=jsonl`;
        window.open(url, '_blank');
        store.addLog("ok", `Exported log file for [${this.selectedFormSlug}]`);
      });
    }

    // Clear Terminal Button
    const btnClear = this.container.querySelector('#btn-clear-terminal');
    if (btnClear) {
      btnClear.addEventListener('click', () => {
        store.clearLogs();
        this.updateLogs([]);
      });
    }

    // Auto-scroll toggle
    const toggleScroll = this.container.querySelector('#toggle-autoscroll');
    if (toggleScroll) {
      toggleScroll.addEventListener('change', (e) => {
        this.autoScroll = e.target.checked;
      });
    }

    this.bindRowClicks();
  }
}
