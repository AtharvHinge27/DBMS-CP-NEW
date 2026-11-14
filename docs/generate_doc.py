"""
InnoSphere Word Documentation Generator
Generates InnoSphere_DBMS_Project_Documentation.docx using python-docx.
Comprehensive academic reference covering all syllabus DBMS concepts for viva.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = os.path.dirname(__file__)
OUTPUT_FILE = os.path.join(DOCS_DIR, "InnoSphere_DBMS_Project_Documentation.docx")

def set_cell_background(cell, fill_hex):
    """Sets background shading of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Sets cell padding in dxa."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_code_block(doc, code_text):
    """Adds a shaded monospace code block."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_callout(doc, title, text, border_color="0F2B5C", bg_color="E8EEF7"):
    """Adds an informative callout box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    
    r_title = p.add_run(f"★ {title}\n")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(10.5)
    r_title.font.color.rgb = RGBColor(15, 43, 92)

    r_text = p.add_run(text)
    r_text.font.name = "Arial"
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def generate_documentation():
    print("Generating comprehensive InnoSphere Word documentation...")
    doc = docx.Document()

    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # Styles
    navy = RGBColor(15, 43, 92)
    gold = RGBColor(217, 119, 6)
    dark = RGBColor(30, 41, 59)

    # -------------------------------------------------------------------------
    # Cover / Title Page
    # -------------------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("ACADEMIC DBMS LABORATORY CAPSTONE PROJECT\nCOMPUTER ENGINEERING & INFORMATION TECHNOLOGY")
    r_inst.bold = True
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(11)
    r_inst.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph().paragraph_format.space_after = Pt(40)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("InnoSphere\n")
    r_title.bold = True
    r_title.font.name = "Georgia"
    r_title.font.size = Pt(30)
    r_title.font.color.rgb = navy

    r_sub = p_title.add_run("Unified Innovation, Hackathon & Research Management Portal\n(Inspired by the AICTE ATAL Academy Portal)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(14)
    r_sub.font.color.rgb = gold

    doc.add_paragraph().paragraph_format.space_after = Pt(30)

    p_desc = doc.add_paragraph()
    p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_desc = p_desc.add_run("A Scalable, Multi-Tenant Relational Database Architecture with\nACID Transactions, Stored Procedures, Functions, Triggers, Views & Dynamic Normalization")
    r_desc.font.name = "Arial"
    r_desc.font.size = Pt(11)
    r_desc.font.color.rgb = dark

    doc.add_paragraph().paragraph_format.space_after = Pt(70)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("Prepared by:\n")
    r_meta.font.name = "Arial"
    r_meta.font.size = Pt(10)
    r_meta.font.color.rgb = RGBColor(100, 116, 139)

    r_author = p_meta.add_run("Atharv Hinge\nSecond Year Computer Engineering\nPune Institute of Computer Technology (PICT)\nAcademic Year 2026 – 2027")
    r_author.bold = True
    r_author.font.name = "Arial"
    r_author.font.size = Pt(11)
    r_author.font.color.rgb = navy

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # Section 1: Project Overview & Vision
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("1. Project Vision & Architecture", level=1)
    h1.runs[0].font.color.rgb = navy

    p = doc.add_paragraph()
    p.add_run(
        "InnoSphere is an enterprise-grade institutional innovation and hackathon management platform engineered from scratch "
        "to solve the widespread fragmentation of student project tracking, hackathon registrations, team formations, and judging workflows across higher education institutions. "
        "Taking inspiration from the national AICTE ATAL (AICTE Training and Learning) Academy portal, InnoSphere provides a unified, multi-college multi-tenant architecture "
        "where administrators, college coordinators, student participants, mentors, and industry judges collaborate seamlessly."
    )

    doc.add_heading("Core Capabilities of InnoSphere:", level=2)
    points = [
        ("Authentication & Role-Based Access Control (RBAC): ", "Dedicated operational portals for Admins, College Coordinators, Participants, Mentors, and Judges with secure password hashing."),
        ("Participant 360° Profile Management: ", "Detailed academic, technical skills, GitHub/LinkedIn repository links, and dynamic profile completion calculation via database functions."),
        ("Internal & External Hackathon Management: ", "Support for both institutional campus hackathons and external national opportunities (SIH, AICTE ATAL) with deadlines and eligibility criteria."),
        ("Team Collaboration & Project Registration: ", "Transactional team formation with auto-generated unique invitation codes, strict capacity enforcement, and project repository submissions."),
        ("Multi-Criteria Evaluation Rubric: ", "Structured 4-factor scoring (Innovation, Feasibility, Technical Execution, Presentation) feeding real-time SQL leaderboard views."),
        ("Attendance Tracking: ", "Verification and attendance check-in roster maintained per event to ensure certificate eligibility."),
        ("Digital Certificate Generation & Verification: ", "Cryptographically unique certificate codes with a public verification portal and automated PDF generation.")
    ]
    for b_title, b_desc in points:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(b_title)
        r1.bold = True
        r1.font.color.rgb = navy
        p.add_run(b_desc)

    add_callout(doc, "Multi-Tenant Scalability",
        "The database is designed from the ground up for multi-college SaaS operation. Every institutional user, department, and event references college_id, allowing independent colleges to operate isolated hackathons while sharing a single unified national platform.")

    doc.add_heading("Dedicated Student Workspace Modules:", level=2)
    p_stu = doc.add_paragraph()
    p_stu.add_run(
        "To provide students with a modern, friction-free experience inspired by national portals, InnoSphere organizes participant features into five dedicated workspace modules:\n"
        "1. My Profile (/profile): Captures student academic credentials, branch, semester, technical skills, and portfolio links. Computes real-time profile completion percentage via MySQL Stored Function fn_calculate_profile_completion.\n"
        "2. My Applications (/applications): Centralized tracker for all registered hackathons, displaying application review status (Applied, Approved, Waitlisted, Rejected), host institutions, team affiliations, and withdrawal actions.\n"
        "3. My Teams (/teams): Facilitates atomic team creation using MySQL Stored Procedure sp_create_team_with_leader, generating cryptographic 8-character invitation codes and enforcing team size boundary constraints.\n"
        "4. My Projects (/projects): Complete project lifecycle hub for submitting abstract, tech stack tags, GitHub repositories, and demo videos, with integrated multi-rubric judge score breakdowns and feedback inspection.\n"
        "5. Certificates & Achievements (/certificates): Displays earned credentials with instant downloadable PDF certificates (generated dynamically via ReportLab) and public cryptographic verification codes."
    )

    doc.add_heading("Expanded Multi-Domain Hackathon Discovery Engine:", level=2)
    p_hack = doc.add_paragraph()
    p_hack.add_run(
        "InnoSphere catalogs 26 curated hackathon opportunities covering both internal campus competitions and premier national/governmental hackathons "
        "(Smart India Hackathon, AICTE ATAL Hackathon, KAVACH Cybersecurity, RBI HarBinger, e-Yantra Robotics, Google Solution Challenge, Microsoft Imagine Cup, and Flipkart GRiD). "
        "The discovery interface provides multi-criteria real-time filtering by:\n"
        "• Technical Domain: AI/ML & GenAI, Web & Mobile, Cybersecurity, Robotics & IoT, Healthcare & FinTech, Sustainability & Smart Cities, Cloud/DevOps, Blockchain, and SpaceTech.\n"
        "• Opportunity Type: Internal (Campus-organized) vs External (National/Governmental).\n"
        "• Registration Status: Open for Registration, In Progress, and Completed.\n"
        "• Search Keywords: Real-time full-text keyword matching across title, host, theme, and description.\n"
        "• Integrity Safeguards: Prevents duplicate registrations at both frontend and database layers (HTTP 409 & unique constraints)."
    )

    # -------------------------------------------------------------------------
    # Section 2: Technology Stack & Connectivity Flow
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("2. Technology Stack & API Connectivity Flow", level=1)
    h1.runs[0].font.color.rgb = navy

    p = doc.add_paragraph()
    p.add_run("The system enforces a clean, modular, beginner-friendly architecture avoiding heavy abstractions or microservices:")

    tech_table = doc.add_table(rows=6, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Layer", "Technology", "Purpose & Architectural Role"]
    for i, h in enumerate(headers):
        cell = tech_table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F2B5C")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].runs[0].font.bold = True

    rows_data = [
        ("Frontend Client", "HTML5, CSS3, JavaScript (Fetch API), Bootstrap 5", "Minimal, modern, light institutional UI with collapsible hamburger sidebar and responsive cards/tables."),
        ("Backend Server", "Python Flask 3.1", "Modular Blueprints (auth, participants, hackathons, teams, evaluations, certificates, admin, notifications)."),
        ("Database Engine", "MySQL 8.0 Community Server", "Normalized relational database executing views, triggers, functions, and ACID procedures."),
        ("Database Driver", "MySQL Connector/Python 8.0+", "Thread-safe connection pooling and parameterized query execution."),
        ("Document / PDF Engine", "ReportLab 4.0 & Python-Docx", "Dynamic on-the-fly certificate PDF generation and automated documentation synthesis.")
    ]
    for r_idx, (layer, tech, role) in enumerate(rows_data, start=1):
        c0 = tech_table.cell(r_idx, 0)
        c0.text = layer
        c0.paragraphs[0].runs[0].font.bold = True
        c1 = tech_table.cell(r_idx, 1)
        c1.text = tech
        c2 = tech_table.cell(r_idx, 2)
        c2.text = role
        for c in [c0, c1, c2]:
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            if r_idx % 2 == 1:
                set_cell_background(c, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    doc.add_heading("End-to-End Request Connectivity Flow:", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "InnoSphere implements a strict 7-stage operational flow for every interaction:\n"
        "1. Frontend Action: User enters data in modal/form and triggers JavaScript Fetch API (async/await).\n"
        "2. HTTP Transmission: Browser sends asynchronous JSON payload to Flask REST endpoint with session cookie.\n"
        "3. Route Handling & RBAC: Flask Blueprint validates request data and verifies caller privileges using @login_required and @role_required.\n"
        "4. Database Connector: Backend acquires an active connection from MySQLConnectionPool and opens a dictionary cursor.\n"
        "5. Parameterized SQL Execution: Queries, stored procedures, or triggers execute inside MySQL 8 using %s placeholders (completely preventing SQL Injection).\n"
        "6. Transaction & Result: Changes commit to InnoDB tables; result rows or status messages are serialized into JSON.\n"
        "7. DOM Updates: Fetch response arrives at frontend; UI immediately updates table rows, shows success toasts, or updates progress meters without full page reloads."
    )

    # -------------------------------------------------------------------------
    # Section 3: Database Normalization (1NF, 2NF, 3NF)
    # -------------------------------------------------------------------------
    doc.add_page_break()
    h1 = doc.add_heading("3. Database Normalization Analysis (1NF, 2NF, 3NF)", level=1)
    h1.runs[0].font.color.rgb = navy

    p = doc.add_paragraph()
    p.add_run(
        "Normalization is a systematic database design technique that decomposes tables to eliminate data redundancy and undesirable anomalies (Insertion, Update, and Deletion anomalies). "
        "InnoSphere is rigorously normalized up to the Third Normal Form (3NF)."
    )

    doc.add_heading("First Normal Form (1NF) Compliance:", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "A relation is in 1NF if and only if all underlying domains contain only atomic (indivisible) values, and there are no repeating groups.\n"
        "• Anti-Pattern Avoided: A naive design might store team members as a comma-separated list of student IDs inside the teams table (e.g., student_ids = '6,7,8'). This violates 1NF because values are not atomic, making querying or indexing individual memberships impossible.\n"
        "• InnoSphere Implementation: We decomposed teams and students into a bridge table called team_members. Each row represents a single atomic (team_id, user_id) pairing with its own primary key and unique constraint."
    )

    doc.add_heading("Second Normal Form (2NF) Compliance:", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "A relation is in 2NF if it is in 1NF and every non-prime attribute is fully functionally dependent on the primary key (no partial functional dependencies).\n"
        "• Anti-Pattern Avoided: In a composite key table such as team_members(team_id, user_id), storing user_name or college_name inside this table would create a partial dependency, because user_name depends solely on user_id, not on (team_id, user_id).\n"
        "• InnoSphere Implementation: All user details remain strictly in the users and participant_profiles tables. The team_members table holds only attributes directly pertaining to the membership relationship (role_in_team, joined_at)."
    )

    doc.add_heading("Third Normal Form (3NF) Compliance:", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "A relation is in 3NF if it is in 2NF and no non-prime attribute is transitively dependent on the primary key (X -> Y and Y -> Z implies X -> Z must be eliminated).\n"
        "• Anti-Pattern Avoided: Storing college_name, city, and state directly inside the users table creates a transitive dependency: user_id -> college_id and college_id -> (college_name, city, state). If the college updates its city, every user record would require an update (Update Anomaly). If all users from a college graduate and are deleted, the college itself would be lost (Deletion Anomaly).\n"
        "• InnoSphere Implementation: We isolated colleges and departments into separate lookup tables. Users store only a foreign key college_id, ensuring zero transitive dependencies."
    )

    # -------------------------------------------------------------------------
    # Section 4: Data Dictionary (All 16 Tables)
    # -------------------------------------------------------------------------
    doc.add_page_break()
    h1 = doc.add_heading("4. Complete Relational Data Dictionary", level=1)
    h1.runs[0].font.color.rgb = navy

    p = doc.add_paragraph()
    p.add_run("The InnoSphere database innosphere_db comprises 16 normalized relational tables, all utilizing the InnoDB storage engine for foreign key constraints and ACID transaction support:")

    table_summaries = [
        ("colleges", "college_id (PK)", "college_code, college_name, city, state, website", "Stores affiliated engineering colleges and institutions for multi-tenant isolation."),
        ("departments", "department_id (PK)", "college_id (FK), department_code, department_name", "Academic departments linked to colleges (e.g., Computer Engineering, IT, AI&DS)."),
        ("users", "user_id (PK)", "college_id (FK), full_name, email, password_hash, role, is_active", "Core authentication and identity entity storing hashed passwords and RBAC roles."),
        ("participant_profiles", "profile_id (PK)", "user_id (FK), roll_number, department_id (FK), branch, year, sem, skills, github, linkedin, bio, profile_completion_pct", "1:1 extension table storing detailed academic records and dynamic profile completion score."),
        ("hackathons", "hackathon_id (PK)", "college_id (FK), title, theme, description, hackathon_type, mode, venue, organizer, deadline, start_date, end_date, min_size, max_size, prize, status", "Internal college hackathons and national external competitions with eligibility and timelines."),
        ("hackathon_registrations", "registration_id (PK)", "hackathon_id (FK), user_id (FK), status, registered_at", "Tracks individual participant registrations and application approval states."),
        ("teams", "team_id (PK)", "hackathon_id (FK), team_name, invitation_code (UQ), leader_user_id (FK)", "Innovation teams formed for a specific hackathon with unique shareable join codes."),
        ("team_members", "team_member_id (PK)", "team_id (FK), user_id (FK), role_in_team, joined_at", "Resolves M:N relationship between Teams and Users with strict capacity limits."),
        ("projects", "project_id (PK)", "team_id (FK, UQ), hackathon_id (FK), title, abstract, tech_stack, github_repo_url, docs_url, demo_video_url, submission_status", "Official hackathon project submissions containing repository links and architecture details."),
        ("judge_assignments", "assignment_id (PK)", "hackathon_id (FK), judge_user_id (FK)", "Authorizes qualified judges to review and grade submissions in designated hackathons."),
        ("evaluation_criteria", "criteria_id (PK)", "hackathon_id (FK), criteria_name, max_score, weight_pct", "Scoring rubric criteria definition (Innovation, Feasibility, Technical, Presentation)."),
        ("evaluations", "evaluation_id (PK)", "project_id (FK), judge_user_id (FK), innovation_score, feasibility_score, technical_score, presentation_score, total_score, feedback", "Multi-rubric score entries submitted by judges with automatic total calculation."),
        ("attendance", "attendance_id (PK)", "hackathon_id (FK), user_id (FK), attendance_status, check_in_time, marked_by (FK)", "Official check-in and participation attendance logs required for credential issuance."),
        ("certificates", "certificate_id (PK)", "certificate_code (UQ), user_id (FK), hackathon_id (FK), team_id (FK), certificate_type, issue_date, verified_count", "Cryptographically verifiable credentials for winners, runners-up, and participants."),
        ("notifications", "notification_id (PK)", "user_id (FK), title, message, link, is_read, created_at", "Real-time system alerts emitted by triggers and stored procedures."),
        ("audit_logs", "log_id (PK)", "user_id (FK), action, entity_type, entity_id, details, ip_address, created_at", "Immutable security audit trail recording all major state changes.")
    ]

    dd_table = doc.add_table(rows=len(table_summaries) + 1, cols=4)
    dd_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    dd_headers = ["Table Name", "Primary Key", "Attributes & Foreign Keys", "Description"]
    for i, h in enumerate(dd_headers):
        cell = dd_table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F2B5C")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        cell.paragraphs[0].runs[0].font.bold = True

    for r_idx, (tname, pk, attrs, desc) in enumerate(table_summaries, start=1):
        c0 = dd_table.cell(r_idx, 0)
        c0.text = tname
        c0.paragraphs[0].runs[0].font.bold = True
        c1 = dd_table.cell(r_idx, 1)
        c1.text = pk
        c2 = dd_table.cell(r_idx, 2)
        c2.text = attrs
        c3 = dd_table.cell(r_idx, 3)
        c3.text = desc
        for c in [c0, c1, c2, c3]:
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            if r_idx % 2 == 1:
                set_cell_background(c, "F8FAFC")

    # -------------------------------------------------------------------------
    # Section 5: DBMS Concepts Implemented with Code & Rationale
    # -------------------------------------------------------------------------
    doc.add_page_break()
    h1 = doc.add_heading("5. In-Depth DBMS Concepts Actually Implemented", level=1)
    h1.runs[0].font.color.rgb = navy

    p = doc.add_paragraph()
    p.add_run(
        "This section details every major DBMS concept implemented in InnoSphere. "
        "Each topic includes its formal theoretical definition, purpose, actual SQL implementation, and where it functions in the live web application."
    )

    # 5.1 Primary Keys, Foreign Keys & Cascading
    doc.add_heading("5.1 Primary Keys, Foreign Keys & Referential Integrity", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• Definition: A Primary Key is a minimal superkey that uniquely identifies each tuple in a relation and cannot contain NULL values. A Foreign Key is a set of attributes in a referencing table whose values match a candidate key of a referenced table, enforcing referential integrity.\n"
        "• Purpose: Prevents orphaned records (e.g. team members belonging to a non-existent team) and maintains relational links across multi-institution data.\n"
        "• Where Used: Implemented in all 16 tables. Uses ON DELETE CASCADE for dependent bridge records (e.g., deleting a team automatically cascades to team_members and projects), while using ON DELETE RESTRICT for team leaders (preventing deletion of a student who currently leads an active team)."
    )
    add_code_block(doc, """-- Example from 02_create_tables.sql
CONSTRAINT fk_teammembers_team
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT fk_teams_leader
    FOREIGN KEY (leader_user_id) REFERENCES users(user_id)
    ON DELETE RESTRICT ON UPDATE CASCADE;""")

    # 5.2 Integrity Constraints
    doc.add_heading("5.2 Check Constraints & Domain Integrity", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• Definition: Integrity constraints enforce business rules directly at the database engine level, rejecting any insertion or modification that violates specified relational or range predicates.\n"
        "• Purpose: Guarantees data validity even if application code fails to validate inputs.\n"
        "• Where Used: Hackathon dates validation (chk_hackathon_dates: end_date >= start_date), student year validation (chk_year_of_study: 1 to 5), and evaluation scores (chk_total_score: 0.00 to 100.00)."
    )
    add_code_block(doc, """-- Example from 02_create_tables.sql
CONSTRAINT chk_hackathon_dates CHECK (end_date >= start_date),
CONSTRAINT chk_reg_deadline CHECK (start_date >= registration_deadline),
CONSTRAINT chk_total_score CHECK (total_score >= 0.00 AND total_score <= 100.00);""")

    # 5.3 Joins
    doc.add_heading("5.3 SQL Joins (INNER JOIN & LEFT OUTER JOIN)", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• Definition: An INNER JOIN returns only records that have matching values in both tables based on a join condition. A LEFT OUTER JOIN returns all rows from the left table and matched rows from the right table, substituting NULLs when no match exists.\n"
        "• Purpose: Combines normalized relations to present unified views to the user.\n"
        "• Where Used:\n"
        "  - INNER JOIN: Used in project listings to pair projects strictly with their valid teams and hackathons.\n"
        "  - LEFT JOIN: Used in user profile views to show participants who may not yet have chosen a department, phone number, or GitHub URL without dropping them from view."
    )
    add_code_block(doc, """-- INNER JOIN Example: Project & Team & College pairing
SELECT p.title, t.team_name, u.full_name AS leader, c.college_name
FROM projects p
INNER JOIN teams t ON p.team_id = t.team_id
INNER JOIN users u ON t.leader_user_id = u.user_id
INNER JOIN colleges c ON u.college_id = c.college_id;

-- LEFT JOIN Example: Hackathons with or without project submissions
SELECT h.title, COALESCE(p.title, 'No Projects Submitted Yet') AS submission
FROM hackathons h
LEFT JOIN projects p ON h.hackathon_id = p.hackathon_id;""")

    # 5.4 Aggregation & GROUP BY / HAVING
    doc.add_heading("5.4 Aggregate Functions, GROUP BY and HAVING Clause", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• Definition: Aggregate functions (COUNT, AVG, SUM, MIN, MAX) compute summary statistics across multiple rows. The GROUP BY clause partitions rows into summary buckets based on common column values. The HAVING clause filters these grouped buckets based on aggregate conditions (acting after grouping, unlike WHERE which filters before grouping).\n"
        "• Purpose: Computes college-wide participation metrics, average judge evaluation marks, and team member headcounts.\n"
        "• Where Used: Used in the Admin Analytics console to filter colleges that have 2 or more registered student innovators."
    )
    add_code_block(doc, """-- Aggregate & HAVING Query from 09_advanced_queries.sql
SELECT 
    c.college_name,
    COUNT(u.user_id) AS total_students
FROM colleges c
INNER JOIN users u ON c.college_id = u.college_id
WHERE u.role = 'Participant'
GROUP BY c.college_id, c.college_name
HAVING COUNT(u.user_id) >= 2
ORDER BY total_students DESC;""")

    # 5.5 Database Views
    doc.add_heading("5.5 Database Views (Virtual Tables)", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• Definition: A View is a virtual table defined by a saved SQL query. It does not store physical data itself (unless materialized), but dynamically executes its definition whenever queried.\n"
        "• Purpose: Encapsulates complex joins and calculations, simplifies application code, and enforces security through data abstraction.\n"
        "• Where Used in InnoSphere:\n"
        "  1. vw_hackathon_leaderboard: Aggregates project scores, calculates averages, and computes dynamic ranks using DENSE_RANK() OVER (PARTITION BY hackathon_id ORDER BY AVG(total_score) DESC).\n"
        "  2. vw_participant_summary: Aggregates student personal info, department, skills, completion %, registered hackathons count, and earned certificates count.\n"
        "  3. vw_hackathon_statistics: Institutional overview aggregating registrations, teams, projects, and judges.\n"
        "  4. vw_team_roster: Flattens team structures, showing leader, members count, and recruiting status."
    )
    add_code_block(doc, """-- Definition of vw_hackathon_leaderboard (04_views.sql)
CREATE OR REPLACE VIEW vw_hackathon_leaderboard AS
SELECT 
    h.hackathon_id, h.title AS hackathon_title,
    p.project_id, p.title AS project_title,
    t.team_name, u.full_name AS leader_name,
    COUNT(e.evaluation_id) AS total_evaluations,
    ROUND(COALESCE(AVG(e.total_score), 0.00), 2) AS average_score,
    DENSE_RANK() OVER (
        PARTITION BY h.hackathon_id 
        ORDER BY COALESCE(AVG(e.total_score), 0.00) DESC
    ) AS leaderboard_rank
FROM projects p
JOIN teams t ON p.team_id = t.team_id
JOIN hackathons h ON p.hackathon_id = h.hackathon_id
JOIN users u ON t.leader_user_id = u.user_id
LEFT JOIN evaluations e ON p.project_id = e.project_id
GROUP BY h.hackathon_id, h.title, p.project_id, p.title, t.team_name, u.full_name;""")

    # 5.6 Stored Functions
    doc.add_heading("5.6 Stored Functions", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• Definition: A Stored Function is a compiled set of SQL statements that accepts input parameters, performs computations, and returns a single scalar value. Stored functions can be called directly within SELECT queries.\n"
        "• Purpose: Centralizes business logic calculations in the database engine, ensuring identical output whether queried by web app, reports, or administrative scripts.\n"
        "• Where Used: fn_calculate_profile_completion(user_id) computes the completion percentage (0 - 100%) dynamically based on academic roll number, department, skills, and links."
    )
    add_code_block(doc, """-- Stored Function from 05_functions.sql
CREATE FUNCTION fn_calculate_profile_completion(p_user_id INT)
RETURNS INT DETERMINISTIC READS SQL DATA
BEGIN
    DECLARE v_score INT DEFAULT 15; -- Base registration
    -- Checks roll_number (+15%), dept (+10%), branch (+10%), year (+10%),
    -- phone (+10%), skills (+15%), github/linkedin (+15%)...
    IF v_score > 100 THEN SET v_score = 100; END IF;
    RETURN v_score;
END;""")

    # 5.7 Stored Procedures & ACID Transactions
    doc.add_heading("5.7 Stored Procedures & ACID Transactions", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• Definition: A Stored Procedure is a subroutine stored in the database catalog that can execute procedural code, modify multiple tables, and manage transaction boundaries (START TRANSACTION, COMMIT, ROLLBACK).\n"
        "• ACID Properties Demonstration:\n"
        "  - Atomicity: In sp_create_team_with_leader, creating the team in teams and inserting the leader into team_members must both succeed, or both be rolled back via DECLARE EXIT HANDLER FOR SQLEXCEPTION.\n"
        "  - Consistency: Enforced via constraints (unique invitation code, capacity checks, foreign keys).\n"
        "  - Isolation: Concurrent transactions cannot read uncommitted team insertions (Repeatable Read isolation).\n"
        "  - Durability: Committed transactions persist to write-ahead redo logs on disk.\n"
        "• Where Used: sp_create_team_with_leader, sp_join_team_by_code, sp_record_evaluation, sp_issue_certificate."
    )
    add_code_block(doc, """-- Stored Procedure with ACID Transaction (06_stored_procedures.sql)
CREATE PROCEDURE sp_create_team_with_leader(
    IN p_hackathon_id INT, IN p_team_name VARCHAR(120),
    IN p_invitation_code VARCHAR(12), IN p_leader_user_id INT,
    OUT p_out_team_id INT, OUT p_status_message VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK; -- Atomicity guarantee: revert all changes on error
        SET p_status_message = 'ERROR: Transaction rolled back.';
    END;

    START TRANSACTION;
    INSERT INTO teams (hackathon_id, team_name, invitation_code, leader_user_id)
    VALUES (p_hackathon_id, p_team_name, p_invitation_code, p_leader_user_id);
    SET p_out_team_id = LAST_INSERT_ID();

    INSERT INTO team_members (team_id, user_id, role_in_team)
    VALUES (p_out_team_id, p_leader_user_id, 'Leader');

    INSERT INTO audit_logs (user_id, action, entity_type, entity_id)
    VALUES (p_leader_user_id, 'CREATE_TEAM', 'teams', p_out_team_id);

    COMMIT; -- Persist atomically
END;""")

    # 5.8 Database Triggers
    doc.add_heading("5.8 Database Triggers (Automated Actions)", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• Definition: A Trigger is a specialized stored program that automatically executes (fires) in response to a specific DML event (INSERT, UPDATE, DELETE) on a specified table.\n"
        "• Purpose: Enforces complex cross-table business logic, automatic entity lifecycle initialization, audit logging, and data integrity guarantees that cannot be bypassed.\n"
        "• Where Used in InnoSphere:\n"
        "  1. trg_after_user_insert: Automatically creates a corresponding row in participant_profiles and sends a welcome notification when a new student registers.\n"
        "  2. trg_before_evaluation_insert / update: Automatically sums NEW.total_score from the 4 sub-criteria and rejects scores exceeding 100 via SIGNAL SQLSTATE '45000'.\n"
        "  3. trg_after_project_insert: Automatically generates notifications for all team members and logs a system audit entry when a team submits a project."
    )
    add_code_block(doc, """-- Trigger Example: Auto-summing evaluation scores (07_triggers.sql)
CREATE TRIGGER trg_before_evaluation_insert
BEFORE INSERT ON evaluations
FOR EACH ROW
BEGIN
    SET NEW.total_score = NEW.innovation_score + NEW.feasibility_score + 
                          NEW.technical_score + NEW.presentation_score;
    IF NEW.total_score > 100.00 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Validation Error: Total score cannot exceed 100.00';
    END IF;
END;""")

    # 5.9 B-Tree Indexing
    doc.add_heading("5.9 Database Indexing Strategies", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• Definition: An Index is an auxiliary data structure (typically a B+ Tree in MySQL InnoDB) that enables high-speed retrieval of rows without performing a sequential full table scan (O(log N) vs O(N)).\n"
        "• Purpose: Optimizes search queries on high-cardinality foreign keys, role filters, deadline ranges, and public verification hashes.\n"
        "• Where Used: Indexes created on users(role), hackathons(status, hackathon_type), certificates(certificate_code), and evaluations(project_id)."
    )
    add_code_block(doc, """-- Indexing Script excerpt (03_indexes.sql)
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_hackathons_status_type ON hackathons(status, hackathon_type);
CREATE INDEX idx_certificates_code ON certificates(certificate_code);""")

    # 5.10 DCL and TCL
    doc.add_heading("5.10 DCL (Data Control) & TCL (Transaction Control)", level=2)
    p = doc.add_paragraph()
    p.add_run(
        "• DCL (Data Control Language): Uses GRANT and REVOKE commands to enforce the Principle of Least Privilege. In InnoSphere, web applications connect using a dedicated database user with standard DML privileges, while evaluation judges are granted SELECT on leaderboard views and INSERT/UPDATE on evaluations.\n"
        "• TCL (Transaction Control Language): Employs START TRANSACTION, COMMIT, ROLLBACK, and SAVEPOINT to maintain consistent database states during multi-table writes."
    )

    # -------------------------------------------------------------------------
    # Section 6: Viva Questions and Answers (Student Guide)
    # -------------------------------------------------------------------------
    doc.add_page_break()
    h1 = doc.add_heading("6. Second-Year DBMS Viva Preparation & Interview Questions", level=1)
    h1.runs[0].font.color.rgb = navy

    p = doc.add_paragraph()
    p.add_run(
        "This section prepares second-year Computer Engineering students to confidently answer faculty and external examiner viva questions regarding InnoSphere's architecture and DBMS implementation."
    )

    viva_qas = [
        ("Q1: What is the primary difference between a View and a Table?",
         "A Table is a physical relation stored on disk containing actual data tuples. A View is a virtual relation defined by an underlying SQL query; it does not occupy data storage (except its definition in the data dictionary) and executes dynamically when queried. In InnoSphere, vw_hackathon_leaderboard is a view that calculates ranks dynamically without duplicating project data."),

        ("Q2: Why did you separate participant_profiles from the users table?",
         "This enforces the Single Responsibility Principle and eliminates NULL pollution. The users table stores core authentication attributes (email, password_hash, role) common to all actors (Admins, Judges, Mentors). The participant_profiles table stores student-specific attributes (roll_number, year, branch, GitHub) in a 1:1 relationship. If all fields were in users, 80% of rows for admins or judges would have null academic fields."),

        ("Q3: What are the ACID properties and how did you guarantee Atomicity in InnoSphere?",
         "ACID stands for Atomicity, Consistency, Isolation, and Durability. In InnoSphere, Atomicity is guaranteed in sp_create_team_with_leader: we begin with START TRANSACTION and define DECLARE EXIT HANDLER FOR SQLEXCEPTION. If inserting the team succeeds but inserting the leader fails, the handler immediately issues a ROLLBACK, ensuring the database never holds a team without a leader."),

        ("Q4: Explain the difference between WHERE and HAVING clauses.",
         "The WHERE clause filters individual rows before any grouping occurs. The HAVING clause filters aggregated groups after GROUP BY has formed the groups. In InnoSphere, WHERE u.role = 'Participant' filters rows first, and HAVING COUNT(u.user_id) >= 2 filters colleges that have at least two participating students."),

        ("Q5: What is the purpose of the ON DELETE CASCADE constraint?",
         "ON DELETE CASCADE automatically deletes referencing child rows when a referenced parent row is deleted. In InnoSphere, if a team is deleted, its team_members entries and project submissions are automatically cascaded. However, for team leaders, we used ON DELETE RESTRICT to prevent deleting a user who is currently designated as a team leader."),

        ("Q6: How does a Stored Procedure differ from a Stored Function in MySQL?",
         "A Stored Function must return exactly one scalar value and can be called directly within a SELECT statement (e.g. SELECT fn_calculate_profile_completion(6);). A Stored Procedure does not have a formal return type, can return multiple OUT parameters, can execute DML transactions (COMMIT/ROLLBACK), and is invoked using the CALL keyword."),

        ("Q7: How did you prevent SQL Injection attacks in InnoSphere?",
         "We used Parameterized Queries with MySQL Connector/Python using %s placeholders. User inputs are sent separately from the SQL statement to the database engine as literal values, never concatenated as raw strings. Thus, malicious input such as \"' OR 1=1 --\" is treated strictly as literal characters, eliminating SQL Injection vulnerabilities."),

        ("Q8: What type of Index did you use and why?",
         "We used B-Tree (Balanced Tree) indexes, which are the default index structure in MySQL's InnoDB storage engine. B-Trees keep data sorted and allow search, sequential access, insertions, and deletions in O(log N) logarithmic time. We indexed certificate_code, hackathon status/dates, and user roles to accelerate frequent lookups.")
    ]

    for q, a in viva_qas:
        p_q = doc.add_paragraph()
        r_q = p_q.add_run(q)
        r_q.bold = True
        r_q.font.color.rgb = navy
        p_a = doc.add_paragraph()
        p_a.add_run(a)
        p_a.paragraph_format.space_after = Pt(8)

    # Save document
    doc.save(OUTPUT_FILE)
    print(f"Document successfully created at: {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE)} bytes")

if __name__ == '__main__':
    generate_documentation()
