-- ============================================================================
-- InnoSphere: Unified Innovation, Hackathon & Research Management Portal
-- Script: 02_create_tables.sql
-- Description: Fully Normalized (3NF) relational tables with strict constraints
-- Engine: InnoDB | MySQL 8.0+
-- ============================================================================

USE innosphere_db;

-- ----------------------------------------------------------------------------
-- 1. Colleges Table (Multi-Institution SaaS Tenant Support)
-- ----------------------------------------------------------------------------
CREATE TABLE colleges (
    college_id INT AUTO_INCREMENT PRIMARY KEY,
    college_code VARCHAR(20) NOT NULL UNIQUE,
    college_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    website VARCHAR(255),
    is_approved BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 2. Departments Table
-- ----------------------------------------------------------------------------
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    college_id INT NOT NULL,
    department_code VARCHAR(20) NOT NULL,
    department_name VARCHAR(120) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_departments_college
        FOREIGN KEY (college_id) REFERENCES colleges(college_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_dept_per_college
        UNIQUE (college_id, department_code)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 3. Users Table (Core Authentication and Role-Based Access)
-- ----------------------------------------------------------------------------
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    college_id INT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'College Coordinator', 'Participant', 'Mentor', 'Judge') NOT NULL DEFAULT 'Participant',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_users_college
        FOREIGN KEY (college_id) REFERENCES colleges(college_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 4. Participant Profiles Table (1:1 Relationship with Users)
-- ----------------------------------------------------------------------------
CREATE TABLE participant_profiles (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    roll_number VARCHAR(30),
    department_id INT NULL,
    branch VARCHAR(100),
    year_of_study INT NULL,
    semester INT NULL,
    phone_number VARCHAR(20),
    technical_skills TEXT,
    interests TEXT,
    github_url VARCHAR(255),
    linkedin_url VARCHAR(255),
    portfolio_url VARCHAR(255),
    bio TEXT,
    profile_completion_pct INT DEFAULT 0,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_profiles_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_profiles_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT chk_year_of_study
        CHECK (year_of_study IS NULL OR (year_of_study >= 1 AND year_of_study <= 5)),
    CONSTRAINT chk_semester
        CHECK (semester IS NULL OR (semester >= 1 AND semester <= 10)),
    CONSTRAINT chk_profile_completion
        CHECK (profile_completion_pct >= 0 AND profile_completion_pct <= 100)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 5. Hackathons Table (Internal & External Opportunity Management)
-- ----------------------------------------------------------------------------
CREATE TABLE hackathons (
    hackathon_id INT AUTO_INCREMENT PRIMARY KEY,
    college_id INT NULL,
    title VARCHAR(180) NOT NULL,
    theme VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    hackathon_type ENUM('Internal', 'External') NOT NULL DEFAULT 'Internal',
    mode ENUM('Online', 'Offline', 'Hybrid') NOT NULL DEFAULT 'Online',
    venue VARCHAR(200) DEFAULT 'Main Campus Auditorium / Virtual',
    organizer_name VARCHAR(150) NOT NULL,
    eligibility TEXT,
    external_url VARCHAR(300) NULL,
    registration_deadline DATE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    min_team_size INT NOT NULL DEFAULT 1,
    max_team_size INT NOT NULL DEFAULT 4,
    prize_pool VARCHAR(100) DEFAULT 'Certificates & Trophies',
    status ENUM('Draft', 'Open', 'In Progress', 'Evaluation', 'Completed') NOT NULL DEFAULT 'Open',
    banner_url VARCHAR(255) NULL,
    created_by INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_hackathons_college
        FOREIGN KEY (college_id) REFERENCES colleges(college_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_hackathons_creator
        FOREIGN KEY (created_by) REFERENCES users(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT chk_hackathon_dates
        CHECK (end_date >= start_date),
    CONSTRAINT chk_reg_deadline
        CHECK (start_date >= registration_deadline),
    CONSTRAINT chk_team_sizes
        CHECK (max_team_size >= min_team_size AND min_team_size >= 1)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 6. Hackathon Registrations Table (Individual Applications & Approvals)
-- ----------------------------------------------------------------------------
CREATE TABLE hackathon_registrations (
    registration_id INT AUTO_INCREMENT PRIMARY KEY,
    hackathon_id INT NOT NULL,
    user_id INT NOT NULL,
    status ENUM('Applied', 'Approved', 'Waitlisted', 'Rejected') NOT NULL DEFAULT 'Approved',
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reg_hackathon
        FOREIGN KEY (hackathon_id) REFERENCES hackathons(hackathon_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_reg_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_user_per_hackathon
        UNIQUE (hackathon_id, user_id)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 7. Teams Table
-- ----------------------------------------------------------------------------
CREATE TABLE teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    hackathon_id INT NOT NULL,
    team_name VARCHAR(120) NOT NULL,
    invitation_code VARCHAR(12) NOT NULL UNIQUE,
    leader_user_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_teams_hackathon
        FOREIGN KEY (hackathon_id) REFERENCES hackathons(hackathon_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_teams_leader
        FOREIGN KEY (leader_user_id) REFERENCES users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT uq_team_name_per_hackathon
        UNIQUE (hackathon_id, team_name)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 8. Team Members Bridge Table (M:N Relationship between Teams and Users)
-- ----------------------------------------------------------------------------
CREATE TABLE team_members (
    team_member_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL,
    user_id INT NOT NULL,
    role_in_team VARCHAR(50) NOT NULL DEFAULT 'Member',
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_teammembers_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_teammembers_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_user_in_team
        UNIQUE (team_id, user_id)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 9. Projects Table (Project Submissions by Teams)
-- ----------------------------------------------------------------------------
CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL UNIQUE,
    hackathon_id INT NOT NULL,
    title VARCHAR(180) NOT NULL,
    abstract TEXT NOT NULL,
    tech_stack VARCHAR(255),
    github_repo_url VARCHAR(300),
    documentation_url VARCHAR(300),
    demo_video_url VARCHAR(300),
    submission_status ENUM('Draft', 'Submitted', 'Under Review', 'Evaluated', 'Disqualified') NOT NULL DEFAULT 'Submitted',
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_projects_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_projects_hackathon
        FOREIGN KEY (hackathon_id) REFERENCES hackathons(hackathon_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 10. Judge Assignments Table
-- ----------------------------------------------------------------------------
CREATE TABLE judge_assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    hackathon_id INT NOT NULL,
    judge_user_id INT NOT NULL,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_judge_hackathon
        FOREIGN KEY (hackathon_id) REFERENCES hackathons(hackathon_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_judge_user
        FOREIGN KEY (judge_user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_judge_hackathon
        UNIQUE (hackathon_id, judge_user_id)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 11. Evaluation Criteria Table
-- ----------------------------------------------------------------------------
CREATE TABLE evaluation_criteria (
    criteria_id INT AUTO_INCREMENT PRIMARY KEY,
    hackathon_id INT NOT NULL,
    criteria_name VARCHAR(100) NOT NULL,
    max_score DECIMAL(5,2) NOT NULL DEFAULT 25.00,
    weight_pct DECIMAL(5,2) NOT NULL DEFAULT 25.00,
    CONSTRAINT fk_criteria_hackathon
        FOREIGN KEY (hackathon_id) REFERENCES hackathons(hackathon_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 12. Evaluations Table (Scoring Rubric per Judge per Project)
-- ----------------------------------------------------------------------------
CREATE TABLE evaluations (
    evaluation_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    judge_user_id INT NOT NULL,
    innovation_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    feasibility_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    technical_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    presentation_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    total_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    feedback TEXT,
    evaluated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_eval_project
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_eval_judge
        FOREIGN KEY (judge_user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_innovation_score
        CHECK (innovation_score >= 0.00 AND innovation_score <= 25.00),
    CONSTRAINT chk_feasibility_score
        CHECK (feasibility_score >= 0.00 AND feasibility_score <= 25.00),
    CONSTRAINT chk_technical_score
        CHECK (technical_score >= 0.00 AND technical_score <= 25.00),
    CONSTRAINT chk_presentation_score
        CHECK (presentation_score >= 0.00 AND presentation_score <= 25.00),
    CONSTRAINT chk_total_score
        CHECK (total_score >= 0.00 AND total_score <= 100.00),
    CONSTRAINT uq_judge_project_eval
        UNIQUE (project_id, judge_user_id)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 13. Attendance Table
-- ----------------------------------------------------------------------------
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    hackathon_id INT NOT NULL,
    user_id INT NOT NULL,
    check_in_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    attendance_status ENUM('Present', 'Absent', 'Excused') NOT NULL DEFAULT 'Present',
    marked_by INT NULL,
    CONSTRAINT fk_att_hackathon
        FOREIGN KEY (hackathon_id) REFERENCES hackathons(hackathon_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_att_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_att_marked_by
        FOREIGN KEY (marked_by) REFERENCES users(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT uq_att_user_hackathon
        UNIQUE (hackathon_id, user_id)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 14. Certificates Table
-- ----------------------------------------------------------------------------
CREATE TABLE certificates (
    certificate_id INT AUTO_INCREMENT PRIMARY KEY,
    certificate_code VARCHAR(36) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    hackathon_id INT NOT NULL,
    team_id INT NULL,
    certificate_type ENUM('Winner', '1st Runner Up', '2nd Runner Up', 'Participation', 'Judge Recognition', 'Mentor Appreciation') NOT NULL DEFAULT 'Participation',
    issue_date DATE NOT NULL,
    verified_count INT NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cert_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_cert_hackathon
        FOREIGN KEY (hackathon_id) REFERENCES hackathons(hackathon_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_cert_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT uq_user_cert_hackathon
        UNIQUE (user_id, hackathon_id, certificate_type)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 15. Notifications Table
-- ----------------------------------------------------------------------------
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    link VARCHAR(255) NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notif_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 16. Audit Logs Table (TCL / Security / Audit Trail)
-- ----------------------------------------------------------------------------
CREATE TABLE audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INT NULL,
    details TEXT,
    ip_address VARCHAR(45) DEFAULT '127.0.0.1',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;
