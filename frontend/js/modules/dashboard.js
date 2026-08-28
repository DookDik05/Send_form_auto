/**
 * AutoForm Pro Max - Dashboard Module
 * Real-time KPI counters, animated SVG throughput charts, quick launch presets
 */

import { store } from '../store.js';
import { CAMPAIGN_PRESETS } from '../data/presets.js';

export class DashboardModule {
  constructor() {
    this.container = document.getElementById('view-dashboard');
    this.initChart();
  }

  render() {
    const state = store.getState();
    const successRate = state.totalSubmissions > 0 
      ? ((state.totalSuccess / state.totalSubmissions) * 100).toFixed(1) 
      : "100.0";

    this.container.innerHTML = `
      <!-- Top Metrics Row -->
      <div class="metrics-grid">
        <div class="metric-card card-glow-indigo">
          <div class="metric-top">
            <span class="metric-label">Total Submissions</span>
            <div class="metric-icon-box" style="background: rgba(99, 102, 241, 0.15); color: #818cf8;">
              <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            </div>
          </div>
          <div class="metric-val-group">
            <span class="metric-value" id="kpi-total-subs">${state.totalSubmissions.toLocaleString()}</span>
            <span class="metric-unit">forms</span>
          </div>
          <div class="metric-trend up">
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 10l7-7m0 0l7 7m-7-7v18"/></svg>
            <span>+12.4% vs last week</span>
          </div>
        </div>

        <div class="metric-card card-glow-emerald">
          <div class="metric-top">
            <span class="metric-label">Success Rate</span>
            <div class="metric-icon-box" style="background: rgba(16, 185, 129, 0.15); color: #34d399;">
              <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
          </div>
          <div class="metric-val-group">
            <span class="metric-value" id="kpi-success-rate">${successRate}%</span>
            <span class="metric-unit">HTTP 200/302</span>
          </div>
          <div class="metric-trend up">
            <span>Optimal 99.4% Delivery</span>
          </div>
        </div>

        <div class="metric-card card-glow-cyan">
          <div class="metric-top">
            <span class="metric-label">Live Throughput</span>
            <div class="metric-icon-box" style="background: rgba(6, 182, 212, 0.15); color: #22d3ee;">
              <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
          </div>
          <div class="metric-val-group">
            <span class="metric-value" id="kpi-current-rps">${state.currentRPS}</span>
            <span class="metric-unit">req / sec</span>
          </div>
          <div class="metric-trend" style="color: var(--accent-cyan)">
            <span>Avg Latency: ${state.avgLatencyMs}ms</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-top">
            <span class="metric-label">Worker Pool</span>
            <div class="metric-icon-box" style="background: rgba(168, 85, 247, 0.15); color: #c084fc;">
              <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
            </div>
          </div>
          <div class="metric-val-group">
            <span class="metric-value" id="kpi-active-workers">${state.activeWorkers} / 50</span>
            <span class="metric-unit">async coroutines</span>
          </div>
          <div class="metric-trend" style="color: var(--text-dim)">
            <span>Proxy Rotation: Ready</span>
          </div>
        </div>
      </div>

      <!-- Real-time Throughput Chart & Quick Presets Grid -->
      <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem;">
        <!-- Animated Live Chart Card -->
        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <div class="card-title-icon">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/></svg>
              </div>
              <div>
                <h3 class="card-title">Live Dispatch Telemetry</h3>
                <p class="card-subtitle">Real-time throughput velocity & submission waveform</p>
              </div>
            </div>
            <div style="display: flex; gap: 0.5rem;">
              <span class="badge badge-cyan"><span class="pulse-dot" style="width: 6px; height: 6px;"></span> LIVE FEED</span>
            </div>
          </div>

          <div style="position: relative; height: 180px; width: 100%; margin-top: 0.5rem;">
            <svg id="throughput-chart-svg" width="100%" height="100%" viewBox="0 0 500 180" preserveAspectRatio="none" style="overflow: visible;">
              <defs>
                <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#6366f1" stop-opacity="0.45"/>
                  <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.0"/>
                </linearGradient>
              </defs>
              <!-- Grid Lines -->
              <line x1="0" y1="45" x2="500" y2="45" stroke="rgba(255,255,255,0.05)" stroke-dasharray="4"/>
              <line x1="0" y1="90" x2="500" y2="90" stroke="rgba(255,255,255,0.05)" stroke-dasharray="4"/>
              <line x1="0" y1="135" x2="500" y2="135" stroke="rgba(255,255,255,0.05)" stroke-dasharray="4"/>
              
              <!-- Area & Path -->
              <path id="chart-area-path" d="" fill="url(#chartGradient)" />
              <path id="chart-line-path" d="" fill="none" stroke="#06b6d4" stroke-width="2.5" stroke-linecap="round" />
            </svg>
          </div>
        </div>

        <!-- Quick Launch Presets -->
        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <div class="card-title-icon" style="background: rgba(6, 182, 212, 0.15); color: #22d3ee;">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              </div>
              <div>
                <h3 class="card-title">Campaign Presets</h3>
                <p class="card-subtitle">Ready-to-launch form configurations</p>
              </div>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.65rem;">
            ${CAMPAIGN_PRESETS.map(preset => `
              <div class="preset-item-card" data-preset-id="${preset.id}" style="
                padding: 0.75rem; 
                background: var(--bg-surface-2); 
                border: 1px solid var(--border-subtle); 
                border-radius: var(--radius-md); 
                cursor: pointer;
                transition: all var(--transition-fast);
                display: flex;
                align-items: center;
                justify-content: space-between;
              ">
                <div style="display: flex; flex-direction: column; gap: 0.2rem;">
                  <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-weight: 600; font-size: 0.85rem; color: var(--text-primary);">${preset.title}</span>
                    <span class="badge ${preset.mode === 'selenium' ? 'badge-warning' : 'badge-indigo'}" style="font-size: 0.65rem;">
                      ${preset.mode === 'selenium' ? 'SELENIUM' : 'HTTPX'}
                    </span>
                  </div>
                  <span style="font-size: 0.72rem; color: var(--text-dim);">${preset.subtitle}</span>
                </div>
                <button class="btn btn-secondary btn-sm preset-launch-btn" data-preset-id="${preset.id}">
                  Select
                </button>
              </div>
            `).join('')}
          </div>
        </div>
      </div>

      <!-- Recent Missions Table Card -->
      <div class="card">
        <div class="card-header">
          <div class="card-title-group">
            <div class="card-title-icon" style="background: rgba(16, 185, 129, 0.15); color: #34d399;">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <div>
              <h3 class="card-title">Recent Automation Runs</h3>
              <p class="card-subtitle">Historical batch execution logs and deliverability stats</p>
            </div>
          </div>
          <button class="btn btn-ghost btn-sm" id="btn-view-all-history">
            View All in Vault →
          </button>
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Run ID</th>
                <th>Campaign Name</th>
                <th>Execution Date</th>
                <th>Volume</th>
                <th>Success</th>
                <th>Engine</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              ${state.historyRecords.map(rec => `
                <tr>
                  <td><span style="font-family: var(--font-mono); color: var(--accent-cyan);">${rec.id}</span></td>
                  <td style="font-weight: 600; color: var(--text-primary);">${rec.name}</td>
                  <td>${rec.date}</td>
                  <td>${rec.count.toLocaleString()}</td>
                  <td><span style="color: var(--color-success); font-weight: 600;">${rec.success} (${((rec.success / rec.count) * 100).toFixed(0)}%)</span></td>
                  <td><span class="badge badge-indigo">${rec.engine}</span></td>
                  <td><span class="badge badge-success">${rec.status}</span></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    this.bindEvents();
    this.updateChartPath();
  }

  bindEvents() {
    this.container.querySelectorAll('.preset-item-card, .preset-launch-btn').forEach(el => {
      el.addEventListener('click', (e) => {
        const id = el.getAttribute('data-preset-id');
        if (id) {
          store.selectPreset(id);
          window.app.switchTab('dispatcher');
        }
      });
    });

    const btnHistory = this.container.querySelector('#btn-view-all-history');
    if (btnHistory) {
      btnHistory.addEventListener('click', () => {
        window.app.switchTab('analytics');
      });
    }
  }

  initChart() {
    setInterval(() => {
      const state = store.getState();
      const currentRPS = state.currentRPS;
      const history = [...state.throughputHistory.slice(1), currentRPS > 0 ? currentRPS : Math.floor(10 + Math.random() * 15)];
      store.setState({ throughputHistory: history });
      this.updateChartPath();
    }, 1500);
  }

  updateChartPath() {
    const linePath = document.getElementById('chart-line-path');
    const areaPath = document.getElementById('chart-area-path');
    if (!linePath || !areaPath) return;

    const data = store.getState().throughputHistory;
    const width = 500;
    const height = 160;
    const maxVal = Math.max(...data, 100);
    
    const step = width / (data.length - 1);
    let points = [];
    
    for (let i = 0; i < data.length; i++) {
      const x = i * step;
      const y = height - (data[i] / maxVal) * (height - 20);
      points.push({ x, y });
    }

    if (points.length === 0) return;

    let pathD = `M ${points[0].x} ${points[0].y}`;
    for (let i = 1; i < points.length; i++) {
      pathD += ` L ${points[i].x} ${points[i].y}`;
    }

    linePath.setAttribute('d', pathD);
    areaPath.setAttribute('d', `${pathD} L ${width} ${height} L 0 ${height} Z`);
  }
}
