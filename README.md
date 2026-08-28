# 🚀 AutoForm Pro Max — Google Forms Automation Cockpit

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/architecture-Senior%20Modular-cyan.svg)]()
[![UI Theme](https://img.shields.io/badge/theme-Neo%20Glassmorphism-purple.svg)]()

**AutoForm Pro Max** is an enterprise-grade Google Forms automation platform featuring:
- **Dual Execution Engines:** Async HTTPX (high-concurrency 50–200 rps) & Selenium Humanizer (real Chrome browser emulation with natural cursor movements).
- **Statistical Persona Simulation:** Correlated Likert ratings across marketing mix (7Ps) and consumer behaviors.
- **Form Inspector & Reverse-Engineer:** Auto-parses entry IDs, types, and choice validation rules from live Google Form URLs.
- **Cyberpunk Web Cockpit UI:** Real-time dispatch telemetry, precision delay controls, interactive Selenium live viewport, and per-form historical data vault.

---

## 📁 Senior-Grade Project Architecture

```
Send_form_auto/
├── src/                          # 🧠 Core Python Engine & Logic
│   ├── core/                     # Shared Foundations
│   │   ├── http_client.py        # Async HTTPX Client with Client Hints rotation
│   │   ├── persona_engine.py     # Statistical Likert correlation & persona archetypes
│   │   └── selenium_driver.py    # Chrome Humanizer & Stealth options
│   │
│   ├── runners/                  # Specific Form Automation Runners
│   │   └── sushi_runner.py       # Conveyor Belt Sushi Survey (7Ps & Behavior)
│   │
│   └── utils/                    # Shared Utilities
│       ├── console.py            # Cross-platform UTF-8 console output
│       └── csv_manager.py        # Result exporter & live disk telemetry scanner
│
├── data/                         # 💾 Structured Data & Artifacts
│   ├── results/                  # All generated CSV result files
│   ├── schemas/                  # Extracted JSON schemas of Google Forms
│   └── mocks/                    # Mock participant profiles & test records
│
├── frontend/                     # 🖥️ Modern Web Cockpit Dashboard
│   ├── index.html                # Single-Page Cockpit Application
│   ├── css/                      # Modular Dark Neo-Glassmorphism CSS
│   │   ├── design-tokens.css
│   │   ├── layout.css
│   │   └── components.css
│   └── js/                       # Vanilla ES6 Modular Javascript
│       ├── app.js
│       ├── store.js
│       ├── data/                 # Thai names, provinces, and presets
│       └── modules/              # Dashboard, Dispatcher, Inspector, Analytics
│
├── main.py                       # ⚡ Central CLI Entrypoint
├── run_ui.py                     # 📡 Local Web UI & Telemetry API Server
├── requirements.txt              # Pinned Python Dependencies
└── README.md                     # Documentation
```

---

## 🚀 Quick Start

### 1. Installation
```powershell
pip install -r requirements.txt
```

### 2. Launching the Web Cockpit Dashboard
```powershell
python run_ui.py
# or
python main.py ui
```
Opens the web dashboard at `http://127.0.0.1:3000` (or the next available port).

---

## 💻 CLI Commands

### View Live Telemetry Stats (Scanned from Disk)
```powershell
python main.py stats
```

### List Registered Forms
```powershell
python main.py list
```

### Run Async HTTPX Automation
```powershell
# Default Human Mode (50 submissions, 5 coroutines)
python main.py run sushi --count 50 --concurrency 5 --mode human

# Stealth Anti-Detect Mode (longer human delays)
python main.py run sushi --count 30 --concurrency 3 --mode stealth

# Turbo Fast Mode (high performance)
python main.py run sushi --count 100 --concurrency 10 --mode fast
```

### Run Selenium Browser Automation
```powershell
# Headless Chrome
python main.py selenium sushi --count 5

# Visual Chrome (opens live Chrome window)
python main.py selenium sushi --count 2 --visual
```

---

## 🧠 Human Persona Modeling

Submissions are not generated with raw, disconnected random choices. The **Persona Engine** distributes answers across 4 distinct behavioral archetypes:

1. **🍣 Super Fan / Sushi Lover (55%):** Scores 5 in Freshness, Taste, Cleanliness, and Revisit intent.
2. **🚶 Satisfied Pragmatist (30%):** Base rating of 4 stars with highlights in top service aspects.
3. **💰 Value-Conscious Diner (10%):** Sensitive to pricing and promotions (3–4 stars), high food ratings.
4. **🔍 Critical Quality Inspector (5%):** Strict evaluations across all 7Ps.

---

## 📄 License
MIT License. Created for professional survey research and automated quality testing.
