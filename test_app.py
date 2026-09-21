import unittest
from app import app, get_db

class TestFovbAiot(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FOVB-AIoT', response.data)
        self.assertIn(b'RTU Pasig Clinic', response.data)
        self.assertIn(b'MLX90614', response.data)
        self.assertIn(b'MAX30102', response.data)
        print("[PASS] Homepage test passed")

    def test_about_page(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Khin Andrei R. Gamboa', response.data)
        self.assertIn(b'Arduino Mega 2560', response.data)
        self.assertIn(b'YOLO', response.data)
        print("[PASS] About page test passed")

    def test_instructions_page(self):
        response = self.client.get('/instructions')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'How to Use the FOVB-AIoT Kiosk', response.data)
        print("[PASS] Instructions page test passed")

    def test_contact_page(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'RTU Pasig Health Clinic', response.data)
        print("[PASS] Contact page test passed")

    def test_demo_login_and_dashboard(self):
        response = self.client.get('/demo-login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Demo Student', response.data)
        self.assertIn(b'AI Health Risk Prediction', response.data)
        self.assertIn(b'E2 80 68 31', response.data)
        print("[PASS] Demo login & Dashboard test passed")

    def test_kiosk_api_rfid_lookup(self):
        response = self.client.get('/api/kiosk/rfid/E2 80 68 31')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['found'])
        self.assertEqual(data['user']['student_id'], 'DEMO-2026-01')
        print("[PASS] Kiosk RFID lookup API passed")

    def test_kiosk_api_checkup_submission(self):
        payload = {
            'rfid_uid': 'E2 80 68 31',
            'height_cm': 172.5,
            'weight_kg': 66.0,
            'temperature': 36.7,
            'heart_rate': 72,
            'respiratory_rate': 16,
            'bp_systolic': 118,
            'bp_diastolic': 78,
            'spo2': 98
        }
        response = self.client.post('/api/kiosk/checkup', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('thermal_receipt_text', data)
        print("[PASS] Kiosk telemetry ingestion & thermal receipt API passed")

    def test_api_stats(self):
        response = self.client.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(data['total_users'], 1)
        self.assertGreaterEqual(data['total_checkups'], 1)
        print("[PASS] Public stats API passed")

if __name__ == '__main__':
    unittest.main()
