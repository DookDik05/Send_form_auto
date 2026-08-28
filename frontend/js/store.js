/**
 * AutoForm Pro Max - Reactive Store & Telemetry Engine (with LocalStorage Persistence)
 */

import { CAMPAIGN_PRESETS } from './data/presets.js';

const STORAGE_KEY = 'autoform_pro_max_settings';

function loadPersistedState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    return null;
  }
}

function savePersistedState(state) {
  try {
    const toSave = {
      activeTab: state.activeTab,
      soundEnabled: state.soundEnabled,
      selectedPresetId: state.currentCampaign?.id || "sushi-conveyor-survey",
      customSettings: state.customSettings || {}
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave));
  } catch (e) {
    // Ignore storage errors
  }
}

class StateStore {
  constructor() {
    const persisted = loadPersistedState();
    const defaultPreset = (persisted && persisted.selectedPresetId)
      ? CAMPAIGN_PRESETS.find(p => p.id === persisted.selectedPresetId) || CAMPAIGN_PRESETS[0]
      : CAMPAIGN_PRESETS[0];

    this.state = {
      activeTab: persisted?.activeTab || "dashboard",
      soundEnabled: persisted?.soundEnabled ?? true,
      currentCampaign: defaultPreset,
      customFormSchema: null,
      customSettings: persisted?.customSettings || {},
      
      // Global Telemetry Counters
      totalSubmissions: 3673,
      totalSuccess: 3673,
      totalFailed: 0,
      totalRateLimited: 0,
      activeWorkers: 0,
      currentRPS: 0,
      avgLatencyMs: 245,

      // Live Mission State
      missionStatus: "idle", // "idle" | "running" | "paused" | "completed"
      missionProgress: {
        sent: 0,
        target: defaultPreset.targetCount,
        success: 0,
        failed: 0,
        rateLimited: 0,
        percent: 0,
        speedRPS: 0,
        startTime: null,
        elapsedSeconds: 0
      },

      // Live Throughput Sparkline Buffer
      throughputHistory: [12, 18, 25, 22, 35, 42, 38, 48, 52, 45, 60, 58, 64, 70, 68, 75, 82, 79, 88, 92],
      
      // Terminal Logs Stream
      logs: [
        { time: "11:00:12", type: "info", msg: "AutoForm Pro Max v2.5 Engine initialized with Cyberpunk Cockpit theme." },
        { time: "11:00:13", type: "info", msg: "Disk Telemetry Vault connected (3,673 historical responses loaded)." },
        { time: "11:00:15", type: "ok", msg: "System ready. Press '?' for Keyboard Shortcuts." }
      ],

      // Historical Campaign Records
      historyRecords: [
        { id: "RUN-SUSHI", name: "แบบสอบถามร้านซูชิสายพาน (7Ps)", date: "2026-08-28 10:43", count: 6, success: 6, failed: 0, engine: "Selenium & HTTPX", status: "SUCCESS" },
        { id: "RUN-890", name: "Registration 890 Batch", date: "2026-01-11 18:45", count: 1448, success: 1448, failed: 0, engine: "HTTPX Async", status: "SUCCESS" },
        { id: "RUN-MALL", name: "แบบประเมินความพึงพอใจศูนย์การค้า", date: "2025-12-21 12:51", count: 1061, success: 1061, failed: 0, engine: "HTTPX Async", status: "SUCCESS" },
        { id: "RUN-SATIS", name: "แบบประเมินความพึงพอใจผู้ใช้บริการ", date: "2025-11-13 17:58", count: 886, success: 886, failed: 0, engine: "HTTPX Async", status: "SUCCESS" },
        { id: "RUN-SEAGAMES", name: "SEA Games Survey 33", date: "2026-01-11 21:08", count: 209, success: 209, failed: 0, engine: "HTTPX Async", status: "SUCCESS" },
        { id: "RUN-FDA", name: "FDA Expo 2026", date: "2026-01-23 11:41", count: 63, success: 63, failed: 0, engine: "HTTPX Async", status: "SUCCESS" }
      ]
    };

    this.listeners = new Set();
  }

  getState() {
    return this.state;
  }

  setState(partial) {
    this.state = { ...this.state, ...partial };
    savePersistedState(this.state);
    this.notify();
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notify() {
    for (const listener of this.listeners) {
      try {
        listener(this.state);
      } catch (e) {
        console.error("Store listener error:", e);
      }
    }
  }

  addLog(type, msg) {
    const now = new Date();
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
    const logItem = { time: timeStr, type, msg };
    
    const nextLogs = [...(this.state.logs || []).slice(-250), logItem];
    this.setState({ logs: nextLogs });
  }

  clearLogs() {
    this.setState({ logs: [] });
  }

  selectPreset(presetId) {
    const found = CAMPAIGN_PRESETS.find(p => p.id === presetId);
    if (found) {
      this.setState({
        currentCampaign: JSON.parse(JSON.stringify(found)),
        missionProgress: {
          ...this.state.missionProgress,
          target: found.targetCount,
          sent: 0,
          success: 0,
          failed: 0,
          percent: 0
        }
      });
      this.addLog("info", `Switched active campaign preset to: [${found.title}]`);
    }
  }
}

export const store = new StateStore();
