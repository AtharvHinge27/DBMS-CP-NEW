-- ============================================================================
-- InnoSphere: Unified Innovation, Hackathon & Research Management Portal
-- Script: 07_triggers.sql
-- Description: Triggers for Automated Integrity, Default Initialization & Audit
-- ============================================================================

USE innosphere_db;

DROP TRIGGER IF EXISTS trg_after_user_insert;
DROP TRIGGER IF EXISTS trg_before_evaluation_insert;
DROP TRIGGER IF EXISTS trg_before_evaluation_update;
DROP TRIGGER IF EXISTS trg_after_project_insert;

DELIMITER $$

-- ----------------------------------------------------------------------------
-- 1. Trigger: Automatically initialize participant profile upon user registration
-- Ensures 1:1 entity constraint and sets base completion percentage to 15%
-- ----------------------------------------------------------------------------
CREATE TRIGGER trg_after_user_insert
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    IF NEW.role = 'Participant' THEN
        INSERT INTO participant_profiles (user_id, profile_completion_pct)
        VALUES (NEW.user_id, 15);

        INSERT INTO notifications (user_id, title, message, link)
        VALUES (
            NEW.user_id,
            'Welcome to InnoSphere!',
            'Complete your academic and technical profile to unlock full team participation and hackathon registrations.',
            '/profile'
        );
    END IF;
END$$

-- ----------------------------------------------------------------------------
-- 2. Trigger: Automatically compute and enforce total_score before evaluation insert
-- ----------------------------------------------------------------------------
CREATE TRIGGER trg_before_evaluation_insert
BEFORE INSERT ON evaluations
FOR EACH ROW
BEGIN
    -- Automatically compute total_score from the 4 sub-criteria
    SET NEW.total_score = NEW.innovation_score + NEW.feasibility_score + NEW.technical_score + NEW.presentation_score;

    IF NEW.total_score > 100.00 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Validation Error: Total evaluation score cannot exceed 100.00';
    END IF;
END$$

-- ----------------------------------------------------------------------------
-- 3. Trigger: Automatically compute and enforce total_score before evaluation update
-- ----------------------------------------------------------------------------
CREATE TRIGGER trg_before_evaluation_update
BEFORE UPDATE ON evaluations
FOR EACH ROW
BEGIN
    SET NEW.total_score = NEW.innovation_score + NEW.feasibility_score + NEW.technical_score + NEW.presentation_score;

    IF NEW.total_score > 100.00 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Validation Error: Total evaluation score cannot exceed 100.00';
    END IF;
END$$

-- ----------------------------------------------------------------------------
-- 4. Trigger: Notify Team Members when a Project is Submitted
-- ----------------------------------------------------------------------------
CREATE TRIGGER trg_after_project_insert
AFTER INSERT ON projects
FOR EACH ROW
BEGIN
    -- Insert notification for the team leader
    INSERT INTO notifications (user_id, title, message, link)
    SELECT 
        tm.user_id,
        'Project Submitted Successfully',
        CONCAT('Project "', NEW.title, '" has been officially submitted for evaluation.'),
        '/teams'
    FROM team_members tm
    WHERE tm.team_id = NEW.team_id;

    -- Audit trail
    INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
    VALUES (
        NULL,
        'PROJECT_SUBMITTED',
        'projects',
        NEW.project_id,
        CONCAT('Project "', NEW.title, '" was submitted for hackathon ID ', NEW.hackathon_id)
    );
END$$

DELIMITER ;
