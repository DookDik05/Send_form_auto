/**
 * AutoForm Pro Max - Analytics & Data Vault
 */

import { store } from '../store.js';

export class AnalyticsModule {
  constructor() {
    this.container = document.getElementById('view-analytics');
    this.searchQuery = '';
    this.selectedCampaign = 'registration_890';
  }

  render() {
    const mockRows = this.getMockDataRows();

    this.container.innerHTML = `
      <!-- Top Breakdown Cards -->
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem;">
        
        <div class="card card-glow-indigo">
          <div class="card-header">
            <h4 class="card-title" style="font-size: 0.9rem;">Satisfaction Rating Breakdown</h4>
            <span class="badge badge-success">85% Highly Satisfied</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 0.5rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
              <span>5 Stars (มากที่สุด)</span>
              <span style="font-weight: 700; color: #34d399;">85.4%</span>
            </div>
            <div class="stacked-dist-bar" style="margin: 0;">
              <div style="width: 85.4%; background: #10b981;"></div>
            </div>

            <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
              <span>4 Stars (มาก)</span>
              <span style="font-weight: 700; color: #38bdf8;">14.6%</span>
            </div>
            <div class="stacked-dist-bar" style="margin: 0;">
              <div style="width: 14.6%; background: #06b6d4;"></div>
            </div>
          </div>
        </div>

        <div class="card card-glow-cyan">
          <div class="card-header">
            <h4 class="card-title" style="font-size: 0.9rem;">Gender Demographic Ratio</h4>
            <span class="badge badge-cyan">Balanced 50/50</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 0.5rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
              <span>ชาย (Male)</span>
              <span style="font-weight: 700; color: #60a5fa;">48.2%</span>
            </div>
            <div class="stacked-dist-bar" style="margin: 0;">
              <div style="width: 48.2%; background: #3b82f6;"></div>
            </div>

            <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
              <span>หญิง (Female)</span>
              <span style="font-weight: 700; color: #f472b6;">47.8%</span>
            </div>
            <div class="stacked-dist-bar" style="margin: 0;">
              <div style="width: 47.8%; background: #ec4899;"></div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h4 class="card-title" style="font-size: 0.9rem;">Top Participant Provinces</h4>
            <span class="badge badge-indigo">Udon Thani Lead</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 0.4rem; font-size: 0.78rem;">
            <div style="display: flex; justify-content: space-between;">
              <span>1. อุดรธานี</span>
              <span style="font-family: var(--font-mono); font-weight: 700; color: var(--accent-cyan);">62.5%</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span>2. ขอนแก่น / หนองคาย</span>
              <span style="font-family: var(--font-mono); font-weight: 700; color: var(--text-secondary);">24.1%</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span>3. กรุงเทพฯ และอื่นๆ</span>
              <span style="font-family: var(--font-mono); font-weight: 700; color: var(--text-dim);">13.4%</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Main Data Table Card -->
      <div class="card">
        <div class="card-header">
          <div class="card-title-group">
            <div class="card-title-icon" style="background: rgba(99, 102, 241, 0.15); color: #a5b4fc;">
              <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            </div>
            <div>
              <h3 class="card-title">Submission Vault & CSV Exports</h3>
              <p class="card-subtitle">Explore raw form response payloads and generated synthetic entries</p>
            </div>
          </div>

          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <input type="text" class="form-input" id="table-search-input" placeholder="Search by name, phone, province..." style="width: 240px; padding: 0.45rem 0.75rem; font-size: 0.8rem;">
            <button class="btn btn-secondary btn-sm" id="btn-export-csv">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
              Export CSV
            </button>
            <button class="btn btn-primary btn-sm" id="btn-export-json">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/></svg>
              Export JSON
            </button>
          </div>
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Full Name (TH)</th>
                <th>Phone Number</th>
                <th>Province / Branch</th>
                <th>Demographics</th>
                <th>Satisfaction</th>
                <th>Timestamp</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="analytics-table-body">
              ${this.renderTableRows(mockRows)}
            </tbody>
          </table>
        </div>
      </div>
    `;

    this.bindEvents();
  }

  getMockDataRows() {
    return [
      { id: 1, name: "สมชาย ใจดี", phone: "081-492-1823", province: "อุดรธานี", demo: "คนไทย • 26-35 ปี", rating: "5 = มากที่สุด", time: "2026-01-23 11:41:18", status: "HTTP 200" },
      { id: 2, name: "สมหญิง ศรีสุข", phone: "089-123-4567", province: "ขอนแก่น", demo: "คนไทย • 18-25 ปี", rating: "5 = มากที่สุด", time: "2026-01-23 11:41:19", status: "HTTP 200" },
      { id: 3, name: "กิตติพงษ์ ทิพย์มณี", phone: "092-887-3102", province: "กรุงเทพมหานคร", demo: "คนไทย • 36-45 ปี", rating: "4 = มาก", time: "2026-01-23 11:41:21", status: "HTTP 200" },
      { id: 4, name: "ชลธิชา วงศ์สุวรรณ", phone: "061-948-2234", province: "อุดรธานี", demo: "คนไทย • 18-25 ปี", rating: "5 = มากที่สุด", time: "2026-01-23 11:41:22", status: "HTTP 200" },
      { id: 5, name: "อภิวัฒน์ สุนทร", phone: "094-551-0982", province: "หนองคาย", demo: "คนไทย • 26-35 ปี", rating: "5 = มากที่สุด", time: "2026-01-23 11:41:23", status: "HTTP 200" },
      { id: 6, name: "รัชนก นาคินทร์", phone: "086-773-1940", province: "อุดรธานี", demo: "คนไทย • 46-60 ปี", rating: "4 = มาก", time: "2026-01-23 11:41:25", status: "HTTP 200" },
      { id: 7, name: "ธีรภัทร ชัยประสิทธิ์", phone: "065-201-9483", province: "ขอนแก่น", demo: "คนไทย • 18-25 ปี", rating: "5 = มากที่สุด", time: "2026-01-23 11:41:26", status: "HTTP 200" }
    ];
  }

  renderTableRows(rows) {
    return rows.map(r => `
      <tr>
        <td style="font-family: var(--font-mono); color: var(--text-dim);">${r.id}</td>
        <td style="font-weight: 600; color: var(--text-primary);">${r.name}</td>
        <td style="font-family: var(--font-mono); color: var(--accent-cyan);">${r.phone}</td>
        <td>${r.province}</td>
        <td style="font-size: 0.78rem; color: var(--text-muted);">${r.demo}</td>
        <td><span class="badge badge-success" style="font-size: 0.7rem;">${r.rating}</span></td>
        <td style="font-size: 0.75rem; color: var(--text-dim);">${r.time}</td>
        <td><span class="badge badge-success">OK</span></td>
      </tr>
    `).join('');
  }

  bindEvents() {
    const btnCsv = this.container.querySelector('#btn-export-csv');
    if (btnCsv) {
      btnCsv.addEventListener('click', () => {
        const rows = this.getMockDataRows();
        const header = "ID,Name,Phone,Province,Demographics,Rating,Timestamp,Status\n";
        const csvContent = header + rows.map(r => `"${r.id}","${r.name}","${r.phone}","${r.province}","${r.demo}","${r.rating}","${r.time}","${r.status}"`).join('\n');
        
        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "submission_results_export.csv";
        a.click();
        store.addLog("ok", "Downloaded complete CSV results export: submission_results_export.csv");
      });
    }

    const searchInput = this.container.querySelector('#table-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const all = this.getMockDataRows();
        const filtered = all.filter(r => 
          r.name.toLowerCase().includes(query) || 
          r.phone.includes(query) || 
          r.province.toLowerCase().includes(query)
        );
        this.container.querySelector('#analytics-table-body').innerHTML = this.renderTableRows(filtered);
      });
    }
  }
}
