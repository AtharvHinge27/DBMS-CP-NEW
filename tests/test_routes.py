"""
InnoSphere Frontend Page & Route Tests
Verifies that all 14 pages render properly with correct HTTP status codes.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestInnoSphereRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_01_public_pages(self):
        """Test public pages accessible without login."""
        public_urls = ['/', '/login', '/register', '/hackathons', '/hackathons/1', '/leaderboard', '/verify-certificate']
        for url in public_urls:
            with self.subTest(url=url):
                res = self.client.get(url)
                self.assertEqual(res.status_code, 200, f"Page {url} should return HTTP 200.")

    def test_02_authenticated_participant_pages(self):
        """Test pages accessible by logged-in participant."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 6
            sess['full_name'] = 'Atharv Hinge'
            sess['email'] = 'atharv@pict.edu'
            sess['role'] = 'Participant'
            sess['college_id'] = 1
            sess['college_name'] = 'Pune Institute of Computer Technology'

        participant_urls = ['/dashboard', '/profile', '/teams', '/certificates']
        for url in participant_urls:
            with self.subTest(url=url):
                res = self.client.get(url)
                self.assertEqual(res.status_code, 200, f"Participant page {url} should return HTTP 200.")

    def test_03_authenticated_judge_pages(self):
        """Test pages accessible by logged-in judge."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 4
            sess['full_name'] = 'Dr. Anand Sharma'
            sess['email'] = 'judge.sharma@innosphere.edu'
            sess['role'] = 'Judge'

        res = self.client.get('/evaluations')
        self.assertEqual(res.status_code, 200)

    def test_04_authenticated_admin_pages(self):
        """Test pages accessible by logged-in admin."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['full_name'] = 'System Administrator'
            sess['email'] = 'admin@innosphere.edu'
            sess['role'] = 'Admin'

        admin_urls = ['/admin', '/coordinator']
        for url in admin_urls:
            with self.subTest(url=url):
                res = self.client.get(url)
                self.assertEqual(res.status_code, 200, f"Admin page {url} should return HTTP 200.")

    def test_05_404_handler(self):
        """Test 404 error handler."""
        res = self.client.get('/non_existent_page_url_12345')
        self.assertEqual(res.status_code, 404)

if __name__ == '__main__':
    unittest.main()
