# FOVB-AIoT Web Portal & Health Prediction System
**Four-in-One Vital Sign Sensors with BMI Calculation using AI and IoT for Health Prediction in RTU Pasig Clinic**

An undergraduate capstone thesis project presented to the Faculty of the **College of Engineering, Department of Computer Engineering**, Rizal Technological University (RTU), Pasig Campus.

---

## 🇵🇭 Project Overview & Research Context

**FOVB-AIoT** is an automated kiosk and web-based health screening platform engineered to modernize health monitoring at the **RTU Pasig Clinic**. The system integrates physical medical sensors, dual microcontrollers, artificial intelligence computer vision, and an IoT web database to eliminate manual vitals logging, decrease queuing times, and provide automated clinical risk predictions.

### Key Hardware & AI Architecture
1. **Body Temperature:** MLX90614 Non-Contact Infrared Sensor (±0.2 °C accuracy, 100% hygienic zero-touch operation).
2. **Pulse Oximetry (Heart Rate & Respiratory Rate):** MAX30102 Photoplethysmography (PPG) optical sensor measuring Heart Rate (BPM), blood Oxygen Saturation (SpO2 %), and derived respiratory rhythm.
3. **Blood Pressure (AI Computer Vision):** Digital blood pressure cuff monitored by an HD webcam using a custom-trained **YOLO** object detection model running on the Mini PC to extract systolic, diastolic, and pulse readings from the LCD.
4. **Automated Anthropometric BMI:** TF-Luna LiDAR laser time-of-flight sensor for overhead height measurement combined with four HX711 industrial load cells for weight, auto-computing Asia-Pacific WHO Body Mass Index.
5. **Fast-Track Contactless RFID:** RC522 13.56 MHz RFID reader allowing students and faculty to tap their ID card to complete screening in under 60 seconds without retyping credentials.
6. **Central Processing:** Dell Mini PC (Intel Core i5 10th Gen) coupled with an Arduino Mega 2560 and Arduino Nano dual-controller setup, integrated with an embedded thermal slip printer.

---

## 🌐 Web System Features & Advertising Portal

- **Minimalist White Health Theme with Pinoy Culture & Medical Red Accents:**
  - Modern, clinical white layout (`#ffffff`, `#f8fafc`) with vitality crimson red accents (`#d32f2f`).
  - Subtle Philippine cultural touches: micro tricolor ribbon, Baybayin accent badge (*ᜃᜎᜓᜐᜓ4ᜈ᜔*), and warm welcoming Filipino tone (*"Kumusta, Ka-RTU! Bantay-Kalusugan para sa bawat Juan"*).
  - Highlighting your project's `pictures/logo.png` and `pictures/hero-image.png` prototype kiosk visual.

- **Informational & Advertising Pages:**
  - **Home (`/`):** High-converting showcase detailing the 4-in-1 sensor architecture, step-by-step kiosk workflow, WHO/DOH Philippines vital sign normal ranges, and registration calls-to-action.
  - **About Thesis (`/about`):** Complete capstone paper abstract, system architecture breakdown, hardware specifications, and researcher profiles (Alcantara, Berongoy, Gamboa, Llona, Oavenada, Relevo, Sagadraca).
  - **Kiosk Guide & Instructions (`/instructions`):** Visual user manual for students and faculty, pre-screening recommendations, step-by-step kiosk operation, and FAQs.
  - **Clinic & Contact (`/contact`):** RTU Pasig Clinic hours, campus location (M. Eusebio Avenue, Maybunga, Pasig City), emergency contacts, and message submission.

- **Online User Account Management:**
  - **Sign Up (`/register`):** Fast online registration with RTU Student/Employee ID, college/department selection, and automatic or manual RFID card UID linking. Includes an auto-fill button for quick testing.
  - **Sign In (`/login`):** Flexible authentication via Student ID, Email, or 4-byte RFID UID. Includes a **1-Click Demo Student Login** button for instant thesis defense presentations.

- **Interactive User Health Dashboard (`/dashboard`):**
  - **Digital RFID Health Pass:** Smart NFC pass graphic displaying the user's details, RFID UID, and scannable QR code.
  - **6 Real-time Vital Metric Cards:** Color-coded clinical status badges for Temperature, Blood Pressure, Heart Rate, Respiratory Rate, SpO2, and BMI.
  - **AI Health Risk Prediction Gauge:** Comprehensive Risk Score (0–100%) with animated meter and personalized clinical recommendation tailored to RTU Pasig Clinic.
  - **Interactive Longitudinal Charts (Chart.js):** Switchable graph tabs for Blood Pressure trends, BMI/Weight progression, and Heart Rate/SpO2 stability.
  - **Screening History Table:** Full log of past sessions with kiosk station stamps.
  - **Simulate Kiosk Checkup Modal:** Built-in interactive simulator to test how new sensor readings flow into the dashboard (includes Healthy, Fever, and High BP presets).
  - **Printable Official RTU Clinic Health Slip:** Professional printable medical slip with university branding, vital readings table, AI remarks, and Nurse signature block (`Ctrl+P` or click Print).
  - **RFID Tag Manager:** Modal to update or re-link physical RFID tags.

- **IoT Hardware REST API:**
  - `GET /api/kiosk/rfid/<uid>`: Looks up patient record on RFID tap.
  - `POST /api/kiosk/checkup`: Ingests sensor data from Arduino/Mini-PC, runs the AI risk model, stores the record, and returns thermal slip printable text.
  - `GET /api/stats`: Real-time public telemetry statistics.

---

## 🚀 How to Run the Web Application

### 1. Requirements
Ensure Python 3.10+ and Flask are installed (already present in your environment):
```bash
pip install flask
```

### 2. Start the Server
From the project folder (`C:\Users\gambo\repos\FOVB-AIoT`):
```bash
python app.py
```

### 3. Open in Browser
Visit:
```
http://127.0.0.1:5000
```

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
