/**
 * AutoForm Pro Max - Main Application Entrypoint & Orchestrator
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
  }

  init() {
    // Instantiate sub-modules
    this.modules.dashboard = new DashboardModule();
    this.modules.inspector = new InspectorModule();
    this.modules.payload = new PayloadStudioModule();
    this.modules.dispatcher = new DispatcherModule();
    this.modules.terminal = new TerminalModule();
    this.modules.analytics = new AnalyticsModule();

    // Render initial views
    this.modules.dashboard.render();
    this.modules.inspector.render();
    this.modules.payload.render();
    this.modules.dispatcher.render();
    this.modules.terminal.render();
    this.modules.analytics.render();

    // Bind sidebar navigation
    this.bindNavigation();

    // Subscribe to reactive store changes
    store.subscribe((state) => {
      this.handleStateChange(state);
    });

    // Setup global keyboard shortcuts
    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        this.switchTab('inspector');
      }
    });

    console.log("⚡ AutoForm Pro Max Web UI Initialized.");
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
  }

  switchTab(tabName) {
    if (!this.modules[tabName] && tabName !== 'dashboard') return;

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

    // Update breadcrumb
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
      } else {
        panel.classList.remove('active');
      }
    });

    // Re-render or refresh specific modules if needed
    if (tabName === 'terminal') {
      this.modules.terminal.scrollToBottom();
    }
  }

  handleStateChange(state) {
    // Update live statusbar items
    const sbTotal = document.getElementById('statusbar-total');
    if (sbTotal) sbTotal.textContent = `Subs: ${state.totalSubmissions.toLocaleString()}`;

    const sbWorkers = document.getElementById('statusbar-workers');
    if (sbWorkers) sbWorkers.textContent = `Workers: ${state.activeWorkers}`;

    const sbEngine = document.getElementById('statusbar-engine');
    if (sbEngine) sbEngine.textContent = `Engine: ${state.currentCampaign.mode.toUpperCase()}`;

    // Update terminal if logs changed
    this.modules.terminal.updateLogs(state.logs);

    // Update KPI counters on dashboard
    const kpiTotal = document.getElementById('kpi-total-subs');
    if (kpiTotal) kpiTotal.textContent = state.totalSubmissions.toLocaleString();

    const kpiRPS = document.getElementById('kpi-current-rps');
    if (kpiRPS) kpiRPS.textContent = state.currentRPS;

    const kpiWorkers = document.getElementById('kpi-active-workers');
    if (kpiWorkers) kpiWorkers.textContent = `${state.activeWorkers} / 50`;
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.app = new Application();
  window.app.init();
});
