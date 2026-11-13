-- ============================================================================
-- InnoSphere: Unified Innovation, Hackathon & Research Management Portal
-- Script: 03_indexes.sql
-- Description: B-Tree Indexes for Query Optimization & High-Throughput Retrieval
-- ============================================================================

USE innosphere_db;

-- Speed up role-based queries and login queries
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_college ON users(college_id);

-- Speed up hackathon filtering (by status, type, and dates)
CREATE INDEX idx_hackathons_status_type ON hackathons(status, hackathon_type);
CREATE INDEX idx_hackathons_dates ON hackathons(start_date, end_date);
CREATE INDEX idx_hackathons_deadline ON hackathons(registration_deadline);

-- Speed up participant lookup by roll number and department
CREATE INDEX idx_profiles_roll ON participant_profiles(roll_number);
CREATE INDEX idx_profiles_dept ON participant_profiles(department_id);

-- Speed up team and project queries per hackathon
CREATE INDEX idx_teams_hackathon ON teams(hackathon_id);
CREATE INDEX idx_teammembers_team ON team_members(team_id);
CREATE INDEX idx_teammembers_user ON team_members(user_id);
CREATE INDEX idx_projects_hackathon ON projects(hackathon_id);

-- Speed up evaluation retrieval and leaderboard calculations
CREATE INDEX idx_eval_project ON evaluations(project_id);
CREATE INDEX idx_eval_judge ON evaluations(judge_user_id);

-- Speed up certificate verification lookup (public verification page)
CREATE INDEX idx_certificates_code ON certificates(certificate_code);

-- Speed up unread notifications fetch
CREATE INDEX idx_notifications_user_read ON notifications(user_id, is_read);
