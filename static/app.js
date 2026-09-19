/**
 * FOVB-AIoT Client-Side Engine (for VS Code Go Live & Standalone Mode)
 * Handles LocalStorage Database, Authentication, Live Chart.js, Kiosk Simulation & Slip Printing
 */

// Default Seed Data
const DEFAULT_USER = {
    id: 1,
    student_id: '2022-104928',
    full_name: 'Khin Andrei Gamboa',
    email: 'gamboa.khinandrei@rtu.edu.ph',
    age: 21,
    sex: 'Male',
    department: 'College of Engineering - Computer Engineering',
    phone: '+63 917 824 5612',
    rfid_uid: 'E2 80 68 31'
};

const DEFAULT_LOGS = [
    {
        id: 1,
        date: '2026-08-23',
        full_date: '2026-08-23 09:15:00',
        height: 172.0,
        weight: 66.5,
        bmi: 22.5,
        bmi_cat: 'Normal',
        temp: 36.6,
        hr: 74,
        rr: 16,
        sys: 118,
        dia: 78,
        bp_cat: 'Normal',
        spo2: 98,
        risk_score: 14.5,
        risk_level: 'Low Risk',
        ai_rec: 'All monitored vital signs and BMI are within standard healthy limits. Keep up your active lifestyle, stay properly hydrated during campus hours, and maintain balanced nutrition.',
        kiosk_id: 'RTU-PASIG-KIOSK-01'
    },
    {
        id: 2,
        date: '2026-08-30',
        full_date: '2026-08-30 10:20:00',
        height: 172.0,
        weight: 67.0,
        bmi: 22.6,
        bmi_cat: 'Normal',
        temp: 36.8,
        hr: 78,
        rr: 17,
        sys: 122,
        dia: 80,
        bp_cat: 'Elevated',
        spo2: 98,
        risk_score: 18.0,
        risk_level: 'Low Risk',
        ai_rec: 'Slightly elevated systolic blood pressure noted. Ensure adequate rest after walking to class and stay hydrated.',
        kiosk_id: 'RTU-PASIG-KIOSK-01'
    },
    {
        id: 3,
        date: '2026-09-06',
        full_date: '2026-09-06 14:05:00',
        height: 172.0,
        weight: 66.8,
        bmi: 22.6,
        bmi_cat: 'Normal',
        temp: 37.1,
        hr: 82,
        rr: 18,
        sys: 124,
        dia: 82,
        bp_cat: 'Hypertension Stage 1',
        spo2: 97,
        risk_score: 28.5,
        risk_level: 'Moderate Risk',
        ai_rec: 'Noted health observation: Hypertension Stage 1. Rest for 15-30 minutes and re-screen at the FOVB-AIoT kiosk. Limit high-caffeine energy drinks.',
        kiosk_id: 'RTU-PASIG-KIOSK-01'
    },
    {
        id: 4,
        date: '2026-09-13',
        full_date: '2026-09-13 11:30:00',
        height: 172.0,
        weight: 66.2,
        bmi: 22.4,
        bmi_cat: 'Normal',
        temp: 36.5,
        hr: 72,
        rr: 16,
        sys: 119,
        dia: 77,
        bp_cat: 'Normal',
        spo2: 99,
        risk_score: 12.0,
        risk_level: 'Low Risk',
        ai_rec: 'Blood pressure returned to optimal range (<120/<80). Respiratory rhythm and oxygen levels excellent.',
        kiosk_id: 'RTU-PASIG-KIOSK-01'
    },
    {
        id: 5,
        date: '2026-09-19',
        full_date: '2026-09-19 08:45:00',
        height: 172.0,
        weight: 66.0,
        bmi: 22.3,
        bmi_cat: 'Normal',
        temp: 36.7,
        hr: 70,
        rr: 15,
        sys: 117,
        dia: 76,
        bp_cat: 'Normal',
        spo2: 99,
        risk_score: 10.5,
        risk_level: 'Low Risk',
        ai_rec: 'All monitored vital signs and BMI are within standard healthy limits. Excellent cardiovascular recovery and stability.',
        kiosk_id: 'RTU-PASIG-KIOSK-01'
    }
];

// Database helpers
function initStorage() {
    if (!localStorage.getItem('fovb_users')) {
        localStorage.setItem('fovb_users', JSON.stringify([DEFAULT_USER]));
    }
    if (!localStorage.getItem('fovb_logs')) {
        localStorage.setItem('fovb_logs', JSON.stringify(DEFAULT_LOGS));
    }
    if (!localStorage.getItem('fovb_current_user')) {
        localStorage.setItem('fovb_current_user', JSON.stringify(DEFAULT_USER));
    }
}

function getCurrentUser() {
    initStorage();
    const data = localStorage.getItem('fovb_current_user');
    return data ? JSON.parse(data) : DEFAULT_USER;
}

function getLogs() {
    initStorage();
    const data = localStorage.getItem('fovb_logs');
    return data ? JSON.parse(data) : DEFAULT_LOGS;
}

function saveLog(log) {
    const logs = getLogs();
    logs.push(log);
    localStorage.setItem('fovb_logs', JSON.stringify(logs));
}

// Clinical Calculations
function calculateBmi(heightCm, weightKg) {
    if (!heightCm || heightCm <= 0) return { bmi: 0, cat: 'Unknown' };
    const heightM = heightCm / 100.0;
    const bmi = +(weightKg / (heightM * heightM)).toFixed(1);
    let cat = 'Normal';
    if (bmi < 18.5) cat = 'Underweight';
    else if (bmi < 23.0) cat = 'Normal';
    else if (bmi < 25.0) cat = 'Overweight';
    else cat = 'Obese';
    return { bmi, cat };
}

function classifyBp(sys, dia) {
    if (sys >= 180 || dia >= 120) return 'Hypertensive Crisis';
    if (sys >= 140 || dia >= 90) return 'Hypertension Stage 2';
    if (sys >= 130 || dia >= 80) return 'Hypertension Stage 1';
    if (sys >= 120 && dia < 80) return 'Elevated';
    if (sys < 90 || dia < 60) return 'Hypotension';
    return 'Normal';
}

function calculateAiRisk(temp, hr, rr, sys, dia, spo2, bmi) {
    let points = 0;
    const flags = [];

    if (temp > 38.3 || temp < 35.5) { points += 25; flags.push('Critical Body Temperature'); }
    else if (temp > 37.5) { points += 15; flags.push('Low-grade Fever / Hyperthermia'); }
    else if (temp < 36.2) { points += 10; flags.push('Mild Hypothermia'); }

    if (sys >= 180 || dia >= 120) { points += 35; flags.push('Hypertensive Crisis'); }
    else if (sys >= 140 || dia >= 90) { points += 25; flags.push('Hypertension Stage 2'); }
    else if (sys >= 130 || dia >= 80) { points += 15; flags.push('Hypertension Stage 1'); }
    else if (sys >= 120 && dia < 80) { points += 8; flags.push('Elevated Blood Pressure'); }
    else if (sys < 90 || dia < 60) { points += 15; flags.push('Hypotension'); }

    if (hr > 115) { points += 20; flags.push('Significant Tachycardia'); }
    else if (hr > 100) { points += 12; flags.push('Mild Tachycardia'); }
    else if (hr < 50) { points += 20; flags.push('Bradycardia'); }
    else if (hr < 60) { points += 8; flags.push('Low Heart Rate'); }

    if (spo2 <= 90) { points += 30; flags.push('Severe Hypoxemia'); }
    else if (spo2 <= 94) { points += 18; flags.push('Mild Hypoxemia'); }

    if (rr > 24) { points += 20; flags.push('Tachypnea'); }
    else if (rr > 20) { points += 10; flags.push('Elevated Respiratory Rate'); }
    else if (rr < 10) { points += 20; flags.push('Bradypnea'); }

    if (bmi >= 30.0) { points += 15; flags.push('Obesity Risk'); }
    else if (bmi >= 25.0) { points += 8; flags.push('Overweight Risk'); }
    else if (bmi < 18.5) { points += 8; flags.push('Underweight Risk'); }

    const riskScore = Math.min(+(points * 0.9).toFixed(1), 100.0);
    let riskLevel = 'Low Risk';
    let rec = "All monitored vital signs and BMI are within standard healthy limits. Keep up your active lifestyle, stay properly hydrated during campus hours, and maintain balanced nutrition.";

    if (riskScore < 25.0) {
        riskLevel = 'Low Risk';
    } else if (riskScore < 50.0) {
        riskLevel = 'Moderate Risk';
        const str = flags.length ? flags.join(', ') : 'Mild vital sign deviation';
        rec = `Noted health observation: ${str}. Rest for 15-30 minutes and re-screen at the FOVB-AIoT kiosk. Limit high-caffeine energy drinks and consult the RTU Pasig Clinic nurse if readings remain atypical.`;
    } else {
        riskLevel = 'High Risk';
        const str = flags.length ? flags.join(', ') : 'Significant vital anomalies detected';
        rec = `URGENT ATTENTION: ${str}. Your multi-parameter health prediction indicates acute strain. Please report directly to the RTU Pasig Clinic (Ground Floor) or nearest healthcare provider for clinical evaluation.`;
    }

    return { riskScore, riskLevel, rec };
}

// Update Dynamic Navbar across all pages
function updateNavbar() {
    initStorage();
    const user = getCurrentUser();
    const authArea = document.getElementById('navbarAuthArea');
    if (!authArea) return;

    if (user) {
        authArea.innerHTML = `
            <li class="nav-user-item">
                <a href="dashboard.html" class="nav-btn-dashboard"><i class="fas fa-chart-line"></i> Dashboard</a>
            </li>
            <li class="nav-user-profile">
                <span class="user-greeting"><i class="fas fa-id-card-clip"></i> ${user.full_name.split(' ')[0]}</span>
                <a href="javascript:void(0)" onclick="logoutUser()" class="nav-btn-logout" title="Sign Out"><i class="fas fa-arrow-right-from-bracket"></i></a>
            </li>
        `;
    } else {
        authArea.innerHTML = `
            <li><a href="login.html" class="nav-link-login">Sign In</a></li>
            <li><a href="register.html" class="btn-nav-cta"><i class="fas fa-user-plus"></i> Register</a></li>
        `;
    }
}

function logoutUser() {
    localStorage.removeItem('fovb_current_user');
    window.location.href = 'index.html';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initStorage();
    updateNavbar();
    const toggle = document.getElementById('menuToggle');
    const links = document.getElementById('navLinks');
    if (toggle && links) {
        toggle.addEventListener('click', () => links.classList.toggle('active'));
    }
});
