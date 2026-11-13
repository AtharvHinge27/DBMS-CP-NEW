-- ============================================================================
-- InnoSphere: Unified Innovation, Hackathon & Research Management Portal
-- Script: 06_stored_procedures.sql
-- Description: Stored Procedures with ACID Transactions, Error Handlers & Audit
-- ============================================================================

USE innosphere_db;

DROP PROCEDURE IF EXISTS sp_create_team_with_leader;
DROP PROCEDURE IF EXISTS sp_join_team_by_code;
DROP PROCEDURE IF EXISTS sp_record_evaluation;
DROP PROCEDURE IF EXISTS sp_issue_certificate;

DELIMITER $$

-- ----------------------------------------------------------------------------
-- 1. Procedure: Create Team with Leader (Demonstrates ACID Properties)
-- Atomicity: Team and Leader insertion must both succeed or both fail.
-- Consistency: Checked via constraints and business logic validations.
-- Isolation: Managed by InnoDB transaction isolation.
-- Durability: Committed changes survive crashes.
-- ----------------------------------------------------------------------------
CREATE PROCEDURE sp_create_team_with_leader(
    IN p_hackathon_id INT,
    IN p_team_name VARCHAR(120),
    IN p_invitation_code VARCHAR(12),
    IN p_leader_user_id INT,
    OUT p_out_team_id INT,
    OUT p_status_message VARCHAR(255)
)
proc_label: BEGIN
    DECLARE v_reg_count INT DEFAULT 0;
    DECLARE v_existing_team INT DEFAULT 0;
    DECLARE v_new_team_id INT;

    -- Error handler: Rollback on any SQL exception
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_out_team_id = NULL;
        SET p_status_message = 'ERROR: Database transaction failed during team creation. Changes rolled back.';
    END;

    -- Step 1: Check if user is registered for this hackathon
    SELECT COUNT(*) INTO v_reg_count
    FROM hackathon_registrations
    WHERE hackathon_id = p_hackathon_id AND user_id = p_leader_user_id;

    IF v_reg_count = 0 THEN
        -- Auto-register user for the hackathon
        INSERT INTO hackathon_registrations (hackathon_id, user_id, status)
        VALUES (p_hackathon_id, p_leader_user_id, 'Approved');
    END IF;

    -- Step 2: Check if user is already in a team for this hackathon
    SELECT COUNT(*) INTO v_existing_team
    FROM team_members tm
    JOIN teams t ON tm.team_id = t.team_id
    WHERE t.hackathon_id = p_hackathon_id AND tm.user_id = p_leader_user_id;

    IF v_existing_team > 0 THEN
        SET p_out_team_id = NULL;
        SET p_status_message = 'ERROR: You are already a member of a team in this hackathon.';
        LEAVE proc_label;
    END IF;

    -- Step 3: Transactional Execution (ACID)
    START TRANSACTION;

    -- Insert team record
    INSERT INTO teams (hackathon_id, team_name, invitation_code, leader_user_id)
    VALUES (p_hackathon_id, p_team_name, p_invitation_code, p_leader_user_id);

    SET v_new_team_id = LAST_INSERT_ID();

    -- Insert leader as first team member
    INSERT INTO team_members (team_id, user_id, role_in_team)
    VALUES (v_new_team_id, p_leader_user_id, 'Leader');

    -- Insert notification for the leader
    INSERT INTO notifications (user_id, title, message, link)
    VALUES (
        p_leader_user_id,
        'Team Created Successfully',
        CONCAT('Your team "', p_team_name, '" has been created. Share invitation code: ', p_invitation_code),
        CONCAT('/teams')
    );

    -- Log transaction in audit trail
    INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
    VALUES (
        p_leader_user_id,
        'CREATE_TEAM',
        'teams',
        v_new_team_id,
        CONCAT('Created team "', p_team_name, '" with code ', p_invitation_code)
    );

    COMMIT;

    SET p_out_team_id = v_new_team_id;
    SET p_status_message = 'SUCCESS: Team created and leader assigned.';
END$$


-- ----------------------------------------------------------------------------
-- 2. Procedure: Join Team by Invitation Code
-- ----------------------------------------------------------------------------
CREATE PROCEDURE sp_join_team_by_code(
    IN p_invitation_code VARCHAR(12),
    IN p_user_id INT,
    IN p_role_in_team VARCHAR(50),
    OUT p_out_team_id INT,
    OUT p_status_message VARCHAR(255)
)
proc_label: BEGIN
    DECLARE v_team_id INT;
    DECLARE v_hackathon_id INT;
    DECLARE v_max_size INT;
    DECLARE v_current_size INT;
    DECLARE v_is_already_member INT;
    DECLARE v_leader_id INT;
    DECLARE v_team_name VARCHAR(120);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_out_team_id = NULL;
        SET p_status_message = 'ERROR: Database transaction failed during team join. Changes rolled back.';
    END;

    -- Find team by code
    SELECT t.team_id, t.hackathon_id, t.leader_user_id, t.team_name, h.max_team_size
    INTO v_team_id, v_hackathon_id, v_leader_id, v_team_name, v_max_size
    FROM teams t
    JOIN hackathons h ON t.hackathon_id = h.hackathon_id
    WHERE t.invitation_code = p_invitation_code;

    IF v_team_id IS NULL THEN
        SET p_out_team_id = NULL;
        SET p_status_message = 'ERROR: Invalid invitation code. No matching team found.';
        LEAVE proc_label;
    END IF;

    -- Check if user is already in a team for this hackathon
    SELECT COUNT(*) INTO v_is_already_member
    FROM team_members tm
    JOIN teams t ON tm.team_id = t.team_id
    WHERE t.hackathon_id = v_hackathon_id AND tm.user_id = p_user_id;

    IF v_is_already_member > 0 THEN
        SET p_out_team_id = NULL;
        SET p_status_message = 'ERROR: You are already registered in a team for this hackathon.';
        LEAVE proc_label;
    END IF;

    -- Check current team size
    SELECT COUNT(*) INTO v_current_size
    FROM team_members
    WHERE team_id = v_team_id;

    IF v_current_size >= v_max_size THEN
        SET p_out_team_id = NULL;
        SET p_status_message = CONCAT('ERROR: Team is already full (Maximum capacity: ', v_max_size, ').');
        LEAVE proc_label;
    END IF;

    -- Transactional Join
    START TRANSACTION;

    -- Auto-register user for hackathon if not already registered
    INSERT IGNORE INTO hackathon_registrations (hackathon_id, user_id, status)
    VALUES (v_hackathon_id, p_user_id, 'Approved');

    -- Insert into team members
    INSERT INTO team_members (team_id, user_id, role_in_team)
    VALUES (v_team_id, p_user_id, COALESCE(p_role_in_team, 'Member'));

    -- Notify Team Leader
    INSERT INTO notifications (user_id, title, message, link)
    VALUES (
        v_leader_id,
        'New Member Joined Your Team',
        CONCAT('A new member has joined your team "', v_team_name, '".'),
        '/teams'
    );

    -- Notify Joining Member
    INSERT INTO notifications (user_id, title, message, link)
    VALUES (
        p_user_id,
        'Joined Team Successfully',
        CONCAT('You have successfully joined team "', v_team_name, '".'),
        '/teams'
    );

    -- Log transaction
    INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
    VALUES (
        p_user_id,
        'JOIN_TEAM',
        'teams',
        v_team_id,
        CONCAT('Joined team id ', v_team_id, ' using code ', p_invitation_code)
    );

    COMMIT;

    SET p_out_team_id = v_team_id;
    SET p_status_message = 'SUCCESS: You have successfully joined the team.';
END$$


-- ----------------------------------------------------------------------------
-- 3. Procedure: Record Evaluation with Multi-Criteria Scoring
-- ----------------------------------------------------------------------------
CREATE PROCEDURE sp_record_evaluation(
    IN p_project_id INT,
    IN p_judge_user_id INT,
    IN p_innovation DECIMAL(5,2),
    IN p_feasibility DECIMAL(5,2),
    IN p_technical DECIMAL(5,2),
    IN p_presentation DECIMAL(5,2),
    IN p_feedback TEXT,
    OUT p_out_total DECIMAL(5,2),
    OUT p_status_message VARCHAR(255)
)
BEGIN
    DECLARE v_calc_total DECIMAL(5,2);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_out_total = 0.00;
        SET p_status_message = 'ERROR: Database transaction failed during evaluation recording.';
    END;

    -- Calculate total score
    SET v_calc_total = p_innovation + p_feasibility + p_technical + p_presentation;

    START TRANSACTION;

    -- Upsert evaluation score
    INSERT INTO evaluations (
        project_id, judge_user_id, 
        innovation_score, feasibility_score, 
        technical_score, presentation_score, 
        total_score, feedback, evaluated_at
    )
    VALUES (
        p_project_id, p_judge_user_id,
        p_innovation, p_feasibility,
        p_technical, p_presentation,
        v_calc_total, p_feedback, NOW()
    )
    ON DUPLICATE KEY UPDATE
        innovation_score = VALUES(innovation_score),
        feasibility_score = VALUES(feasibility_score),
        technical_score = VALUES(technical_score),
        presentation_score = VALUES(presentation_score),
        total_score = VALUES(total_score),
        feedback = VALUES(feedback),
        evaluated_at = NOW();

    -- Update project status to 'Evaluated'
    UPDATE projects
    SET submission_status = 'Evaluated'
    WHERE project_id = p_project_id;

    -- Audit log
    INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details)
    VALUES (
        p_judge_user_id,
        'SUBMIT_EVALUATION',
        'projects',
        p_project_id,
        CONCAT('Evaluated project ID ', p_project_id, ' with total score: ', v_calc_total)
    );

    COMMIT;

    SET p_out_total = v_calc_total;
    SET p_status_message = 'SUCCESS: Evaluation recorded successfully.';
END$$


-- ----------------------------------------------------------------------------
-- 4. Procedure: Issue Certificate with Unique Verification Hash
-- ----------------------------------------------------------------------------
CREATE PROCEDURE sp_issue_certificate(
    IN p_user_id INT,
    IN p_hackathon_id INT,
    IN p_team_id INT,
    IN p_certificate_type VARCHAR(50),
    OUT p_out_code VARCHAR(36),
    OUT p_status_message VARCHAR(255)
)
proc_label: BEGIN
    DECLARE v_existing_code VARCHAR(36);
    DECLARE v_generated_code VARCHAR(36);
    DECLARE v_hackathon_title VARCHAR(180);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_out_code = NULL;
        SET p_status_message = 'ERROR: Transaction failed while generating certificate.';
    END;

    -- Check if certificate already exists
    SELECT certificate_code INTO v_existing_code
    FROM certificates
    WHERE user_id = p_user_id 
      AND hackathon_id = p_hackathon_id 
      AND certificate_type = p_certificate_type;

    IF v_existing_code IS NOT NULL THEN
        SET p_out_code = v_existing_code;
        SET p_status_message = 'NOTICE: Certificate already exists for this participant.';
        LEAVE proc_label;
    END IF;

    -- Generate Unique Certificate Code: INNO-{YEAR}-{RANDOM_HEX}
    SET v_generated_code = CONCAT('INNO-', YEAR(CURDATE()), '-', UPPER(SUBSTRING(MD5(CONCAT(p_user_id, p_hackathon_id, NOW(), RAND())), 1, 8)));

    START TRANSACTION;

    INSERT INTO certificates (
        certificate_code, user_id, hackathon_id, 
        team_id, certificate_type, issue_date
    )
    VALUES (
        v_generated_code, p_user_id, p_hackathon_id, 
        p_team_id, p_certificate_type, CURDATE()
    );

    SELECT title INTO v_hackathon_title
    FROM hackathons
    WHERE hackathon_id = p_hackathon_id;

    -- Send notification
    INSERT INTO notifications (user_id, title, message, link)
    VALUES (
        p_user_id,
        'Certificate Issued!',
        CONCAT('Your ', p_certificate_type, ' certificate for "', v_hackathon_title, '" has been generated. Code: ', v_generated_code),
        '/certificates'
    );

    COMMIT;

    SET p_out_code = v_generated_code;
    SET p_status_message = 'SUCCESS: Certificate issued successfully.';
END$$

DELIMITER ;
