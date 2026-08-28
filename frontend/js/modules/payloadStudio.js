/**
 * AutoForm Pro Max - Payload Studio & Probability Engine
 */

import { store } from '../store.js';
import { generateRandomThaiProfile } from '../data/thaiData.js';

export class PayloadStudioModule {
  constructor() {
    this.container = document.getElementById('view-payload');
    this.thaiProfile = generateRandomThaiProfile();
  }

  render() {
    this.container.innerHTML = `
      <div style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 1.5rem;">
        
        <!-- Left: Probability Sliders & Weight Tuning -->
        <div style="display: flex; flex-direction: column; gap: 1.25rem;">
          
          <div class="card card-glow-indigo">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-title-icon">
                  <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/></svg>
                </div>
                <div>
                  <h3 class="card-title">Demographic Probability Weights</h3>
                  <p class="card-subtitle">Adjust answer distribution percentages for randomized submissions</p>
                </div>
              </div>
              <div style="display: flex; gap: 0.5rem;">
                <button class="btn btn-ghost btn-sm" id="btn-preset-natural">Natural Curve</button>
                <button class="btn btn-ghost btn-sm" id="btn-preset-highsat">High 5-Star</button>
              </div>
            </div>

            <!-- Nationality Distribution -->
            <div class="prob-card" style="margin-bottom: 0.75rem;">
              <div class="prob-header">
                <span class="prob-title">1. สัญชาติ (Nationality)</span>
                <span class="prob-badge" id="badge-nat-sum">Total: 100%</span>
              </div>
              <div class="prob-item">
                <div class="prob-item-meta">
                  <span>คนไทย (Thai)</span>
                  <span class="prob-item-val" id="val-nat-thai">92%</span>
                </div>
                <input type="range" class="range-slider" id="slider-nat-thai" min="50" max="100" value="92">
              </div>
              <div class="prob-item">
                <div class="prob-item-meta">
                  <span>ต่างชาติ (Foreigner)</span>
                  <span class="prob-item-val" id="val-nat-foreign">8%</span>
                </div>
              </div>
              <div class="stacked-dist-bar">
                <div id="bar-nat-thai" class="stacked-dist-segment" style="width: 92%; background: #6366f1;"></div>
                <div id="bar-nat-foreign" class="stacked-dist-segment" style="width: 8%; background: #06b6d4;"></div>
              </div>
            </div>

            <!-- Gender Distribution -->
            <div class="prob-card" style="margin-bottom: 0.75rem;">
              <div class="prob-header">
                <span class="prob-title">2. เพศ (Gender)</span>
                <span class="prob-badge" id="badge-gender-sum">Total: 100%</span>
              </div>
              <div class="prob-item">
                <div class="prob-item-meta">
                  <span>ชาย (Male)</span>
                  <span class="prob-item-val" id="val-gender-m">48%</span>
                </div>
                <input type="range" class="range-slider" id="slider-gender-m" min="20" max="80" value="48">
              </div>
              <div class="prob-item">
                <div class="prob-item-meta">
                  <span>หญิง (Female)</span>
                  <span class="prob-item-val" id="val-gender-f">48%</span>
                </div>
              </div>
              <div class="stacked-dist-bar">
                <div id="bar-gender-m" class="stacked-dist-segment" style="width: 48%; background: #3b82f6;"></div>
                <div id="bar-gender-f" class="stacked-dist-segment" style="width: 48%; background: #ec4899;"></div>
                <div id="bar-gender-o" class="stacked-dist-segment" style="width: 4%; background: #a855f7;"></div>
              </div>
            </div>

            <!-- Likert Satisfaction 5-Point Matrix -->
            <div class="prob-card">
              <div class="prob-header">
                <span class="prob-title">3. ความพึงพอใจ Likert Scale (5-Point)</span>
                <span class="badge badge-success">Optimized Delivery</span>
              </div>
              <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.5rem; text-align: center; margin-top: 0.25rem;">
                <div style="background: rgba(16, 185, 129, 0.15); padding: 0.5rem; border-radius: var(--radius-sm); border: 1px solid var(--color-success-border);">
                  <div style="font-weight: 700; color: #34d399; font-size: 0.95rem;">85%</div>
                  <div style="font-size: 0.7rem; color: var(--text-muted);">5 = มากที่สุด</div>
                </div>
                <div style="background: rgba(6, 182, 212, 0.1); padding: 0.5rem; border-radius: var(--radius-sm);">
                  <div style="font-weight: 700; color: #22d3ee; font-size: 0.95rem;">15%</div>
                  <div style="font-size: 0.7rem; color: var(--text-muted);">4 = มาก</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.04); padding: 0.5rem; border-radius: var(--radius-sm);">
                  <div style="font-weight: 700; color: var(--text-dim); font-size: 0.95rem;">0%</div>
                  <div style="font-size: 0.7rem; color: var(--text-muted);">3 = ปานกลาง</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.04); padding: 0.5rem; border-radius: var(--radius-sm);">
                  <div style="font-weight: 700; color: var(--text-dim); font-size: 0.95rem;">0%</div>
                  <div style="font-size: 0.7rem; color: var(--text-muted);">2 = น้อย</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.04); padding: 0.5rem; border-radius: var(--radius-sm);">
                  <div style="font-weight: 700; color: var(--text-dim); font-size: 0.95rem;">0%</div>
                  <div style="font-size: 0.7rem; color: var(--text-muted);">1 = น้อยที่สุด</div>
                </div>
              </div>
            </div>

          </div>

        </div>

        <!-- Right: Thai Synthetic Identity Generator & Mock Data Picker -->
        <div style="display: flex; flex-direction: column; gap: 1.25rem;">
          
          <!-- Thai Identity Card -->
          <div class="card card-glow-cyan">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-title-icon" style="background: rgba(6, 182, 212, 0.15); color: #22d3ee;">
                  <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                </div>
                <div>
                  <h3 class="card-title">Thai Synthetic Identity</h3>
                  <p class="card-subtitle">Real-time profile preview engine</p>
                </div>
              </div>
              <button class="btn btn-secondary btn-sm" id="btn-regen-identity">
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                Regenerate
              </button>
            </div>

            <div id="thai-identity-preview" style="display: flex; flex-direction: column; gap: 0.65rem; background: var(--bg-surface-2); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
              <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 0.75rem; color: var(--text-dim);">Full Name (TH):</span>
                <span style="font-weight: 700; color: var(--text-primary);" id="id-name">${this.thaiProfile.fullName}</span>
              </div>
              <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 0.75rem; color: var(--text-dim);">Mobile Phone:</span>
                <span style="font-family: var(--font-mono); color: var(--accent-cyan);" id="id-phone">${this.thaiProfile.phone}</span>
              </div>
              <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 0.75rem; color: var(--text-dim);">Email Address:</span>
                <span style="font-family: var(--font-mono); color: #a5b4fc; font-size: 0.8rem;" id="id-email">${this.thaiProfile.email}</span>
              </div>
              <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 0.75rem; color: var(--text-dim);">Province:</span>
                <span style="color: var(--text-secondary);" id="id-province">${this.thaiProfile.province}</span>
              </div>
              <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 0.75rem; color: var(--text-dim);">Organization:</span>
                <span style="color: var(--text-secondary); font-size: 0.8rem;" id="id-org">${this.thaiProfile.organization}</span>
              </div>
              <div style="margin-top: 0.35rem; padding-top: 0.5rem; border-top: 1px solid var(--border-subtle);">
                <span style="font-size: 0.72rem; color: var(--text-dim); display: block; margin-bottom: 0.2rem;">Generated Feedback Comment:</span>
                <p style="font-size: 0.78rem; font-style: italic; color: #cbd5e1;" id="id-comment">"${this.thaiProfile.comment}"</p>
              </div>
            </div>
          </div>

          <!-- Mock Dataset Mapper -->
          <div class="card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-title-icon" style="background: rgba(168, 85, 247, 0.15); color: #c084fc;">
                  <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7c0-2-1-3-3-3H7C5 4 4 5 4 7z"/></svg>
                </div>
                <div>
                  <h3 class="card-title">Dataset File Loader</h3>
                  <p class="card-subtitle">Select repository JSON/CSV records</p>
                </div>
              </div>
            </div>

            <div class="form-group" style="margin-bottom: 0.75rem;">
              <label class="form-label">Active Dataset Source</label>
              <select class="form-select" id="select-dataset-source">
                <option value="mock_data_890.json">mock_data_890.json (890 Records)</option>
                <option value="mock_data_95.json">mock_data_95.json (95 Records)</option>
                <option value="entries.csv">entries.csv (CSV Table)</option>
                <option value="synthetic">Pure Synthetic Generator (Unlimited)</option>
              </select>
            </div>

            <button class="btn btn-primary" style="width: 100%;" id="btn-apply-payload">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
              Apply to Campaign Dispatcher
            </button>
          </div>

        </div>

      </div>
    `;

    this.bindEvents();
  }

  bindEvents() {
    const btnRegen = this.container.querySelector('#btn-regen-identity');
    if (btnRegen) {
      btnRegen.addEventListener('click', () => {
        this.thaiProfile = generateRandomThaiProfile();
        this.container.querySelector('#id-name').textContent = this.thaiProfile.fullName;
        this.container.querySelector('#id-phone').textContent = this.thaiProfile.phone;
        this.container.querySelector('#id-email').textContent = this.thaiProfile.email;
        this.container.querySelector('#id-province').textContent = this.thaiProfile.province;
        this.container.querySelector('#id-org').textContent = this.thaiProfile.organization;
        this.container.querySelector('#id-comment').textContent = `"${this.thaiProfile.comment}"`;
      });
    }

    const sliderNat = this.container.querySelector('#slider-nat-thai');
    if (sliderNat) {
      sliderNat.addEventListener('input', (e) => {
        const val = parseInt(e.target.value, 10);
        const foreign = 100 - val;
        this.container.querySelector('#val-nat-thai').textContent = `${val}%`;
        this.container.querySelector('#val-nat-foreign').textContent = `${foreign}%`;
        this.container.querySelector('#bar-nat-thai').style.width = `${val}%`;
        this.container.querySelector('#bar-nat-foreign').style.width = `${foreign}%`;
      });
    }

    const sliderGender = this.container.querySelector('#slider-gender-m');
    if (sliderGender) {
      sliderGender.addEventListener('input', (e) => {
        const val = parseInt(e.target.value, 10);
        const female = 100 - val - 4;
        this.container.querySelector('#val-gender-m').textContent = `${val}%`;
        this.container.querySelector('#val-gender-f').textContent = `${female}%`;
        this.container.querySelector('#bar-gender-m').style.width = `${val}%`;
        this.container.querySelector('#bar-gender-f').style.width = `${female}%`;
      });
    }

    const btnApply = this.container.querySelector('#btn-apply-payload');
    if (btnApply) {
      btnApply.addEventListener('click', () => {
        store.addLog("ok", "Probability weights & Thai synthetic profiles updated and primed for dispatch.");
        window.app.switchTab('dispatcher');
      });
    }
  }
}
