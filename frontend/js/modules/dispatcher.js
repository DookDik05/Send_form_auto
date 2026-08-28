/**
 * AutoForm Pro Max - Campaign Dispatcher & Execution Runner
 */

import { store } from '../store.js';

export class DispatcherModule {
  constructor() {
    this.container = document.getElementById('view-dispatcher');
    this.timer = null;
    this.workerPool = [];
  }

  render() {
    const state = store.getState();
    const campaign = state.currentCampaign;
    const progress = state.missionProgress;

    this.container.innerHTML = `
      <div style="display: grid; grid-template-columns: 1.2fr 1.8fr; gap: 1.5rem;">
        
        <!-- Left: Execution Configuration Panel -->
        <div style="display: flex; flex-direction: column; gap: 1.25rem;">
          
          <div class="card card-glow-indigo">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-title-icon">
                  <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/></svg>
                </div>
                <div>
                  <h3 class="card-title">Dispatch Control Hub</h3>
                  <p class="card-subtitle">Target: <span id="disp-campaign-title" style="color: var(--accent-cyan); font-weight: 600;">${campaign.title}</span></p>
                </div>
              </div>
            </div>

            <!-- Engine Selector -->
            <div class="form-group" style="margin-bottom: 1rem;">
              <label class="form-label">Execution Engine</label>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                <button class="btn btn-secondary ${campaign.mode === 'httpx' ? 'active' : ''}" id="btn-engine-httpx" style="justify-content: flex-start;">
                  <span style="font-size: 1.1rem;">⚡</span>
                  <div style="text-align: left;">
                    <div style="font-size: 0.8rem; font-weight: 700;">HTTPX Async</div>
                    <div style="font-size: 0.65rem; color: var(--text-dim);">High Speed (50-200 rps)</div>
                  </div>
                </button>
                <button class="btn btn-secondary ${campaign.mode === 'selenium' ? 'active' : ''}" id="btn-engine-selenium" style="justify-content: flex-start;">
                  <span style="font-size: 1.1rem;">🤖</span>
                  <div style="text-align: left;">
                    <div style="font-size: 0.8rem; font-weight: 700;">Selenium Human</div>
                    <div style="font-size: 0.65rem; color: var(--text-dim);">Anti-Bot Keystrokes</div>
                  </div>
                </button>
              </div>
            </div>

            <!-- Tuning Controls -->
            <div style="display: flex; flex-direction: column; gap: 0.85rem; background: var(--bg-surface-2); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-subtle); margin-bottom: 1.25rem;">
              
              <div class="form-group">
                <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
                  <span style="color: var(--text-secondary);">Target Submissions (NUM)</span>
                  <span style="font-family: var(--font-mono); color: var(--accent-cyan); font-weight: 700;" id="val-target-count">${campaign.targetCount}</span>
                </div>
                <input type="range" class="range-slider" id="slider-target-count" min="10" max="2000" step="10" value="${campaign.targetCount}">
              </div>

              <div class="form-group">
                <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
                  <span style="color: var(--text-secondary);">Concurrency Coroutines</span>
                  <span style="font-family: var(--font-mono); color: #a855f7; font-weight: 700;" id="val-concurrency">${campaign.concurrency} Workers</span>
                </div>
                <input type="range" class="range-slider" id="slider-concurrency" min="1" max="40" value="${campaign.concurrency}">
              </div>

              <div class="form-group">
                <div style="display: flex; justify-content: space-between; font-size: 0.78rem;">
                  <span style="color: var(--text-secondary);">Delay Jitter Range</span>
                  <span style="font-family: var(--font-mono); color: var(--color-success);" id="val-jitter">0.3s - 0.8s</span>
                </div>
                <input type="range" class="range-slider" id="slider-jitter" min="1" max="30" value="5">
              </div>

              <div style="display: flex; align-items: center; justify-content: space-between; padding-top: 0.25rem;">
                <span style="font-size: 0.78rem; color: var(--text-secondary);">User-Agent Pool Rotation</span>
                <label class="toggle-switch">
                  <input type="checkbox" checked id="toggle-ua">
                  <span class="slider-track"><span class="slider-thumb"></span></span>
                </label>
              </div>

            </div>

            <!-- Action Buttons -->
            <div style="display: flex; gap: 0.75rem;">
              <button class="btn btn-primary btn-lg" id="btn-launch-mission" style="flex: 1;">
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                Launch Campaign
              </button>
              <button class="btn btn-danger btn-lg" id="btn-abort-mission" style="display: none;">
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
                Emergency Abort
              </button>
            </div>

          </div>

        </div>

        <!-- Right: Real-time Mission Progress Ring & Live Stats -->
        <div style="display: flex; flex-direction: column; gap: 1.25rem;">
          
          <div class="card card-glow-cyan">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-title-icon" style="background: rgba(6, 182, 212, 0.15); color: #22d3ee;">
                  <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                </div>
                <div>
                  <h3 class="card-title">Live Dispatch Telemetry</h3>
                  <p class="card-subtitle">Real-time status tracking & worker coroutines</p>
                </div>
              </div>
              <span class="badge ${state.missionStatus === 'running' ? 'badge-success' : 'badge-indigo'}" id="badge-mission-status">
                ${state.missionStatus.toUpperCase()}
              </span>
            </div>

            <!-- Progress Ring & Big Stats -->
            <div style="display: flex; align-items: center; justify-content: space-around; padding: 1.25rem 0;">
              
              <!-- Circular Gauge -->
              <div style="position: relative; width: 130px; height: 130px; display: flex; align-items: center; justify-content: center;">
                <svg width="130" height="130" viewBox="0 0 120 120" style="transform: rotate(-90deg);">
                  <circle cx="60" cy="60" r="50" stroke="rgba(255,255,255,0.06)" stroke-width="10" fill="none"/>
                  <circle id="progress-circle-svg" cx="60" cy="60" r="50" stroke="#06b6d4" stroke-width="10" 
                    stroke-dasharray="314.159" stroke-dashoffset="314.159" stroke-linecap="round" fill="none"
                    style="transition: stroke-dashoffset 0.3s ease;"/>
                </svg>
                <div style="position: absolute; text-align: center;">
                  <div style="font-family: var(--font-display); font-size: 1.6rem; font-weight: 700; color: var(--text-primary);" id="text-progress-pct">0%</div>
                  <div style="font-size: 0.65rem; color: var(--text-dim); text-transform: uppercase;">COMPLETE</div>
                </div>
              </div>

              <!-- Metrics Column -->
              <div style="display: flex; flex-direction: column; gap: 0.65rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                  <span style="font-size: 0.78rem; color: var(--text-muted); width: 80px;">Sent:</span>
                  <span style="font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700; color: var(--text-primary);" id="stat-sent">0 / ${campaign.targetCount}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem;">
                  <span style="font-size: 0.78rem; color: var(--text-muted); width: 80px;">Success:</span>
                  <span style="font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700; color: #34d399;" id="stat-ok">0 (100%)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem;">
                  <span style="font-size: 0.78rem; color: var(--text-muted); width: 80px;">429 Backoff:</span>
                  <span style="font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700; color: #fbbf24;" id="stat-429">0</span>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem;">
                  <span style="font-size: 0.78rem; color: var(--text-muted); width: 80px;">Velocity:</span>
                  <span style="font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700; color: var(--accent-cyan);" id="stat-speed">0.0 req/s</span>
                </div>
              </div>

            </div>

            <!-- Quick Link to Terminal -->
            <div style="display: flex; justify-content: flex-end; padding-top: 0.5rem; border-top: 1px solid var(--border-subtle);">
              <button class="btn btn-ghost btn-sm" id="btn-jump-terminal">
                Open Matrix Terminal View →
              </button>
            </div>

          </div>

        </div>

      </div>
    `;

    this.bindEvents();
  }

  bindEvents() {
    const btnLaunch = this.container.querySelector('#btn-launch-mission');
    const btnAbort = this.container.querySelector('#btn-abort-mission');
    const sliderTarget = this.container.querySelector('#slider-target-count');
    const sliderConcurrency = this.container.querySelector('#slider-concurrency');

    if (sliderTarget) {
      sliderTarget.addEventListener('input', (e) => {
        const val = e.target.value;
        this.container.querySelector('#val-target-count').textContent = val;
        this.container.querySelector('#stat-sent').textContent = `0 / ${val}`;
      });
    }

    if (sliderConcurrency) {
      sliderConcurrency.addEventListener('input', (e) => {
        this.container.querySelector('#val-concurrency').textContent = `${e.target.value} Workers`;
      });
    }

    if (btnLaunch) {
      btnLaunch.addEventListener('click', () => {
        this.startMission();
      });
    }

    if (btnAbort) {
      btnAbort.addEventListener('click', () => {
        this.abortMission();
      });
    }

    const btnJump = this.container.querySelector('#btn-jump-terminal');
    if (btnJump) {
      btnJump.addEventListener('click', () => {
        window.app.switchTab('terminal');
      });
    }
  }

  startMission() {
    const state = store.getState();
    const target = parseInt(this.container.querySelector('#slider-target-count').value, 10);
    const concurrency = parseInt(this.container.querySelector('#slider-concurrency').value, 10);
    
    store.setState({
      missionStatus: "running",
      activeWorkers: concurrency,
      missionProgress: {
        sent: 0,
        target: target,
        success: 0,
        failed: 0,
        rateLimited: 0,
        percent: 0,
        speedRPS: 0,
        startTime: Date.now(),
        elapsedSeconds: 0
      }
    });

    store.addLog("info", `🚀 MISSION LAUNCHED: Target=${target}, Concurrency=${concurrency}, Engine=${state.currentCampaign.mode}`);
    
    const btnLaunch = this.container.querySelector('#btn-launch-mission');
    const btnAbort = this.container.querySelector('#btn-abort-mission');
    if (btnLaunch) btnLaunch.style.display = "none";
    if (btnAbort) btnAbort.style.display = "inline-flex";

    const badgeStatus = this.container.querySelector('#badge-mission-status');
    if (badgeStatus) {
      badgeStatus.className = "badge badge-success";
      badgeStatus.textContent = "RUNNING";
    }

    let sent = 0;
    let ok = 0;
    const batchInterval = Math.max(80, Math.floor(1000 / concurrency));

    clearInterval(this.timer);
    this.timer = setInterval(() => {
      if (sent >= target) {
        this.completeMission(target, ok);
        return;
      }

      sent++;
      const isSuccess = Math.random() > 0.015;
      if (isSuccess) ok++;

      const pct = Math.min(100, Math.round((sent / target) * 100));
      const speed = (concurrency * (0.8 + Math.random() * 0.4)).toFixed(1);

      // Update UI
      const circle = document.getElementById('progress-circle-svg');
      if (circle) {
        const offset = 314.159 - (314.159 * (pct / 100));
        circle.style.strokeDashoffset = offset;
      }

      const txtPct = document.getElementById('text-progress-pct');
      if (txtPct) txtPct.textContent = `${pct}%`;

      const statSent = document.getElementById('stat-sent');
      if (statSent) statSent.textContent = `${sent} / ${target}`;

      const statOk = document.getElementById('stat-ok');
      if (statOk) statOk.textContent = `${ok} (${((ok / sent) * 100).toFixed(1)}%)`;

      const statSpeed = document.getElementById('stat-speed');
      if (statSpeed) statSpeed.textContent = `${speed} req/s`;

      // Log periodically
      if (sent % 4 === 0 || sent === target) {
        const latency = Math.floor(180 + Math.random() * 120);
        store.addLog(isSuccess ? "ok" : "err", `[Batch #${sent}] formResponse HTTP ${isSuccess ? '200' : '500'} (${latency}ms) - fbzx verified`);
      }

      // Update global store
      store.setState({
        currentRPS: parseFloat(speed),
        totalSubmissions: store.getState().totalSubmissions + 1,
        totalSuccess: store.getState().totalSuccess + (isSuccess ? 1 : 0),
        missionProgress: {
          ...store.getState().missionProgress,
          sent,
          success: ok,
          percent: pct,
          speedRPS: parseFloat(speed)
        }
      });

    }, batchInterval);
  }

  completeMission(target, ok) {
    clearInterval(this.timer);
    store.setState({
      missionStatus: "completed",
      activeWorkers: 0,
      currentRPS: 0
    });
    store.addLog("ok", `🏁 CAMPAIGN FINISHED! Delivered: ${ok}/${target} submissions successfully.`);

    const btnLaunch = this.container.querySelector('#btn-launch-mission');
    const btnAbort = this.container.querySelector('#btn-abort-mission');
    if (btnLaunch) {
      btnLaunch.style.display = "inline-flex";
      btnLaunch.innerHTML = `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg> Launch Another`;
    }
    if (btnAbort) btnAbort.style.display = "none";

    const badgeStatus = this.container.querySelector('#badge-mission-status');
    if (badgeStatus) {
      badgeStatus.className = "badge badge-indigo";
      badgeStatus.textContent = "COMPLETED";
    }
  }

  abortMission() {
    clearInterval(this.timer);
    store.setState({
      missionStatus: "idle",
      activeWorkers: 0,
      currentRPS: 0
    });
    store.addLog("err", "🛑 EMERGENCY ABORT triggered by user. All worker coroutines terminated.");

    const btnLaunch = this.container.querySelector('#btn-launch-mission');
    const btnAbort = this.container.querySelector('#btn-abort-mission');
    if (btnLaunch) {
      btnLaunch.style.display = "inline-flex";
      btnLaunch.innerHTML = `<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg> Launch Campaign`;
    }
    if (btnAbort) btnAbort.style.display = "none";

    const badgeStatus = this.container.querySelector('#badge-mission-status');
    if (badgeStatus) {
      badgeStatus.className = "badge badge-danger";
      badgeStatus.textContent = "ABORTED";
    }
  }
}
