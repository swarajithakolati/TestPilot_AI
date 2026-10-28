# TestPilot AI — AI-Powered Web Test Case & Bug Script Generator (PS-03)

[![Playwright](https://img.shields.io/badge/Playwright-1.49-2EAD33?logo=playwright)](https://playwright.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB?logo=react)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?logo=vite)](https://vitejs.dev/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python)](https://www.python.org/)

**TestPilot AI** is an autonomous web quality engineering platform built for modern development teams and QA engineers. It crawls any target web application, harvests interactive DOM elements and accessibility landmarks, uses hybrid AI to synthesize comprehensive QA test matrices, generates ready-to-run Playwright automation code (Python & TypeScript), executes tests with real-time browser telemetry, and autonomously generates root-cause bug reports and standalone bug reproduction scripts when defects are detected.

---

## 🎯 Key Capabilities

- 🔍 **Autonomous DOM Crawler**: Launches Playwright Chromium to inspect interactive forms, buttons, inputs, links, and accessibility trees with live full-page screenshot capture.
- 🧠 **Hybrid Intelligence Architecture**: Integrates directly with **Google Gemini 2.5 Flash** and **OpenAI GPT-4o-mini**, backed by a resilient **Offline Heuristic AST Engine** that guarantees zero-failure live demonstrations even without an API key or internet access.
- 📊 **Multi-Category Test Synthesis**: Generates high-coverage test cases across:
  - **Smoke & Happy Path** flows
  - **Boundary & Edge Cases** (zero/negative quantities, overflow values)
  - **Negative Input Validations** (malformed inputs, blank submissions)
  - **Security Probes** (XSS/SQLi payload sanitization verification)
- ⚡ **Multi-Framework Automation Hub**: Produces executable **Playwright Python** (`pytest`) and **Playwright TypeScript** (`@playwright/test`) test files with one-click copy and download.
- 🚀 **Live Browser Execution & Telemetry**: Runs tests on demand with step-by-step millisecond timing, console error capture, and support for both **Headless (Speed)** and **Headed (Visual)** modes.
- 🪲 **Autonomous Defect Analysis & Script Synthesis**: Detects runtime invariant violations, isolates the failed step, formulates a root-cause hypothesis, recommends code remediation, and exports a standalone `reproduce_bug.py` script.
- 🛡️ **Built-in Offline Testbed (`/demo/shop`)**: An integrated, zero-latency e-commerce testbed with intentional edge-case bugs ensuring a 100% flawless presentation under any Wi-Fi conditions.

---

## 🏗️ Project Architecture

```
SK_Project/
├── run.sh                          # One-click startup script (backend + frontend)
├── README.md                       # Complete documentation & demo guide
├── .gitignore                      # Git ignore rules
│
├── backend/                        # Python FastAPI Backend
│   ├── main.py                     # API Gateway, WebSocket telemetry, CORS
│   ├── config.py                   # Environment & path configuration
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Configuration template
│   ├── models/
│   │   └── schemas.py              # Pydantic data schemas
│   ├── services/
│   │   ├── crawler.py              # Playwright DOM element & screenshot harvester
│   │   ├── ai_generator.py         # Hybrid AI engine (Gemini / OpenAI / AST)
│   │   ├── test_runner.py          # Live Playwright test runner with step streaming
│   │   ├── bug_reporter.py         # Root-cause bug reporter & reproduce script generator
│   │   └── sample_apps.py          # Built-in demo store (/demo/shop)
│   └── static/
│       └── screenshots/            # Live inspection & defect snapshot store
│
└── frontend/                       # React 19 + Vite Dashboard
    ├── package.json                # Node dependencies
    ├── vite.config.js              # Vite reverse proxy configuration
    ├── index.html                  # HTML5 entry with Google typography
    └── src/
        ├── App.jsx                 # Central state coordinator
        ├── index.css               # Bespoke dark glassmorphism design system
        └── components/
            ├── Header.jsx          # Branding, model picker, headed toggle
            ├── UrlBar.jsx          # Target URL input, demo presets
            ├── DomInspector.jsx    # DOM element explorer & screenshot lightbox
            ├── TestCaseViewer.jsx  # Structured test case cards & BDD drawer
            ├── CodeViewer.jsx      # Automation script hub (Python & TS)
            ├── LiveRunner.jsx      # Real-time execution console & telemetry
            └── BugReportModal.jsx  # Defect diagnosis & reproduction script export
```

---

## 🚀 Quick Start Guide

### Option 1: One-Click Startup (Recommended)

From the project root directory, run:

```bash
./run.sh
```

This will automatically configure the Python virtual environment, install dependencies, launch the backend on port `8000`, launch the frontend on port `5173`, and open the platform.

### Option 2: Manual Startup

**1. Start the Backend:**
```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
playwright install chromium
uvicorn backend.main:app --port 8000 --reload
```

**2. Start the Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**3. Open in Browser:**
- **Dashboard UI:** [http://localhost:5173](http://localhost:5173)
- **API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Built-in Demo Shop:** [http://localhost:8000/demo/shop](http://localhost:8000/demo/shop)

---

## 🎤 Hackathon Demonstration Pitch Script (For Judges)

Follow this 3-minute sequence to demonstrate the platform to hackathon evaluators:

1. **Introduction (30s):**
   - Open [http://localhost:5173](http://localhost:5173).
   - Point out the clean architecture: *"Judges, this is TestPilot AI for Problem Statement 03. Testing web applications manually or writing scripts from scratch takes days. TestPilot AI autonomously inspects live web applications, plans test suites using AI, and actually executes them to reproduce defects."*
2. **Autonomous DOM Crawl & Test Generation (45s):**
   - Click the preset: **AeroMart Pro Store (Built-in Testbed)**.
   - Click **Generate Test Suite**.
   - Show the generated test suite: *"Within seconds, Playwright analyzed the page DOM and synthesized 5 structured test cases: Smoke, Boundary/Edge Cases, Negative Validations, and Security XSS Probes."*
   - Click the **DOM Elements** tab to highlight the harvested selector hierarchy and screenshot snapshot.
3. **Multi-Language Automation Export (30s):**
   - Click the **Automation Scripts** tab.
   - Toggle between **Playwright (Python)** and **Playwright (TypeScript)**.
   - Highlight the production-grade selectors (`data-testid`, accessible roles) and the one-click file download.
4. **Live Execution & The "Wow" Factor: Autonomous Defect Reproduction (60s):**
   - Go back to the **Test Cases** tab.
   - Click **Run Live Test** on **TC-002: Boundary & Edge Case: Zero / Negative Quantity Guard**.
   - Watch the live execution telemetry stream in real time.
   - When the test fails, observe the **Defect Report Modal** automatically open:
     - **Defect Title & Severity Badge**: Medium Defect
     - **Expected vs Actual**: Shows that quantity was allowed to drop below 1 without validation.
     - **Defect State Snapshot**: Real captured screenshot of the buggy page state.
     - **Root Cause Hypothesis & Remediation**: Specific engineering advice on clamping math handlers.
     - **Standalone Reproduction Script**: Click **Download Script** to show `reproduce_bug.py`. Explain: *"A developer can take this generated standalone script, run it in their terminal, and immediately see the exact bug reproduced in a live browser without guessing."*
5. **Conclusion (15s):**
   - Highlight the **Headed vs Headless** toggle and **Hybrid AI Engine** (works offline with zero API key dependencies or with Gemini/OpenAI).

---

## 🔒 Security & Privacy

- No API keys are hardcoded in the codebase.
- API keys can be passed in runtime headers or `.env`.
- TestPilot AI sanitizes inspection evaluations and isolates browser contexts with separate ephemeral incognito profiles.

---

## 📄 License
MIT License. Built for Hackathon PS-03 demonstration.
