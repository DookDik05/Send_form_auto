/**
 * AutoForm Pro Max - Reactive Store & Telemetry Engine
 */

import { CAMPAIGN_PRESETS } from './data/presets.js';

class StateStore {
  constructor() {
    this.state = {
      activeTab: "dashboard",
      soundEnabled: true,
      currentCampaign: CAMPAIGN_PRESETS[0],
      customFormSchema: null,
      
      // Global Telemetry Counters
      totalSubmissions: 2840,
      totalSuccess: 2824,
      totalFailed: 16,
      totalRateLimited: 5,
      activeWorkers: 0,
      currentRPS: 0,
      avgLatencyMs: 245,

      // Live Mission State
      missionStatus: "idle", // "idle" | "running" | "paused" | "completed"
      missionProgress: {
        sent: 0,
        target: 150,
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
        { time: "09:45:12", type: "info", msg: "AutoForm Pro Max v2.4 Engine initialized." },
        { time: "09:45:13", type: "info", msg: "Proxy pool ready. User-Agent rotation enabled (120 signatures)." },
        { time: "09:45:15", type: "ok", msg: "Initial session established with Google Forms endpoint." }
      ],

      // Historical Campaign Records
      historyRecords: [
        { id: "RUN-890", name: "Registration 890 Batch", date: "2026-01-11 18:45", count: 890, success: 890, failed: 0, engine: "HTTPX Async", status: "SUCCESS" },
        { id: "RUN-782", name: "SEA Games Survey 33", date: "2026-01-11 17:32", count: 120, success: 119, failed: 1, engine: "Selenium Headless", status: "COMPLETED" },
        { id: "RUN-650", name: "FDA Expo 2026", date: "2026-01-23 11:41", count: 300, success: 298, failed: 2, engine: "HTTPX Async", status: "COMPLETED" },
        { id: "RUN-512", name: "Mall Satisfaction Survey", date: "2025-12-14 18:59", count: 105, success: 105, failed: 0, engine: "HTTPX Async", status: "SUCCESS" }
      ]
    };

    this.listeners = new Set();
  }

  getState() {
    return this.state;
  }

  setState(partial) {
    this.state = { ...this.state, ...partial };
    this.notify();
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notify() {
    for (const listener of this.listeners) {
      listener(this.state);
    }
  }

  addLog(type, msg) {
    const now = new Date();
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
    const logItem = { time: timeStr, type, msg };
    
    const nextLogs = [...this.state.logs.slice(-250), logItem];
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
