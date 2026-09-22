import os
import sqlite3
import random
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'fovb-aiot-rtu-pasig-clinic-secure-key-2026')

DB_PATH = os.path.join(os.path.dirname(__file__), 'fovb_aiot.db')

# Route to serve pictures folder directly if requested as /pictures/...
@app.route('/pictures/<path:filename>')
def serve_pictures(filename):
    pictures_dir = os.path.join(os.path.dirname(__file__), 'pictures')
    if os.path.exists(os.path.join(pictures_dir, filename)):
        return send_from_directory(pictures_dir, filename)
    static_pics = os.path.join(os.path.dirname(__file__), 'static', 'pictures')
    if os.path.exists(os.path.join(static_pics, filename)):
        return send_from_directory(static_pics, filename)
    return send_from_directory(pictures_dir, filename)

# Route to serve documents folder (e.g. final research paper PDF) directly
@app.route('/documents/<path:filename>')
def serve_documents(filename):
    docs_dir = os.path.join(os.path.dirname(__file__), 'documents')
    return send_from_directory(docs_dir, filename)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            age INTEGER,
            sex TEXT,
            department TEXT,
            phone TEXT,
            rfid_uid TEXT UNIQUE,
            role TEXT DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Checkup Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checkup_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            checkup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            height_cm REAL,
            weight_kg REAL,
            bmi REAL,
            bmi_category TEXT,
            temperature REAL,
            heart_rate INTEGER,
            respiratory_rate INTEGER,
            bp_systolic INTEGER,
            bp_diastolic INTEGER,
            bp_category TEXT,
            spo2 INTEGER,
            risk_score REAL,
            risk_level TEXT,
            ai_recommendation TEXT,
            kiosk_id TEXT DEFAULT 'RTU-PASIG-KIOSK-01',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Contact Inquiries Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()

    # Seed demo user and checkup history if empty
    cursor.execute('SELECT COUNT(*) as count FROM users')
    if cursor.fetchone()['count'] == 0:
        seed_demo_data(conn)

    conn.close()

def seed_demo_data(conn):
    cursor = conn.cursor()
    # Demo Student
    demo_pw = generate_password_hash('password123')
    cursor.execute('''
        INSERT INTO users (student_id, full_name, email, password_hash, age, sex, department, phone, rfid_uid, role)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'DEMO-2026-01',
        'Demo Student',
        'demo.student@rtu.edu.ph',
        demo_pw,
        21,
        'Male',
        'College of Engineering - Computer Engineering',
        '+63 917 824 5612',
        'E2 80 68 31',
        'student'
    ))
    user_id = cursor.lastrowid

    # Seed historical checkups across past months
    sample_records = [
        {
            'days_ago': 28,
            'height': 172.0,
            'weight': 66.5,
            'temp': 36.6,
            'hr': 74,
            'rr': 16,
            'sys': 118,
            'dia': 78,
            'spo2': 98
        },
        {
            'days_ago': 21,
            'height': 172.0,
            'weight': 67.0,
            'temp': 36.8,
            'hr': 78,
            'rr': 17,
            'sys': 122,
            'dia': 80,
            'spo2': 98
        },
        {
            'days_ago': 14,
            'height': 172.0,
            'weight': 66.8,
            'temp': 37.1,
            'hr': 82,
            'rr': 18,
            'sys': 124,
            'dia': 82,
            'spo2': 97
        },
        {
            'days_ago': 7,
            'height': 172.0,
            'weight': 66.2,
            'temp': 36.5,
            'hr': 72,
            'rr': 16,
            'sys': 119,
            'dia': 77,
            'spo2': 99
        },
        {
            'days_ago': 1,
            'height': 172.0,
            'weight': 66.0,
            'temp': 36.7,
            'hr': 70,
            'rr': 15,
            'sys': 117,
            'dia': 76,
            'spo2': 99
        }
    ]

    for rec in sample_records:
        bmi, bmi_cat = calculate_bmi(rec['height'], rec['weight'])
        bp_cat = classify_bp(rec['sys'], rec['dia'])
        risk_score, risk_level, ai_rec = calculate_ai_risk(
            rec['temp'], rec['hr'], rec['rr'], rec['sys'], rec['dia'], rec['spo2'], bmi
        )
        checkup_time = (datetime.now() - timedelta(days=rec['days_ago'], hours=random.randint(1, 5))).strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
            INSERT INTO checkup_logs (
                user_id, checkup_date, height_cm, weight_kg, bmi, bmi_category,
                temperature, heart_rate, respiratory_rate, bp_systolic, bp_diastolic,
                bp_category, spo2, risk_score, risk_level, ai_recommendation, kiosk_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, checkup_time, rec['height'], rec['weight'], bmi, bmi_cat,
            rec['temp'], rec['hr'], rec['rr'], rec['sys'], rec['dia'],
            bp_cat, rec['spo2'], risk_score, risk_level, ai_rec, 'RTU-PASIG-KIOSK-01'
        ))

    conn.commit()

# Clinical Calculations
def calculate_bmi(height_cm, weight_kg):
    if not height_cm or height_cm <= 0:
        return 0, 'Unknown'
    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m * height_m), 1)
    if bmi < 18.5:
        category = 'Underweight'
    elif bmi < 23.0:
        category = 'Normal'
    elif bmi < 25.0:
        category = 'Overweight (Pre-obese)'
    else:
        category = 'Obese'
    return bmi, category

def classify_bp(systolic, diastolic):
    if systolic >= 180 or diastolic >= 120:
        return 'Hypertensive Crisis'
    elif systolic >= 140 or diastolic >= 90:
        return 'Hypertension Stage 2'
    elif systolic >= 130 or diastolic >= 80:
        return 'Hypertension Stage 1'
    elif systolic >= 120 and diastolic < 80:
        return 'Elevated'
    elif systolic < 90 or diastolic < 60:
        return 'Hypotension'
    else:
        return 'Normal'

def calculate_ai_risk(temp, hr, rr, sys, dia, spo2, bmi):
    """
    FOVB-AIoT AI Comprehensive Health Risk Prediction Model:
    Evaluates multi-modal physiological vital signs captured by sensors and AI OCR.
    """
    points = 0
    flags = []

    # 1. Temperature (°C)
    if temp > 38.3 or temp < 35.5:
        points += 25
        flags.append('Critical Body Temperature')
    elif temp > 37.5:
        points += 15
        flags.append('Low-grade Fever / Hyperthermia')
    elif temp < 36.2:
        points += 10
        flags.append('Mild Hypothermia')

    # 2. Blood Pressure (mmHg)
    if sys >= 180 or dia >= 120:
        points += 35
        flags.append('Hypertensive Crisis')
    elif sys >= 140 or dia >= 90:
        points += 25
        flags.append('Hypertension Stage 2')
    elif sys >= 130 or dia >= 80:
        points += 15
        flags.append('Hypertension Stage 1')
    elif sys >= 120 and dia < 80:
        points += 8
        flags.append('Elevated Blood Pressure')
    elif sys < 90 or dia < 60:
        points += 15
        flags.append('Hypotension / Low Blood Pressure')

    # 3. Heart Rate (BPM)
    if hr > 115:
        points += 20
        flags.append('Significant Tachycardia')
    elif hr > 100:
        points += 12
        flags.append('Mild Tachycardia')
    elif hr < 50:
        points += 20
        flags.append('Bradycardia')
    elif hr < 60:
        points += 8
        flags.append('Low Heart Rate')

    # 4. SpO2 Oxygen Saturation (%)
    if spo2 <= 90:
        points += 30
        flags.append('Severe Hypoxemia')
    elif spo2 <= 94:
        points += 18
        flags.append('Mild Hypoxemia')

    # 5. Respiratory Rate (breaths/min)
    if rr > 24:
        points += 20
        flags.append('Tachypnea (Rapid Breathing)')
    elif rr > 20:
        points += 10
        flags.append('Slightly High Respiratory Rate')
    elif rr < 10:
        points += 20
        flags.append('Bradypnea (Depressed Breathing)')

    # 6. BMI Risk Factor
    if bmi >= 30.0:
        points += 15
        flags.append('Obesity Risk')
    elif bmi >= 25.0:
        points += 8
        flags.append('Overweight Risk')
    elif bmi < 18.5:
        points += 8
        flags.append('Underweight Risk')

    # Normalize to 0-100%
    risk_score = min(round(points * 0.9, 1), 100.0)

    # Risk level classification
    if risk_score < 25.0:
        risk_level = 'Low Risk'
        rec = "All monitored vital signs and BMI are within standard healthy limits. Keep up your active lifestyle, stay properly hydrated during campus hours, and maintain balanced nutrition."
    elif risk_score < 50.0:
        risk_level = 'Moderate Risk'
        identified = ", ".join(flags) if flags else "Mild vital sign deviation"
        rec = f"Noted health observation: {identified}. Rest for 15-30 minutes and re-screen at the FOVB-AIoT kiosk. Limit high-caffeine energy drinks and consult the RTU Pasig Clinic nurse if readings remain atypical."
    else:
        risk_level = 'High Risk'
        identified = ", ".join(flags) if flags else "Significant vital anomalies detected"
        rec = f"URGENT ATTENTION: {identified}. Your multi-parameter health prediction indicates acute strain. Please report directly to the RTU Pasig Clinic (Ground Floor) or nearest healthcare provider for clinical evaluation."

    return risk_score, risk_level, rec

# Auth Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access your health dashboard.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Context Processor for User Info
@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
    return dict(current_user=user)

# --- Routes ---

@app.route('/')
@app.route('/index.html')
def index():
    conn = get_db()
    total_users = conn.execute('SELECT COUNT(*) as c FROM users').fetchone()['c']
    total_checkups = conn.execute('SELECT COUNT(*) as c FROM checkup_logs').fetchone()['c']
    conn.close()
    return render_template('index.html', total_users=total_users, total_checkups=total_checkups)

@app.route('/about')
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/instructions')
@app.route('/instructions.html')
def instructions():
    return render_template('instructions.html')

@app.route('/contact', methods=['GET', 'POST'])
@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash('Please fill out all required fields.', 'error')
        else:
            conn = get_db()
            conn.execute('''
                INSERT INTO contact_messages (name, email, phone, subject, message)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, phone, subject, message))
            conn.commit()
            conn.close()
            flash('Salamat! Your message has been sent to RTU Pasig Clinic and the FOVB-AIoT team. We will get back to you shortly.', 'success')
            return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        student_id = request.form.get('student_id', '').strip().upper()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        age = request.form.get('age', type=int)
        sex = request.form.get('sex', '')
        department = request.form.get('department', '').strip()
        phone = request.form.get('phone', '').strip()
        rfid_uid = request.form.get('rfid_uid', '').strip().upper()

        # Validation
        if not full_name or not student_id or not email or not password:
            flash('Please fill in all mandatory fields.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match. Please re-enter.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')

        # Auto-generate RFID if user requested
        if not rfid_uid or rfid_uid == 'AUTO':
            hex_parts = [f"{random.randint(0, 255):02X}" for _ in range(4)]
            rfid_uid = " ".join(hex_parts)

        conn = get_db()
        existing_student = conn.execute('SELECT id FROM users WHERE student_id = ?', (student_id,)).fetchone()
        if existing_student:
            conn.close()
            flash(f'Student/Faculty ID {student_id} is already registered. Please log in or contact clinic support.', 'error')
            return render_template('register.html')

        existing_email = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing_email:
            conn.close()
            flash(f'Email address {email} is already in use.', 'error')
            return render_template('register.html')

        existing_rfid = conn.execute('SELECT id FROM users WHERE rfid_uid = ?', (rfid_uid,)).fetchone()
        if existing_rfid:
            conn.close()
            flash(f'RFID UID {rfid_uid} is already associated with another account.', 'error')
            return render_template('register.html')

        pw_hash = generate_password_hash(password)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (student_id, full_name, email, password_hash, age, sex, department, phone, rfid_uid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, full_name, email, pw_hash, age, sex, department, phone, rfid_uid))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Automatically log the user in
        session['user_id'] = user_id
        session['user_name'] = full_name
        flash(f'Mabuhay, {full_name}! Registration successful. Your RFID UID is {rfid_uid}.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')

        if not login_identifier or not password:
            flash('Please enter your Student ID / Email and password.', 'error')
            return render_template('login.html')

        conn = get_db()
        # Search by email, student_id, or RFID UID
        user = conn.execute('''
            SELECT * FROM users 
            WHERE email = ? OR student_id = ? OR rfid_uid = ?
        ''', (login_identifier.lower(), login_identifier.upper(), login_identifier.upper())).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Invalid login credentials or unregistered RFID/ID. Please check and try again.', 'error')

    return render_template('login.html')

@app.route('/demo-login')
def demo_login():
    conn = get_db()
    user = conn.execute('SELECT * FROM users ORDER BY id ASC LIMIT 1').fetchone()
    conn.close()
    if user:
        session['user_id'] = user['id']
        session['user_name'] = user['full_name']
        flash(f'Logged in as Demo Student: {user["full_name"]} (RFID: {user["rfid_uid"]})', 'info')
        return redirect(url_for('dashboard'))
    flash('Demo user not found. Please register a new account.', 'warning')
    return redirect(url_for('register'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been safely logged out. Ingat sa iyong kalusugan!', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    logs = conn.execute('''
        SELECT * FROM checkup_logs 
        WHERE user_id = ? 
        ORDER BY checkup_date DESC
    ''', (user_id,)).fetchall()
    conn.close()

    latest = logs[0] if logs else None
    return render_template('dashboard.html', user=user, logs=logs, latest=latest)

@app.route('/update-rfid', methods=['POST'])
@login_required
def update_rfid():
    user_id = session['user_id']
    new_rfid = request.form.get('rfid_uid', '').strip().upper()

    if not new_rfid:
        flash('RFID UID cannot be empty.', 'error')
        return redirect(url_for('dashboard'))

    conn = get_db()
    existing = conn.execute('SELECT id FROM users WHERE rfid_uid = ? AND id != ?', (new_rfid, user_id)).fetchone()
    if existing:
        conn.close()
        flash('This RFID card UID is already registered to another user.', 'error')
        return redirect(url_for('dashboard'))

    conn.execute('UPDATE users SET rfid_uid = ? WHERE id = ?', (new_rfid, user_id))
    conn.commit()
    conn.close()
    flash(f'RFID card successfully updated to {new_rfid}!', 'success')
    return redirect(url_for('dashboard'))

# --- Interactive Checkup Simulation Route ---
@app.route('/simulate-checkup', methods=['POST'])
@login_required
def simulate_checkup():
    user_id = session['user_id']
    # Generate realistic physiological parameters or take from form
    height = float(request.form.get('height_cm', random.uniform(160.0, 178.0)))
    weight = float(request.form.get('weight_kg', random.uniform(54.0, 75.0)))
    temp = round(float(request.form.get('temperature', random.uniform(36.4, 37.2))), 1)
    hr = int(request.form.get('heart_rate', random.randint(65, 88)))
    rr = int(request.form.get('respiratory_rate', random.randint(14, 18)))
    sys = int(request.form.get('bp_systolic', random.randint(110, 126)))
    dia = int(request.form.get('bp_diastolic', random.randint(70, 84)))
    spo2 = int(request.form.get('spo2', random.randint(97, 99)))

    bmi, bmi_cat = calculate_bmi(height, weight)
    bp_cat = classify_bp(sys, dia)
    risk_score, risk_level, ai_rec = calculate_ai_risk(temp, hr, rr, sys, dia, spo2, bmi)

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db()
    conn.execute('''
        INSERT INTO checkup_logs (
            user_id, checkup_date, height_cm, weight_kg, bmi, bmi_category,
            temperature, heart_rate, respiratory_rate, bp_systolic, bp_diastolic,
            bp_category, spo2, risk_score, risk_level, ai_recommendation, kiosk_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, now_str, height, weight, bmi, bmi_cat,
        temp, hr, rr, sys, dia, bp_cat, spo2, risk_score, risk_level, ai_rec, 'RTU-PASIG-KIOSK-01'
    ))
    conn.commit()
    conn.close()

    flash('Kiosk checkup simulation complete! New vital readings and AI Risk Prediction logged.', 'success')
    return redirect(url_for('dashboard'))

# --- REST APIs for IoT Hardware (Arduino Mega / Nano & Mini PC) ---

@app.route('/api/kiosk/rfid/<path:rfid_uid>', methods=['GET'])
def api_check_rfid(rfid_uid):
    cleaned_rfid = rfid_uid.strip().upper()
    conn = get_db()
    user = conn.execute('SELECT id, student_id, full_name, email, age, sex, department, rfid_uid FROM users WHERE rfid_uid = ?', (cleaned_rfid,)).fetchone()
    conn.close()

    if user:
        return jsonify({
            'status': 'success',
            'found': True,
            'user': {
                'id': user['id'],
                'student_id': user['student_id'],
                'full_name': user['full_name'],
                'email': user['email'],
                'age': user['age'],
                'sex': user['sex'],
                'department': user['department'],
                'rfid_uid': user['rfid_uid']
            }
        }), 200
    else:
        return jsonify({
            'status': 'not_found',
            'found': False,
            'message': f'RFID UID {cleaned_rfid} not registered in FOVB-AIoT system. Please register online.'
        }), 404

@app.route('/api/kiosk/checkup', methods=['POST'])
def api_record_checkup():
    data = request.get_json(silent=True) or request.form
    rfid_uid = data.get('rfid_uid', '').strip().upper()

    conn = get_db()
    user = conn.execute('SELECT id, full_name, student_id FROM users WHERE rfid_uid = ?', (rfid_uid,)).fetchone()
    if not user:
        conn.close()
        return jsonify({
            'status': 'error',
            'message': 'Unregistered RFID card. Please register at the FOVB-AIoT web portal.'
        }), 400

    user_id = user['id']
    try:
        height_cm = float(data.get('height_cm', 170.0))
        weight_kg = float(data.get('weight_kg', 65.0))
        temperature = float(data.get('temperature', 36.6))
        heart_rate = int(data.get('heart_rate', 75))
        respiratory_rate = int(data.get('respiratory_rate', 16))
        bp_systolic = int(data.get('bp_systolic', 120))
        bp_diastolic = int(data.get('bp_diastolic', 80))
        spo2 = int(data.get('spo2', 98))
        kiosk_id = data.get('kiosk_id', 'RTU-PASIG-KIOSK-01')
    except (ValueError, TypeError) as e:
        conn.close()
        return jsonify({'status': 'error', 'message': f'Invalid sensor parameters: {str(e)}'}), 400

    bmi, bmi_cat = calculate_bmi(height_cm, weight_kg)
    bp_cat = classify_bp(bp_systolic, bp_diastolic)
    risk_score, risk_level, ai_rec = calculate_ai_risk(
        temperature, heart_rate, respiratory_rate, bp_systolic, bp_diastolic, spo2, bmi
    )

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO checkup_logs (
            user_id, checkup_date, height_cm, weight_kg, bmi, bmi_category,
            temperature, heart_rate, respiratory_rate, bp_systolic, bp_diastolic,
            bp_category, spo2, risk_score, risk_level, ai_recommendation, kiosk_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, now_str, height_cm, weight_kg, bmi, bmi_cat,
        temperature, heart_rate, respiratory_rate, bp_systolic, bp_diastolic,
        bp_cat, spo2, risk_score, risk_level, ai_rec, kiosk_id
    ))
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Return thermal receipt printable structure
    return jsonify({
        'status': 'success',
        'message': 'Checkup logged successfully',
        'log_id': log_id,
        'user': {
            'student_id': user['student_id'],
            'full_name': user['full_name']
        },
        'results': {
            'timestamp': now_str,
            'height_cm': height_cm,
            'weight_kg': weight_kg,
            'bmi': bmi,
            'bmi_category': bmi_cat,
            'temperature': temperature,
            'heart_rate': heart_rate,
            'respiratory_rate': respiratory_rate,
            'blood_pressure': f"{bp_systolic}/{bp_diastolic} mmHg",
            'bp_category': bp_cat,
            'spo2': f"{spo2}%",
            'risk_score': f"{risk_score}%",
            'risk_level': risk_level,
            'ai_recommendation': ai_rec
        },
        'thermal_receipt_text': (
            f"=== RTU PASIG HEALTH CLINIC ===\n"
            f"FOVB-AIoT Vital Signs Receipt\n"
            f"Date: {now_str}\n"
            f"ID: {user['student_id']} | {user['full_name']}\n"
            f"--------------------------------\n"
            f"Height: {height_cm} cm | Weight: {weight_kg} kg\n"
            f"BMI: {bmi} ({bmi_cat})\n"
            f"Temp: {temperature} C\n"
            f"Blood Pressure: {bp_systolic}/{bp_diastolic} mmHg\n"
            f"Heart Rate: {heart_rate} bpm\n"
            f"Respiratory Rate: {respiratory_rate} br/min\n"
            f"SpO2: {spo2}%\n"
            f"--------------------------------\n"
            f"AI Risk: {risk_level} ({risk_score}%)\n"
            f"{ai_rec[:70]}...\n"
            f"================================\n"
        )
    }), 201

@app.route('/api/stats')
def api_stats():
    conn = get_db()
    total_users = conn.execute('SELECT COUNT(*) as c FROM users').fetchone()['c']
    total_checkups = conn.execute('SELECT COUNT(*) as c FROM checkup_logs').fetchone()['c']
    low_risk = conn.execute("SELECT COUNT(*) as c FROM checkup_logs WHERE risk_level = 'Low Risk'").fetchone()['c']
    mod_risk = conn.execute("SELECT COUNT(*) as c FROM checkup_logs WHERE risk_level = 'Moderate Risk'").fetchone()['c']
    high_risk = conn.execute("SELECT COUNT(*) as c FROM checkup_logs WHERE risk_level = 'High Risk'").fetchone()['c']
    conn.close()

    return jsonify({
        'total_users': total_users,
        'total_checkups': total_checkups,
        'risk_distribution': {
            'low_risk': low_risk,
            'moderate_risk': mod_risk,
            'high_risk': high_risk
        }
    })

# Initialize Database on launch
init_db()

if __name__ == '__main__':
    print("FOVB-AIoT Kiosk & Health Portal running on http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
