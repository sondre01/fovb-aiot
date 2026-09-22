# 🌐 FOVB-AIoT Standalone Client-Side Preview (VS Code Live Server)

This directory contains the zero-backend, client-side static edition of the **FOVB-AIoT** web portal.

---

## 🚀 How to Run

### Method 1: VS Code Live Server ("Go Live")
1. In VS Code, navigate to this folder (`standalone/`).
2. Right-click on [`index.html`](file:///C:/Users/gambo/repos/FOVB-AIoT/standalone/index.html).
3. Select **"Open with Live Server"** (runs locally on port `5500`).

### Method 2: Direct File Execution
Double-click [`index.html`](file:///C:/Users/gambo/repos/FOVB-AIoT/standalone/index.html) in Windows Explorer to open it directly in any modern web browser (`file:///` protocol).

---

## ⚙️ Architecture & Data Storage
- **Zero Python / Flask Required:** Runs entirely client-side using HTML5, CSS3, and JavaScript.
- **Client-Side Persistence:** Session authentication, RFID card linking, kiosk checkup simulations, and historical health records are managed in the browser's `localStorage` via [`static/app.js`](file:///C:/Users/gambo/repos/FOVB-AIoT/static/app.js).
- **Demo Student Preset:** Pre-loaded with demo student `DEMO-2026-01` and sample historical telemetry for offline presentations and evaluation.
