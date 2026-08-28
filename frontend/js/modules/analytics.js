/**
 * AutoForm Pro Max - Analytics & Per-Form History Vault
 */

import { store } from '../store.js';

export class AnalyticsModule {
  constructor() {
    this.container = document.getElementById('view-analytics');
    this.selectedFormId = 'all';
    this.searchQuery = '';
    
    // Detailed Per-Form Historical Catalog
    this.formCatalog = [
      {
        id: "sushi-conveyor",
        formId: "1FAIpQLSfVCqzAoQZkyfPxRpkme_HV_7I_ZcoZxXjODZiAIQm8wcakBw",
        name: "แบบสอบถามร้านซูชิสายพาน (7Ps & พฤติกรรม)",
        icon: "🍣",
        totalSent: 107,
        successCount: 107,
        failedCount: 0,
        successRate: "100.0%",
        runsCount: 3,
        lastRun: "2026-08-28 10:26",
        primaryEngine: "Selenium & HTTPX Async",
        color: "#f43f5e",
        csvFiles: [
          { name: "sushi_survey_results_20260828_101951.csv", count: 3, size: "1.8 KB", date: "2026-08-28 10:19" },
          { name: "sushi_survey_results_20260828_101043.csv", count: 3, size: "1.8 KB", date: "2026-08-28 10:10" }
        ],
        rows: [
          { id: 1, name: "Super Fan (Sushi Lover)", phone: "081-948-2234", province: "กรุงเทพฯ", rating: "5 = มากที่สุด (80%)", time: "2026-08-28 10:26:05", status: "HTTP 200 (Selenium)" },
          { id: 2, name: "Satisfied Pragmatist", phone: "086-773-1940", province: "นนทบุรี", rating: "5 = มากที่สุด (85%)", time: "2026-08-28 10:19:51", status: "HTTP 200 (HTTPX)" },
          { id: 3, name: "Super Fan (Sushi Lover)", phone: "092-887-3102", province: "กรุงเทพฯ", rating: "5 = มากที่สุด (90%)", time: "2026-08-28 10:19:50", status: "HTTP 200 (HTTPX)" },
          { id: 4, name: "Value-Conscious Diner", phone: "094-551-0982", province: "ปทุมธานี", rating: "4 = มาก (คุ้มค่าราคา)", time: "2026-08-28 10:10:43", status: "HTTP 200 (HTTPX)" }
        ]
      },
      {
        id: "seagames-33",
        formId: "1FAIpQLSeklchUtv4O-H1SpMgWkBm1RVVJWgqqNO4KZeBeqaEtQt_UAg",
        name: "แบบประเมินซีเกมส์ ครั้งที่ 33 (SEA Games)",
        icon: "🏅",
        totalSent: 380,
        successCount: 377,
        failedCount: 3,
        successRate: "99.2%",
        runsCount: 14,
        lastRun: "2026-01-11 21:08",
        primaryEngine: "Selenium & HTTPX",
        color: "#6366f1",
        csvFiles: [
          { name: "seagames_survey_results_20260111_210804.csv", count: 80, size: "2.3 KB", date: "2026-01-11 21:08" },
          { name: "seagames_survey_results_20260111_173229.csv", count: 50, size: "1.0 KB", date: "2026-01-11 17:32" },
          { name: "seagames_survey_results_20260111_162516.csv", count: 40, size: "450 B", date: "2026-01-11 16:25" }
        ],
        rows: [
          { id: 101, name: "สมชาย ใจดี", phone: "081-492-1823", province: "อุดรธานี", rating: "5 = มากที่สุด", time: "2026-01-11 21:08:04", status: "HTTP 200" },
          { id: 102, name: "สมหญิง ศรีสุข", phone: "089-123-4567", province: "ขอนแก่น", rating: "5 = มากที่สุด", time: "2026-01-11 21:08:02", status: "HTTP 200" },
          { id: 103, name: "ชลธิชา วงศ์สุวรรณ", phone: "061-948-2234", province: "อุดรธานี", rating: "4 = มาก", time: "2026-01-11 17:32:29", status: "HTTP 200" }
        ]
      },
      {
        id: "fda-expo",
        formId: "1FAIpQLSdhA8GSrZL5-4a0Q_rWnmfkW6KFphzxLDgzcqbwaH3AATwzmQ",
        name: "แบบลงทะเบียน FDA Expo 2026 (อย.)",
        icon: "💊",
        totalSent: 367,
        successCount: 365,
        failedCount: 2,
        successRate: "99.5%",
        runsCount: 3,
        lastRun: "2026-01-23 11:41",
        primaryEngine: "HTTPX Async",
        color: "#06b6d4",
        csvFiles: [
          { name: "fda_expo_results_20260123_114118.csv", count: 67, size: "1.7 KB", date: "2026-01-23 11:41" }
        ],
        rows: [
          { id: 201, name: "นพ. กิตติพงษ์ ทิพย์มณี", phone: "092-887-3102", province: "กรุงเทพมหานคร", rating: "ยืนยันเข้าร่วมงาน", time: "2026-01-23 11:41:18", status: "HTTP 200" },
          { id: 202, name: "ภก. อภิวัฒน์ สุนทร", phone: "094-551-0982", province: "นนทบุรี", rating: "ยืนยันเข้าร่วมงาน", time: "2026-01-23 11:41:19", status: "HTTP 200" }
        ]
      },
      {
        id: "batch-890",
        formId: "1FAIpQLSeFltPTHhM4uNfOSh0vDuAWL5M-TFzD8KQiuLKF8J3G9jSnlw",
        name: "Batch Registration 890 Records",
        icon: "📋",
        totalSent: 1090,
        successCount: 1090,
        failedCount: 0,
        successRate: "100.0%",
        runsCount: 8,
        lastRun: "2026-01-11 18:45",
        primaryEngine: "HTTPX Coroutines",
        color: "#10b981",
        csvFiles: [
          { name: "registration_results_890.csv", count: 890, size: "94.8 KB", date: "2026-01-11 18:45" },
          { name: "registration_results_100.csv", count: 100, size: "11.0 KB", date: "2026-01-11 17:32" }
        ],
        rows: [
          { id: 301, name: "รัชนก นาคินทร์", phone: "086-773-1940", province: "เดอะมอลล์ บางแค", rating: "5 = มากที่สุด", time: "2026-01-11 18:45:38", status: "HTTP 200" },
          { id: 302, name: "ธีรภัทร ชัยประสิทธิ์", phone: "065-201-9483", province: "เดอะมอลล์ งามวงศ์วาน", rating: "5 = มากที่สุด", time: "2026-01-11 18:45:35", status: "HTTP 200" }
        ]
      },
      {
        id: "mall-survey",
        formId: "1FAIpQLScYXOItwUXkBmHpgQ-oZHozu2BqkfYK7WswvwkQRXANxru8PA",
        name: "แบบประเมินความพึงพอใจศูนย์การค้า",
        icon: "🏬",
        totalSent: 880,
        successCount: 880,
        failedCount: 0,
        successRate: "100.0%",
        runsCount: 12,
        lastRun: "2025-12-21 12:51",
        primaryEngine: "HTTPX Async",
        color: "#f59e0b",
        csvFiles: [
          { name: "survey_mall_results_105_20251210_160822.csv", count: 105, size: "4.8 KB", date: "2025-12-10 16:08" },
          { name: "survey_mall_results_100_20251209_173841.csv", count: 100, size: "4.6 KB", date: "2025-12-09 17:38" }
        ],
        rows: [
          { id: 401, name: "ปิยะ มณีรัตน์", phone: "082-114-9982", province: "เดอะมอลล์ โคราช", rating: "5 = มากที่สุด", time: "2025-12-21 12:51:08", status: "HTTP 200" }
        ]
      }
    ];
  }

  render() {
    const totalAllSent = this.formCatalog.reduce((sum, f) => sum + f.totalSent, 0);
    const totalAllSuccess = this.formCatalog.reduce((sum, f) => sum + f.successCount, 0);
    const totalAllRuns = this.formCatalog.reduce((sum, f) => sum + f.runsCount, 0);

    const activeForm = this.selectedFormId === 'all' 
      ? null 
      : this.formCatalog.find(f => f.id === this.selectedFormId);

    const displayRows = activeForm 
      ? activeForm.rows 
      : this.formCatalog.flatMap(f => f.rows);

    this.container.innerHTML = `
      <!-- Top Title & Global Aggregate KPIs -->
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
        <div>
          <h2 style="font-family: var(--font-display); font-size: 1.3rem; font-weight: 700;">Form Submission History & Intelligence Vault</h2>
          <p style="font-size: 0.8rem; color: var(--text-muted);">ประวัติการส่งข้อมูล จำนวนรอบที่รัน และผลลัพธ์แยกตามแต่ละฟอร์ม</p>
        </div>
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <button class="btn btn-secondary btn-sm ${this.selectedFormId === 'all' ? 'active' : ''}" id="btn-filter-all-forms">
            All Forms (${totalAllSent.toLocaleString()})
          </button>
        </div>
      </div>

      <!-- Per-Form History Cards Grid -->
      <div class="form-history-grid">
        ${this.formCatalog.map(f => `
          <div class="form-history-card ${this.selectedFormId === f.id ? 'active' : ''}" data-form-id="${f.id}">
            <div class="form-history-card-top">
              <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.4rem;">${f.icon}</span>
                <div>
                  <div class="form-history-title">${f.name}</div>
                  <div class="form-history-id">ID: ${f.formId.substring(0, 18)}...</div>
                </div>
              </div>
              <span class="badge badge-success" style="font-size: 0.68rem;">${f.successRate}</span>
            </div>

            <div class="form-history-stats-row">
              <div class="form-history-stat">
                <span class="form-history-stat-label">Total Sent</span>
                <span class="form-history-stat-val" style="color: ${f.color};">${f.totalSent.toLocaleString()}</span>
              </div>
              <div class="form-history-stat">
                <span class="form-history-stat-label">Batches</span>
                <span class="form-history-stat-val" style="font-size: 0.9rem; color: var(--text-secondary);">${f.runsCount} runs</span>
              </div>
              <div class="form-history-stat">
                <span class="form-history-stat-label">Engine</span>
                <span style="font-size: 0.72rem; color: var(--text-dim); font-weight: 600;">${f.primaryEngine}</span>
              </div>
            </div>

            <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.72rem; color: var(--text-dim);">
              <span>Last Run: ${f.lastRun}</span>
              <span style="color: var(--accent-cyan); font-weight: 600;">View Data →</span>
            </div>
          </div>
        `).join('')}
      </div>

      <!-- Detailed Breakdown for Selected Form & CSV File Vault -->
      <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;">
        
        <!-- Live Data Table for Selected Form -->
        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <div class="card-title-icon" style="background: rgba(99, 102, 241, 0.15); color: #a5b4fc;">
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              </div>
              <div>
                <h3 class="card-title">${activeForm ? activeForm.name : "All Forms Combined Submissions"}</h3>
                <p class="card-subtitle">Showing ${displayRows.length} recent response entries</p>
              </div>
            </div>

            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <input type="text" class="form-input" id="table-search-input" placeholder="Search records..." style="width: 180px; padding: 0.4rem 0.65rem; font-size: 0.78rem;">
              <button class="btn btn-secondary btn-sm" id="btn-export-csv">Export CSV</button>
            </div>
          </div>

          <div class="table-container" style="max-height: 280px; overflow-y: auto;">
            <table class="data-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Respondent / Persona</th>
                  <th>Contact / Phone</th>
                  <th>Province / Store</th>
                  <th>Rating / Response</th>
                  <th>Timestamp</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody id="analytics-table-body">
                ${this.renderTableRows(displayRows)}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Historical CSV Result Files Vault -->
        <div class="card">
          <div class="card-header">
            <div class="card-title-group">
              <div class="card-title-icon" style="background: rgba(16, 185, 129, 0.15); color: #34d399;">
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
              </div>
              <div>
                <h3 class="card-title">Saved CSV Runs</h3>
                <p class="card-subtitle">Repository result files</p>
              </div>
            </div>
          </div>

          <div class="file-vault-list">
            ${this.renderCsvFileList(activeForm)}
          </div>
        </div>

      </div>
    `;

    this.bindEvents();
  }

  renderCsvFileList(activeForm) {
    const files = activeForm 
      ? activeForm.csvFiles 
      : this.formCatalog.flatMap(f => f.csvFiles);

    if (!files || files.length === 0) {
      return `<div style="color: var(--text-dim); font-size: 0.78rem; text-align: center; padding: 1rem;">No saved CSV runs for this form yet.</div>`;
    }

    return files.map(file => `
      <div class="file-vault-item">
        <div style="display: flex; flex-direction: column; gap: 0.15rem; overflow: hidden;">
          <span style="font-family: var(--font-mono); font-weight: 600; color: var(--text-primary); font-size: 0.75rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            ${file.name}
          </span>
          <span style="font-size: 0.68rem; color: var(--text-dim);">
            ${file.date} • ${file.count} rows • ${file.size}
          </span>
        </div>
        <button class="btn btn-ghost btn-sm download-csv-file-btn" data-filename="${file.name}" style="padding: 0.2rem 0.5rem; font-size: 0.7rem; color: var(--accent-cyan);">
          Download
        </button>
      </div>
    `).join('');
  }

  renderTableRows(rows) {
    if (!rows || rows.length === 0) {
      return `<tr><td colspan="7" style="text-align: center; color: var(--text-dim); padding: 1.5rem;">No records found matching criteria.</td></tr>`;
    }

    return rows.map(r => `
      <tr>
        <td style="font-family: var(--font-mono); color: var(--text-dim); font-size: 0.75rem;">${r.id}</td>
        <td style="font-weight: 600; color: var(--text-primary); font-size: 0.8rem;">${r.name}</td>
        <td style="font-family: var(--font-mono); color: var(--accent-cyan); font-size: 0.78rem;">${r.phone}</td>
        <td style="font-size: 0.78rem;">${r.province}</td>
        <td><span class="badge badge-success" style="font-size: 0.7rem;">${r.rating}</span></td>
        <td style="font-size: 0.72rem; color: var(--text-dim); font-family: var(--font-mono);">${r.time}</td>
        <td><span class="badge badge-indigo" style="font-size: 0.68rem;">${r.status}</span></td>
      </tr>
    `).join('');
  }

  bindEvents() {
    // Click on per-form card to filter
    this.container.querySelectorAll('.form-history-card').forEach(card => {
      card.addEventListener('click', () => {
        const formId = card.getAttribute('data-form-id');
        this.selectedFormId = (this.selectedFormId === formId) ? 'all' : formId;
        this.render();
      });
    });

    const btnAll = this.container.querySelector('#btn-filter-all-forms');
    if (btnAll) {
      btnAll.addEventListener('click', () => {
        this.selectedFormId = 'all';
        this.render();
      });
    }

    // Search filter
    const searchInput = this.container.querySelector('#table-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const activeForm = this.selectedFormId === 'all' ? null : this.formCatalog.find(f => f.id === this.selectedFormId);
        const allRows = activeForm ? activeForm.rows : this.formCatalog.flatMap(f => f.rows);
        const filtered = allRows.filter(r => 
          r.name.toLowerCase().includes(query) || 
          r.phone.includes(query) || 
          r.province.toLowerCase().includes(query) ||
          r.rating.toLowerCase().includes(query)
        );
        const tbody = this.container.querySelector('#analytics-table-body');
        if (tbody) tbody.innerHTML = this.renderTableRows(filtered);
      });
    }

    // Export CSV
    const btnCsv = this.container.querySelector('#btn-export-csv');
    if (btnCsv) {
      btnCsv.addEventListener('click', () => {
        const activeForm = this.selectedFormId === 'all' ? null : this.formCatalog.find(f => f.id === this.selectedFormId);
        const allRows = activeForm ? activeForm.rows : this.formCatalog.flatMap(f => f.rows);
        const header = "ID,Name,Phone,Province,Rating,Timestamp,Status\n";
        const csvContent = header + allRows.map(r => `"${r.id}","${r.name}","${r.phone}","${r.province}","${r.rating}","${r.time}","${r.status}"`).join('\n');
        
        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${this.selectedFormId}_submissions_export.csv`;
        a.click();
        store.addLog("ok", `Downloaded CSV history for [${this.selectedFormId}]: ${a.download}`);
      });
    }

    // Download specific CSV file
    this.container.querySelectorAll('.download-csv-file-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const filename = btn.getAttribute('data-filename');
        store.addLog("info", `Ready to download CSV file: ${filename}`);
        alert(`ไฟล์ ${filename} อยู่ในโปรเจกต์ของคุณเรียบร้อยแล้วครับ`);
      });
    });
  }
}
