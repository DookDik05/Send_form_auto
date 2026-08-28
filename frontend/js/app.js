/**
 * AutoForm Pro Max - Main Application Entrypoint & Orchestrator (Robust Lifecycle Edition)
 */

import { store } from './store.js';
import { DashboardModule } from './modules/dashboard.js';
import { InspectorModule } from './modules/inspector.js';
import { PayloadStudioModule } from './modules/payloadStudio.js';
import { DispatcherModule } from './modules/dispatcher.js';
import { TerminalModule } from './modules/terminal.js';
import { AnalyticsModule } from './modules/analytics.js';

class Application {
  constructor() {
    this.modules = {};
    this.currentTab = 'dashboard';
    this.isInitialized = false;
  }

  init() {
    if (this.isInitialized) return;
    this.isInitialized = true;
    console.log("⚡ AutoForm Pro Max - Booting cockpit modules...");

    try {
      // 1. Instantiate modules safely
      this.modules.dashboard = new DashboardModule();
      this.modules.inspector = new InspectorModule();
      this.modules.payload = new PayloadStudioModule();
      this.modules.dispatcher = new DispatcherModule();
      this.modules.terminal = new TerminalModule();
      this.modules.analytics = new AnalyticsModule();

      // 2. Render initial views
      if (this.modules.dashboard) this.modules.dashboard.render();
      if (this.modules.inspector) this.modules.inspector.render();
      if (this.modules.payload) this.modules.payload.render();
      if (this.modules.dispatcher) this.modules.dispatcher.render();
      if (this.modules.terminal) this.modules.terminal.render();
      if (this.modules.analytics) this.modules.analytics.render();

      // 3. Bind navigation & interactions
      this.bindNavigation();
      this.setupKeyboardShortcuts();
      this.setupTooltips();

      // 4. Subscribe to reactive store
      store.subscribe((state) => {
        this.handleStateChange(state);
      });

      // 5. Activate initial tab
      const initialTab = store.getState().activeTab || 'dashboard';
      this.switchTab(initialTab);

      console.log("✅ AutoForm Pro Max - All cockpit modules rendered successfully.");
    } catch (err) {
      console.error("❌ AutoForm Pro Max - Boot error:", err);
    }
  }

  bindNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const tab = item.getAttribute('data-tab');
        if (tab) {
          this.switchTab(tab);
        }
      });
    });

    // Quick Dispatch button
    const btnQuick = document.getElementById('btn-quick-dispatch');
    if (btnQuick) {
      btnQuick.addEventListener('click', () => {
        this.switchTab('dispatcher');
      });
    }

    // Inspect Form button
    const btnInspect = document.getElementById('btn-inspect-form');
    if (btnInspect) {
      btnInspect.addEventListener('click', () => {
        this.switchTab('inspector');
      });
    }
  }

  setupKeyboardShortcuts() {
    window.addEventListener('keydown', (e) => {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {
        if (e.key === 'Escape') document.activeElement.blur();
        return;
      }

      if (e.key === '1') this.switchTab('dashboard');
      else if (e.key === '2') this.switchTab('dispatcher');
      else if (e.key === '3') this.switchTab('inspector');
      else if (e.key === '4') this.switchTab('terminal');
      else if (e.key === '5') this.switchTab('analytics');

      else if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        this.switchTab('dispatcher');
        setTimeout(() => {
          const btn = document.getElementById('btn-launch-mission');
          if (btn && btn.style.display !== 'none') btn.click();
        }, 150);
      }

      else if (e.key === 'Escape') {
        const modal = document.getElementById('shortcuts-modal');
        if (modal && modal.classList.contains('active')) {
          modal.classList.remove('active');
        } else {
          const btnAbort = document.getElementById('btn-abort-mission');
          if (btnAbort && btnAbort.style.display !== 'none') btnAbort.click();
        }
      }

      else if (e.key === '?' || e.key === '/') {
        this.toggleShortcutsModal();
      }
    });
  }

  toggleShortcutsModal() {
    let modal = document.getElementById('shortcuts-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'shortcuts-modal';
      modal.className = 'shortcuts-modal-overlay';
      modal.innerHTML = `
        <div class="shortcuts-modal-card">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <span style="font-size: 1.2rem;">⌨️</span>
              <h3 style="font-size: 1rem; font-weight: 700; color: var(--text-primary);">Keyboard Shortcuts</h3>
            </div>
            <button class="btn btn-ghost btn-sm" id="btn-close-shortcuts-modal" style="padding: 0.2rem 0.5rem;">✕</button>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; font-size: 0.8rem;">
            <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
              <span>Dashboard</span>
              <kbd class="kbd-badge">1</kbd>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
              <span>Dispatcher</span>
              <kbd class="kbd-badge">2</kbd>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
              <span>Inspector</span>
              <kbd class="kbd-badge">3</kbd>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
              <span>Matrix Terminal</span>
              <kbd class="kbd-badge">4</kbd>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
              <span>Analytics Vault</span>
              <kbd class="kbd-badge">5</kbd>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
              <span>Launch Campaign</span>
              <kbd class="kbd-badge">Ctrl+Enter</kbd>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
              <span>Abort Mission</span>
              <kbd class="kbd-badge">Esc</kbd>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.4rem 0.6rem; background: var(--bg-surface-3); border-radius: var(--radius-sm);">
              <span>Toggle Shortcuts</span>
              <kbd class="kbd-badge">?</kbd>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
      modal.querySelector('#btn-close-shortcuts-modal').addEventListener('click', () => {
        modal.classList.remove('active');
      });
      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('active');
      });
    }
    modal.classList.toggle('active');
  }

  setupTooltips() {
    document.addEventListener('mouseover', (e) => {
      const target = e.target.closest('[data-tooltip]');
      if (!target) return;
      const text = target.getAttribute('data-tooltip');
      if (!text) return;

      let tip = document.getElementById('global-micro-tooltip');
      if (!tip) {
        tip = document.createElement('div');
        tip.id = 'global-micro-tooltip';
        tip.className = 'micro-tooltip';
        document.body.appendChild(tip);
      }
      tip.textContent = text;
      tip.classList.add('visible');

      const rect = target.getBoundingClientRect();
      tip.style.top = `${Math.max(10, rect.top - 32)}px`;
      tip.style.left = `${rect.left + (rect.width / 2)}px`;
    });

    document.addEventListener('mouseout', (e) => {
      const target = e.target.closest('[data-tooltip]');
      if (!target) return;
      const tip = document.getElementById('global-micro-tooltip');
      if (tip) tip.classList.remove('visible');
    });
  }

  switchTab(tabName) {
    if (!tabName) tabName = 'dashboard';
    this.currentTab = tabName;
    store.setState({ activeTab: tabName });

    // Update active nav items
    document.querySelectorAll('.nav-item').forEach(item => {
      if (item.getAttribute('data-tab') === tabName) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    // Update breadcrumb title
    const breadcrumb = document.getElementById('current-view-title');
    if (breadcrumb) {
      const titles = {
        dashboard: "Mission Control Overview",
        inspector: "Google Form Inspector & Parser",
        payload: "Payload Studio & Probability Engine",
        dispatcher: "Campaign Execution & Runner",
        terminal: "Live Stream Matrix Terminal",
        analytics: "Analytics & Submission Vault"
      };
      breadcrumb.textContent = titles[tabName] || tabName;
    }

    // Toggle view panels
    document.querySelectorAll('.view-panel').forEach(panel => {
      if (panel.id === `view-${tabName}`) {
        panel.classList.add('active');
        panel.style.display = 'flex';
      } else {
        panel.classList.remove('active');
        panel.style.display = 'none';
      }
    });

    // Module-specific hooks
    if (tabName === 'terminal' && this.modules.terminal) {
      this.modules.terminal.scrollToBottom();
    } else if (tabName === 'analytics' && this.modules.analytics) {
      this.modules.analytics.fetchLiveHistory();
    }
  }

  handleStateChange(state) {
    const sbTotal = document.getElementById('statusbar-total');
    if (sbTotal) sbTotal.textContent = `Subs: ${state.totalSubmissions.toLocaleString()}`;

    const sbWorkers = document.getElementById('statusbar-workers');
    if (sbWorkers) sbWorkers.textContent = `Workers: ${state.activeWorkers}`;

    const sbEngine = document.getElementById('statusbar-engine');
    if (sbEngine && state.currentCampaign) sbEngine.textContent = `Engine: ${state.currentCampaign.mode.toUpperCase()}`;

    if (this.modules.terminal) {
      this.modules.terminal.updateLogs(state.logs);
    }

    const kpiTotal = document.getElementById('kpi-total-subs');
    if (kpiTotal) kpiTotal.textContent = state.totalSubmissions.toLocaleString();

    const kpiRPS = document.getElementById('kpi-current-rps');
    if (kpiRPS) kpiRPS.textContent = state.currentRPS;

    const kpiWorkers = document.getElementById('kpi-active-workers');
    if (kpiWorkers) kpiWorkers.textContent = `${state.activeWorkers} / 50`;
  }
}

// Unconditional boot instantiation (overrides the automatic window.app DOM reference)
function boot() {
  const appInstance = new Application();
  window.app = appInstance;
  window.autoFormApp = appInstance;
  appInstance.init();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
