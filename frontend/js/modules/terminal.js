/**
 * AutoForm Pro Max - Matrix Live Stream Terminal
 */

import { store } from '../store.js';

export class TerminalModule {
  constructor() {
    this.container = document.getElementById('view-terminal');
    this.filterType = 'all';
    this.searchQuery = '';
    this.autoScroll = true;
  }

  render() {
    const logs = store.getState().logs;

    this.container.innerHTML = `
      <div class="terminal-window">
        <!-- Terminal Header -->
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
            <!-- Filter Pills -->
            <div style="display: flex; gap: 0.35rem;">
              <button class="btn btn-ghost btn-sm term-filter-btn active" data-filter="all" style="font-size: 0.7rem; padding: 0.2rem 0.5rem;">ALL</button>
              <button class="btn btn-ghost btn-sm term-filter-btn" data-filter="ok" style="font-size: 0.7rem; padding: 0.2rem 0.5rem; color: #34d399;">200 OK</button>
              <button class="btn btn-ghost btn-sm term-filter-btn" data-filter="retry" style="font-size: 0.7rem; padding: 0.2rem 0.5rem; color: #fbbf24;">429 RETRY</button>
              <button class="btn btn-ghost btn-sm term-filter-btn" data-filter="err" style="font-size: 0.7rem; padding: 0.2rem 0.5rem; color: #fb7185;">ERRORS</button>
            </div>

            <!-- Auto Scroll Toggle -->
            <label style="display: flex; align-items: center; gap: 0.35rem; font-size: 0.72rem; color: var(--text-muted); cursor: pointer;">
              <input type="checkbox" checked id="toggle-autoscroll">
              <span>Auto-scroll</span>
            </label>

            <!-- Clear Button -->
            <button class="btn btn-secondary btn-sm" id="btn-clear-terminal" style="font-size: 0.7rem; padding: 0.25rem 0.6rem;">
              Clear
            </button>
          </div>
        </div>

        <!-- Terminal Body -->
        <div class="terminal-body" id="terminal-log-body">
          ${this.renderLogLines(logs)}
        </div>
      </div>
    `;

    this.bindEvents();
    this.scrollToBottom();
  }

  renderLogLines(logs) {
    const filtered = logs.filter(l => {
      if (this.filterType !== 'all' && l.type !== this.filterType) return false;
      if (this.searchQuery && !l.msg.toLowerCase().includes(this.searchQuery.toLowerCase())) return false;
      return true;
    });

    if (filtered.length === 0) {
      return `<div style="color: var(--text-dim); text-align: center; padding: 2rem;">No logs matching current filter.</div>`;
    }

    return filtered.map(l => `
      <div class="log-line">
        <span class="log-time">[${l.time}]</span>
        <span class="log-badge ${l.type}">${l.type.toUpperCase()}</span>
        <span class="log-msg">${l.msg}</span>
      </div>
    `).join('');
  }

  updateLogs(logs) {
    const body = document.getElementById('terminal-log-body');
    if (!body) return;
    body.innerHTML = this.renderLogLines(logs);
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

  bindEvents() {
    this.container.querySelectorAll('.term-filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.container.querySelectorAll('.term-filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.filterType = btn.getAttribute('data-filter');
        this.updateLogs(store.getState().logs);
      });
    });

    const toggleScroll = this.container.querySelector('#toggle-autoscroll');
    if (toggleScroll) {
      toggleScroll.addEventListener('change', (e) => {
        this.autoScroll = e.target.checked;
      });
    }

    const btnClear = this.container.querySelector('#btn-clear-terminal');
    if (btnClear) {
      btnClear.addEventListener('click', () => {
        store.clearLogs();
        this.updateLogs([]);
      });
    }
  }
}
