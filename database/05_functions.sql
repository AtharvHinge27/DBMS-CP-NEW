-- ============================================================================
-- InnoSphere: Unified Innovation, Hackathon & Research Management Portal
-- Script: 05_functions.sql
-- Description: Stored Functions for Calculations, Metrics & Data Transformations
-- ============================================================================

USE innosphere_db;

DROP FUNCTION IF EXISTS fn_calculate_profile_completion;
DROP FUNCTION IF EXISTS fn_get_team_member_count;
DROP FUNCTION IF EXISTS fn_get_user_college_name;

DELIMITER $$

-- ----------------------------------------------------------------------------
-- 1. Function: Calculate Profile Completion Percentage dynamically
-- ----------------------------------------------------------------------------
CREATE FUNCTION fn_calculate_profile_completion(p_user_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_score INT DEFAULT 0;
    DECLARE v_roll VARCHAR(30);
    DECLARE v_dept INT;
    DECLARE v_branch VARCHAR(100);
    DECLARE v_year INT;
    DECLARE v_phone VARCHAR(20);
    DECLARE v_skills TEXT;
    DECLARE v_github VARCHAR(255);
    DECLARE v_linkedin VARCHAR(255);
    DECLARE v_bio TEXT;

    SELECT 
        roll_number, department_id, branch, year_of_study, 
        phone_number, technical_skills, github_url, linkedin_url, bio
    INTO 
        v_roll, v_dept, v_branch, v_year, 
        v_phone, v_skills, v_github, v_linkedin, v_bio
    FROM participant_profiles
    WHERE user_id = p_user_id;

    -- Base user registration starts with 15%
    SET v_score = 15;

    IF v_roll IS NOT NULL AND CHAR_LENGTH(TRIM(v_roll)) > 0 THEN
        SET v_score = v_score + 15;
    END IF;

    IF v_dept IS NOT NULL THEN
        SET v_score = v_score + 10;
    END IF;

    IF v_branch IS NOT NULL AND CHAR_LENGTH(TRIM(v_branch)) > 0 THEN
        SET v_score = v_score + 10;
    END IF;

    IF v_year IS NOT NULL AND v_year > 0 THEN
        SET v_score = v_score + 10;
    END IF;

    IF v_phone IS NOT NULL AND CHAR_LENGTH(TRIM(v_phone)) > 0 THEN
        SET v_score = v_score + 10;
    END IF;

    IF v_skills IS NOT NULL AND CHAR_LENGTH(TRIM(v_skills)) > 0 THEN
        SET v_score = v_score + 15;
    END IF;

    IF (v_github IS NOT NULL AND CHAR_LENGTH(TRIM(v_github)) > 0) OR 
       (v_linkedin IS NOT NULL AND CHAR_LENGTH(TRIM(v_linkedin)) > 0) THEN
        SET v_score = v_score + 15;
    END IF;

    IF v_score > 100 THEN
        SET v_score = 100;
    END IF;

    RETURN v_score;
END$$

-- ----------------------------------------------------------------------------
-- 2. Function: Get Team Member Count
-- ----------------------------------------------------------------------------
CREATE FUNCTION fn_get_team_member_count(p_team_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_count INT DEFAULT 0;
    
    SELECT COUNT(*) INTO v_count
    FROM team_members
    WHERE team_id = p_team_id;

    RETURN v_count;
END$$

-- ----------------------------------------------------------------------------
-- 3. Function: Get User College Name
-- ----------------------------------------------------------------------------
CREATE FUNCTION fn_get_user_college_name(p_user_id INT)
RETURNS VARCHAR(150)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_college_name VARCHAR(150);
    
    SELECT c.college_name INTO v_college_name
    FROM users u
    JOIN colleges c ON u.college_id = c.college_id
    WHERE u.user_id = p_user_id;

    RETURN COALESCE(v_college_name, 'Independent / External');
END$$

DELIMITER ;
