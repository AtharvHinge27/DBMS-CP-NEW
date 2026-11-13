-- ============================================================================
-- InnoSphere: Unified Innovation, Hackathon & Research Management Portal
-- Script: 09_advanced_queries.sql
-- Description: Comprehensive DBMS Concept Demonstrations (Viva & Lab Reference)
-- ============================================================================

USE innosphere_db;

-- ============================================================================
-- 1. INNER JOIN DEMONSTRATION
-- Purpose: Retrieve projects along with their team name, leader name, and college
-- Concept: Matches rows present in both tables based on foreign key relationship
-- ============================================================================
SELECT 
    p.project_id,
    p.title AS project_title,
    t.team_name,
    u.full_name AS team_leader,
    c.college_name
FROM projects p
INNER JOIN teams t ON p.team_id = t.team_id
INNER JOIN users u ON t.leader_user_id = u.user_id
INNER JOIN colleges c ON u.college_id = c.college_id;


-- ============================================================================
-- 2. LEFT JOIN DEMONSTRATION
-- Purpose: List all registered hackathons, including those without any project submissions
-- Concept: Retains all rows from the left table (hackathons) even if right table (projects) is NULL
-- ============================================================================
SELECT 
    h.hackathon_id,
    h.title AS hackathon_title,
    h.hackathon_type,
    p.project_id,
    COALESCE(p.title, 'No Projects Submitted Yet') AS submission_status
FROM hackathons h
LEFT JOIN projects p ON h.hackathon_id = p.hackathon_id;


-- ============================================================================
-- 3. AGGREGATE FUNCTIONS, GROUP BY AND HAVING CLAUSE
-- Purpose: Find colleges having more than 2 participating students registered
-- Concept: GROUP BY groups records by college; HAVING filters aggregated groups (unlike WHERE)
-- ============================================================================
SELECT 
    c.college_id,
    c.college_name,
    COUNT(u.user_id) AS total_students
FROM colleges c
INNER JOIN users u ON c.college_id = u.college_id
WHERE u.role = 'Participant'
GROUP BY c.college_id, c.college_name
HAVING COUNT(u.user_id) >= 2
ORDER BY total_students DESC;


-- ============================================================================
-- 4. NESTED SUBQUERIES (SCALAR AND IN / NOT IN)
-- Purpose: Find all participants who have registered for hackathons but not yet joined any team
-- Concept: Subquery inside NOT IN clause isolates orphaned registrations
-- ============================================================================
SELECT 
    u.user_id,
    u.full_name,
    u.email
FROM users u
WHERE u.role = 'Participant'
  AND u.user_id IN (SELECT DISTINCT user_id FROM hackathon_registrations)
  AND u.user_id NOT IN (SELECT DISTINCT user_id FROM team_members);


-- ============================================================================
-- 5. CORRELATED SUBQUERY
-- Purpose: Find projects that scored strictly above the average score of all evaluated projects
-- Concept: Inner subquery computes the overall mean score dynamically
-- ============================================================================
SELECT 
    p.project_id,
    p.title,
    (SELECT AVG(e.total_score) FROM evaluations e WHERE e.project_id = p.project_id) AS avg_score
FROM projects p
WHERE (SELECT AVG(e.total_score) FROM evaluations e WHERE e.project_id = p.project_id) > (
    SELECT AVG(total_score) FROM evaluations
);


-- ============================================================================
-- 6. DCL (DATA CONTROL LANGUAGE) DEMONSTRATION
-- Concept: GRANT and REVOKE permissions to control user access privileges
-- ============================================================================
-- Create dedicated database users for application roles
-- CREATE USER IF NOT EXISTS 'innosphere_web'@'localhost' IDENTIFIED BY 'InnoWebPass@2026';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON innosphere_db.* TO 'innosphere_web'@'localhost';
-- CREATE USER IF NOT EXISTS 'innosphere_evaluator'@'localhost' IDENTIFIED BY 'EvalPass@2026';
-- GRANT SELECT ON innosphere_db.vw_hackathon_leaderboard TO 'innosphere_evaluator'@'localhost';
-- GRANT INSERT, UPDATE ON innosphere_db.evaluations TO 'innosphere_evaluator'@'localhost';
-- FLUSH PRIVILEGES;


-- ============================================================================
-- 7. TCL (TRANSACTION CONTROL LANGUAGE) DEMONSTRATION
-- Concept: Demonstrating COMMIT, ROLLBACK and SAVEPOINT
-- ============================================================================
/*
START TRANSACTION;

INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
VALUES (1, 'MANUAL_TEST', 'test', 999, 'Testing transaction rollback');

SAVEPOINT test_savepoint;

-- Let's say something goes wrong:
ROLLBACK TO test_savepoint;

-- Or commit if all operations succeed:
COMMIT;
*/
