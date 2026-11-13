"""
InnoSphere API Integration & Functional Tests
Tests all Flask REST endpoints across Auth, Hackathons, Teams, Evaluations, and Certificates.
"""

import os
import sys
import unittest
import json

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from modules.db import execute_dml

class TestInnoSphereAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_01_login_success(self):
        """Test successful login with admin credentials."""
        response = self.client.post('/api/auth/login', json={
            'email': 'admin@innosphere.edu',
            'password': 'admin123'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['role'], 'Admin')

    def test_02_login_invalid_password(self):
        """Test failed login with incorrect password."""
        response = self.client.post('/api/auth/login', json={
            'email': 'admin@innosphere.edu',
            'password': 'wrongpassword'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_03_list_hackathons(self):
        """Test listing hackathons with filters."""
        # All hackathons
        response = self.client.get('/api/hackathons')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['hackathons']), 3)

        # Filter by internal
        res_internal = self.client.get('/api/hackathons?type=Internal')
        data_int = json.loads(res_internal.data)
        self.assertTrue(all(h['hackathon_type'] == 'Internal' for h in data_int['hackathons']))

    def test_04_leaderboard_endpoint(self):
        """Test real-time leaderboard endpoint."""
        response = self.client.get('/api/evaluations/leaderboard?hackathon_id=1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['leaderboard']), 1)
        # Check first rank has highest score
        self.assertEqual(data['leaderboard'][0]['leaderboard_rank'], 1)

    def test_05_certificate_verification(self):
        """Test public certificate verification endpoint."""
        # Existing seed certificate code: INNO-2026-WIN001
        response = self.client.get('/api/certificates/verify/INNO-2026-WIN001')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['verified'])
        self.assertEqual(data['certificate']['recipient_name'], 'Atharv Hinge')
        self.assertEqual(data['certificate']['certificate_type'], 'Winner')

    def test_06_certificate_verification_invalid(self):
        """Test public certificate verification with non-existent code."""
        response = self.client.get('/api/certificates/verify/INNO-INVALID-999')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['verified'])

if __name__ == '__main__':
    unittest.main()
