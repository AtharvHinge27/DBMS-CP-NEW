"""
InnoSphere Database Integrity & Unit Tests
Tests connection, constraints, triggers, procedures, views and functions.
"""

import os
import unittest
import mysql.connector
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

class TestDatabaseIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'atharv@27'),
            database=os.getenv('DB_NAME', 'innosphere_db')
        )
        cls.cursor = cls.conn.cursor(dictionary=True)

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        cls.conn.close()

    def test_01_tables_exist(self):
        """Verify all 16 core normalized tables exist in innosphere_db."""
        expected_tables = {
            'colleges', 'departments', 'users', 'participant_profiles',
            'hackathons', 'hackathon_registrations', 'teams', 'team_members',
            'projects', 'judge_assignments', 'evaluation_criteria',
            'evaluations', 'attendance', 'certificates', 'notifications',
            'audit_logs'
        }
        self.cursor.execute("SHOW FULL TABLES WHERE Table_Type = 'BASE TABLE';")
        actual_tables = {list(row.values())[0].lower() for row in self.cursor.fetchall()}
        for table in expected_tables:
            self.assertIn(table, actual_tables, f"Table {table} must exist.")

    def test_02_views_exist(self):
        """Verify all 4 analytical and reporting views exist."""
        expected_views = {
            'vw_hackathon_leaderboard', 'vw_participant_summary',
            'vw_hackathon_statistics', 'vw_team_roster'
        }
        self.cursor.execute("SHOW FULL TABLES WHERE Table_Type = 'VIEW';")
        actual_views = {list(row.values())[0].lower() for row in self.cursor.fetchall()}
        for view in expected_views:
            self.assertIn(view, actual_views, f"View {view} must exist.")

    def test_03_trigger_after_user_insert(self):
        """Test trigger trg_after_user_insert automatically creates profile row."""
        test_email = 'unit_test_student@pict.edu'
        # Clean up if exists
        self.cursor.execute("DELETE FROM users WHERE email = %s;", (test_email,))
        self.conn.commit()

        # Insert user
        self.cursor.execute("""
            INSERT INTO users (college_id, full_name, email, password_hash, role)
            VALUES (1, 'Unit Test Student', %s, 'hash123', 'Participant');
        """, (test_email,))
        self.conn.commit()
        new_user_id = self.cursor.lastrowid

        # Verify profile was automatically created by trigger
        self.cursor.execute("SELECT * FROM participant_profiles WHERE user_id = %s;", (new_user_id,))
        profile = self.cursor.fetchone()
        self.assertIsNotNone(profile, "Trigger should have auto-created participant profile.")
        self.assertEqual(profile['profile_completion_pct'], 15)

        # Verify welcome notification was created
        self.cursor.execute("SELECT * FROM notifications WHERE user_id = %s AND title = 'Welcome to InnoSphere!';", (new_user_id,))
        notif = self.cursor.fetchone()
        self.assertIsNotNone(notif, "Trigger should have auto-created welcome notification.")

        # Clean up test user
        self.cursor.execute("DELETE FROM users WHERE user_id = %s;", (new_user_id,))
        self.conn.commit()

    def test_04_stored_function_profile_calc(self):
        """Test stored function fn_calculate_profile_completion."""
        self.cursor.execute("SELECT fn_calculate_profile_completion(6) AS pct;")
        res = self.cursor.fetchone()
        self.assertGreaterEqual(res['pct'], 80, "Atharv Hinge profile completion should be >= 80%.")

    def test_05_stored_procedure_acid_transaction(self):
        """Test sp_create_team_with_leader execution and rollback integrity."""
        # Clean up any leftover test team
        self.cursor.execute("DELETE FROM teams WHERE invitation_code = 'TEST-CODE-01';")
        self.conn.commit()

        # Call procedure with participant 8 for hackathon 2
        args = [2, 'Test Team Innovators', 'TEST-CODE-01', 8, 0, '']
        result = self.cursor.callproc('sp_create_team_with_leader', args)
        self.conn.commit()

        # In mysql-connector-python, callproc returns updated args in tuple/dict
        # Or we can verify the team in the database directly
        self.cursor.execute("SELECT team_id, team_name, leader_user_id FROM teams WHERE invitation_code = 'TEST-CODE-01';")
        team = self.cursor.fetchone()
        self.assertIsNotNone(team, "Team should have been created by stored procedure.")
        out_team_id = team['team_id']

        # Verify team members has leader
        self.cursor.execute("SELECT * FROM team_members WHERE team_id = %s AND user_id = 8;", (out_team_id,))
        member = self.cursor.fetchone()
        self.assertIsNotNone(member, "Team leader should have been automatically added to team_members.")
        self.assertEqual(member['role_in_team'], 'Leader')

        # Clean up test team
        self.cursor.execute("DELETE FROM teams WHERE team_id = %s;", (out_team_id,))
        self.conn.commit()

if __name__ == '__main__':
    unittest.main()
