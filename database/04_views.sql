-- ============================================================================
-- InnoSphere: Unified Innovation, Hackathon & Research Management Portal
-- Script: 04_views.sql
-- Description: Database Views for Complex Aggregations, Leaderboards & Analytics
-- ============================================================================

USE innosphere_db;

-- ----------------------------------------------------------------------------
-- 1. Leaderboard View: Ranked projects per hackathon by average judge score
-- Uses: INNER JOIN, LEFT JOIN, Aggregate AVG(), GROUP BY, Window Function DENSE_RANK()
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_hackathon_leaderboard AS
SELECT 
    h.hackathon_id,
    h.title AS hackathon_title,
    p.project_id,
    p.title AS project_title,
    p.submission_status,
    t.team_id,
    t.team_name,
    u.full_name AS leader_name,
    u.email AS leader_email,
    c.college_name,
    COUNT(e.evaluation_id) AS total_evaluations,
    ROUND(COALESCE(AVG(e.total_score), 0.00), 2) AS average_score,
    ROUND(COALESCE(AVG(e.innovation_score), 0.00), 2) AS avg_innovation,
    ROUND(COALESCE(AVG(e.feasibility_score), 0.00), 2) AS avg_feasibility,
    ROUND(COALESCE(AVG(e.technical_score), 0.00), 2) AS avg_technical,
    ROUND(COALESCE(AVG(e.presentation_score), 0.00), 2) AS avg_presentation,
    DENSE_RANK() OVER (
        PARTITION BY h.hackathon_id 
        ORDER BY COALESCE(AVG(e.total_score), 0.00) DESC
    ) AS leaderboard_rank
FROM projects p
JOIN teams t ON p.team_id = t.team_id
JOIN hackathons h ON p.hackathon_id = h.hackathon_id
JOIN users u ON t.leader_user_id = u.user_id
LEFT JOIN colleges c ON u.college_id = c.college_id
LEFT JOIN evaluations e ON p.project_id = e.project_id
GROUP BY 
    h.hackathon_id, h.title, p.project_id, p.title, 
    p.submission_status, t.team_id, t.team_name, 
    u.full_name, u.email, c.college_name;

-- ----------------------------------------------------------------------------
-- 2. Participant Summary View: Consolidated student 360-degree profile
-- Uses: LEFT JOIN across 5 tables, aggregate counts, subqueries
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_participant_summary AS
SELECT 
    u.user_id,
    u.full_name,
    u.email,
    u.role,
    u.is_active,
    c.college_name,
    c.college_code,
    d.department_name,
    d.department_code,
    pp.roll_number,
    pp.branch,
    pp.year_of_study,
    pp.semester,
    pp.phone_number,
    pp.technical_skills,
    pp.interests,
    pp.github_url,
    pp.linkedin_url,
    pp.profile_completion_pct,
    (SELECT COUNT(*) FROM hackathon_registrations hr WHERE hr.user_id = u.user_id) AS total_hackathons_registered,
    (SELECT COUNT(*) FROM team_members tm WHERE tm.user_id = u.user_id) AS total_teams_joined,
    (SELECT COUNT(*) FROM certificates cert WHERE cert.user_id = u.user_id) AS total_certificates_earned
FROM users u
LEFT JOIN colleges c ON u.college_id = c.college_id
LEFT JOIN participant_profiles pp ON u.user_id = pp.user_id
LEFT JOIN departments d ON pp.department_id = d.department_id
WHERE u.role = 'Participant';

-- ----------------------------------------------------------------------------
-- 3. Hackathon Comprehensive Statistics View
-- Uses: Aggregates, Subqueries, GROUP BY, CASE statements
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_hackathon_statistics AS
SELECT 
    h.hackathon_id,
    h.title,
    h.theme,
    h.hackathon_type,
    h.mode,
    h.status,
    h.start_date,
    h.end_date,
    h.registration_deadline,
    COALESCE(c.college_name, 'External / National Platform') AS host_institution,
    (SELECT COUNT(*) FROM hackathon_registrations hr WHERE hr.hackathon_id = h.hackathon_id) AS total_registrations,
    (SELECT COUNT(*) FROM teams t WHERE t.hackathon_id = h.hackathon_id) AS total_teams,
    (SELECT COUNT(*) FROM projects p WHERE p.hackathon_id = h.hackathon_id) AS total_projects_submitted,
    (SELECT COUNT(*) FROM judge_assignments ja WHERE ja.hackathon_id = h.hackathon_id) AS total_judges_assigned,
    (SELECT COUNT(*) FROM certificates cert WHERE cert.hackathon_id = h.hackathon_id) AS total_certificates_issued
FROM hackathons h
LEFT JOIN colleges c ON h.college_id = c.college_id;

-- ----------------------------------------------------------------------------
-- 4. Team Roster View: Detailed team structure with leader and member count
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_team_roster AS
SELECT 
    t.team_id,
    t.team_name,
    t.invitation_code,
    t.hackathon_id,
    h.title AS hackathon_title,
    h.max_team_size,
    u.user_id AS leader_id,
    u.full_name AS leader_name,
    u.email AS leader_email,
    COUNT(tm.team_member_id) AS current_member_count,
    CASE 
        WHEN COUNT(tm.team_member_id) >= h.max_team_size THEN 'Full'
        ELSE 'Recruiting'
    END AS team_status,
    p.project_id,
    p.title AS project_title,
    p.submission_status,
    t.created_at
FROM teams t
JOIN hackathons h ON t.hackathon_id = h.hackathon_id
JOIN users u ON t.leader_user_id = u.user_id
LEFT JOIN team_members tm ON t.team_id = tm.team_id
LEFT JOIN projects p ON t.team_id = p.team_id
GROUP BY 
    t.team_id, t.team_name, t.invitation_code, t.hackathon_id, 
    h.title, h.max_team_size, u.user_id, u.full_name, u.email, 
    p.project_id, p.title, p.submission_status, t.created_at;
