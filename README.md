# FOVB-AIoT Thesis Archive & Student Health Portal
**Four-in-One Vital Sign Sensors with BMI Calculation using AI and IoT for Health Prediction in RTU Pasig Clinic**

An undergraduate capstone thesis project presented to the Faculty of the **College of Engineering, Department of Computer Engineering**, Rizal Technological University (RTU), Pasig Campus.

---

## 🇵🇭 Project Overview & Research Context

**FOVB-AIoT** serves as the **Thesis Memorial & Documentation Archive** and **Student Health History Portal** for the RTU Pasig Clinic capstone research. It provides a permanent, accessible digital record of the engineering journey, academic paper, team memories, and longitudinal student vital signs history.

> [!NOTE]
> **System & Hardware Boundaries:**
> - **The Web Portal (This Website):** A permanent documentation, thesis memory, and student health history dashboard. It has **no directly wired microcontrollers or sensor circuits**.
> - **The Physical Kiosk Station:** Installed on-site at the RTU Pasig Clinic. The physical kiosk contains the custom sensor cluster, dual microcontrollers, and touchscreen system where patients perform physical screenings.
> - **USB RFID Registration:** The sole hardware interaction supported on this web portal is a standard **plug-and-play USB RFID reader** (HID keyboard emulation) plugged directly into your laptop or PC USB port, allowing convenient scanning of RTU ID cards during student account registration.

### The Physical FOVB-AIoT Kiosk Station (RTU Pasig Clinic)
1. **Non-Contact Core Temperature:** MLX90614 Infrared optical sensor (±0.2 °C accuracy, 100% hygienic zero-touch operation).
2. **Pulse Oximetry (Heart Rate & Respiratory Rate):** MAX30102 Photoplethysmography (PPG) optical sensor measuring Heart Rate (BPM), blood Oxygen Saturation (SpO2 %), and derived respiratory rhythm.
3. **Blood Pressure (AI Computer Vision):** Digital blood pressure cuff monitored by an HD webcam using a custom-trained **YOLO** object detection model running on the Mini PC to extract systolic, diastolic, and pulse readings from the LCD.
4. **Automated Anthropometric BMI:** TF-Luna LiDAR laser time-of-flight sensor for overhead height measurement combined with four HX711 industrial load cells for weight, auto-computing Asia-Pacific WHO Body Mass Index.
5. **Fast-Track Contactless RFID:** RC522 13.56 MHz RFID reader on the physical kiosk console allowing students and faculty to tap their ID card to complete screening in under 60 seconds without retyping credentials.
6. **Central Processing Unit:** Dell Mini PC (Intel Core i5 10th Gen) coupled with an Arduino Mega 2560 and Arduino Nano dual-controller setup, integrated with an embedded thermal slip printer.

---

## 🌐 Web Portal Features

- **Minimalist White Health Theme with Pinoy Culture & Medical Red Accents:**
  - Modern, clinical white layout (`#ffffff`, `#f8fafc`) with vitality crimson red accents (`#d32f2f`).
  - Subtle Philippine cultural touches: micro tricolor ribbon, Baybayin accent badge (*ᜃᜎᜓᜐᜓ4ᜈ᜔*), and warm welcoming Filipino tone (*"Kumusta, Ka-RTU! Bantay-Kalusugan para sa bawat Juan"*).
  - Highlights the official project logo (`pictures/logo.png`) and kiosk prototype imagery (`pictures/hero-image.png`).

- **Thesis Documentation & Memorial Pages:**
  - **Home (`/` or `index.html`):** Capstone project overview, physical kiosk architecture showcase, WHO/DOH vital sign benchmarks, and registration CTAs.
  - **About Thesis (`/about` or `about.html`):** Complete capstone paper abstract, hardware breakdown, full research PDF download link, and researcher profiles (Alcantara, Berongoy, Gamboa, Llona, Oavenada, Relevo, Sagadraca).
  - **Kiosk Guide & Instructions (`/instructions` or `instructions.html`):** Step-by-step user manual for the physical kiosk, pre-screening guidelines, and clinical FAQs.
  - **Clinic & Contact (`/contact` or `contact.html`):** RTU Pasig Clinic hours, campus location (M. Eusebio Avenue, Maybunga, Pasig City), emergency contacts, and inquiry submission.

- **Student Account & USB RFID Registration:**
  - **Sign Up (`/register` or `register.html`):** Online registration supporting RTU Student/Employee ID, college/department selection, and automatic RFID UID detection via any USB RFID reader plugged into your laptop/PC (or one-click demo UID generation).
  - **Sign In (`/login` or `login.html`):** Authentication via Student ID, Email, or 4-byte RFID UID. Includes a **1-Click Demo Student Login** button for rapid thesis presentations.

- **Student Health History Dashboard (`/dashboard` or `dashboard.html`):**
  - **Digital RFID Health Pass:** Smart NFC pass graphic displaying user details, RFID UID, and scannable QR code.
  - **6 Vital Metric Cards:** Color-coded clinical status badges for Temperature, Blood Pressure, Heart Rate, Respiratory Rate, SpO2, and BMI.
  - **AI Health Risk Prediction Gauge:** Comprehensive Risk Score (0–100%) with animated meter and personalized recommendations for RTU Pasig Clinic.
  - **Interactive Longitudinal Charts (Chart.js):** Switchable graph tabs for Blood Pressure trends, BMI progression, and Heart Rate/SpO2 stability.
  - **Screening History Log:** Complete log of past kiosk checkup sessions.
  - **Sample Kiosk Record Sync (Demo Preview):** Interactive preview modal to test how records synchronized from the physical kiosk appear on the dashboard.
  - **Printable Official RTU Clinic Health Slip:** Printable medical slip with university branding, vital readings table, AI remarks, and Nurse signature block (`Ctrl+P` or click Print).

- **Kiosk Sync REST API (Flask Mode):**
  - `GET /api/kiosk/rfid/<uid>`: Looks up registered patient record on RFID tap.
  - `POST /api/kiosk/checkup`: Ingests telemetry synchronized from the physical kiosk, computes the AI risk score, records the session, and generates thermal slip text.
  - `GET /api/stats`: Real-time public telemetry statistics.

---

## 🚀 How to Run the Web Application

### Option A: Python Flask Server (Recommended, Port 5000)
1. **One-Click Run (Windows):** Simply double-click `run.bat` in the project root directory.
2. **Or via Terminal:**
   ```bash
   pip install flask
   python app.py
   ```
3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

### Option B: VS Code Live Server ("Go Live", Port 5500)
If you prefer running without Python/Flask:
1. In VS Code, right-click `index.html`.
2. Click **"Open with Live Server"** (runs on port 5500).
3. The application runs client-side using browser `localStorage` and demo mock data, with zero infinite redirect loops.

### 4. Testing & Account Access
- **Public Access & Open Documentation:** Visitors can freely explore the system documentation, engineering journey, and download the full research paper PDF without logging in.
- **Personal Accounts:** Visitors can click **Register** to create their own personal account, receive a unique RFID token, and record/view their own checkup history.
- **Pre-configured Demo Student (for Thesis Evaluation):**
  - **Identifier:** `DEMO-2026-01` (or `demo.student@rtu.edu.ph` or RFID: `E2 80 68 31`)
  - **Password:** `password123`
  - *(Alternatively, click the **1-Click Demo Student Login** button on the Sign In page to evaluate sample multi-month clinical trend data)*

---

## 👥 Authors & Researchers
- **Mar Kevin P. Alcantara** — Full-Stack IoT & Software Development, System Integration
- **Bernie C. Berongoy** — Sensor Calibration & Testing, Research, Hardware
- **Khin Andrei R. Gamboa** — Software Development, Research & Data Management, Clinical Validation & Analysis
- **Reymart G. Llona** — Firmware & Arduino Control, Sensor Calibration & Testing, Hardware
- **Erick John A. Oavenada** — AI Vision Development, Hardware
- **Paul Andrew A. Relevo** — Sensor Calibration & Testing, Hardware
- **Yuri Lorenz C. Sagadraca** — Software Development, Sensor Calibration & Testing

**Rizal Technological University — Pasig Campus**  
*College of Engineering • Computer Engineering Department*
