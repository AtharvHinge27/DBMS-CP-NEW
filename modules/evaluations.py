"""
InnoSphere Evaluation & Leaderboard Module
Handles judge assignments, rubric scoring, real-time leaderboards, and attendance tracking.
"""

from flask import Blueprint, request, jsonify, session
from modules.db import query_one, query_all, execute_dml, get_db
from modules.auth import login_required, role_required

evaluations_bp = Blueprint('evaluations', __name__, url_prefix='/api/evaluations')


@evaluations_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    Fetches the real-time project leaderboard using view vw_hackathon_leaderboard.
    Supports filtering by hackathon_id.
    """
    hackathon_id = request.args.get('hackathon_id')

    sql = "SELECT * FROM vw_hackathon_leaderboard"
    params = []
    if hackathon_id:
        sql += " WHERE hackathon_id = %s"
        params.append(hackathon_id)

    sql += " ORDER BY hackathon_id ASC, leaderboard_rank ASC;"

    leaderboard = query_all(sql, params)
    return jsonify({'success': True, 'leaderboard': leaderboard})


@evaluations_bp.route('/assigned-projects', methods=['GET'])
@login_required
@role_required('Judge', 'Admin')
def get_assigned_projects():
    """
    Fetches all projects assigned to the current judge for evaluation.
    """
    judge_user_id = session['user_id']
    role = session['role']

    if role == 'Admin':
        # Admin can view all projects across all hackathons
        projects = query_all("""
            SELECT 
                p.project_id, p.hackathon_id, p.title AS project_title,
                p.abstract, p.tech_stack, p.github_repo_url, p.documentation_url,
                p.submission_status, p.submitted_at,
                t.team_id, t.team_name,
                h.title AS hackathon_title,
                COALESCE(e.total_score, 0.00) AS my_score,
                (CASE WHEN e.evaluation_id IS NOT NULL THEN TRUE ELSE FALSE END) AS is_evaluated
            FROM projects p
            JOIN teams t ON p.team_id = t.team_id
            JOIN hackathons h ON p.hackathon_id = h.hackathon_id
            LEFT JOIN evaluations e ON p.project_id = e.project_id AND e.judge_user_id = %s
            ORDER BY h.hackathon_id ASC, p.submitted_at DESC;
        """, (judge_user_id,))
    else:
        # Judge can view projects in hackathons they are assigned to
        projects = query_all("""
            SELECT 
                p.project_id, p.hackathon_id, p.title AS project_title,
                p.abstract, p.tech_stack, p.github_repo_url, p.documentation_url,
                p.submission_status, p.submitted_at,
                t.team_id, t.team_name,
                h.title AS hackathon_title,
                COALESCE(e.total_score, 0.00) AS my_score,
                (CASE WHEN e.evaluation_id IS NOT NULL THEN TRUE ELSE FALSE END) AS is_evaluated,
                e.innovation_score, e.feasibility_score, e.technical_score, e.presentation_score,
                e.feedback
            FROM judge_assignments ja
            JOIN hackathons h ON ja.hackathon_id = h.hackathon_id
            JOIN projects p ON h.hackathon_id = p.hackathon_id
            JOIN teams t ON p.team_id = t.team_id
            LEFT JOIN evaluations e ON p.project_id = e.project_id AND e.judge_user_id = %s
            WHERE ja.judge_user_id = %s
            ORDER BY p.submitted_at DESC;
        """, (judge_user_id, judge_user_id))

    return jsonify({'success': True, 'projects': projects})


@evaluations_bp.route('/submit', methods=['POST'])
@login_required
@role_required('Judge', 'Admin')
def submit_evaluation():
    """
    Submits or updates an evaluation score using Stored Procedure sp_record_evaluation.
    Scores: Innovation (0-25), Feasibility (0-25), Technical (0-25), Presentation (0-25).
    Total score is calculated automatically and triggers update project status.
    """
    judge_user_id = session['user_id']
    data = request.get_json() or {}

    project_id = data.get('project_id')
    innovation = float(data.get('innovation_score', 0))
    feasibility = float(data.get('feasibility_score', 0))
    technical = float(data.get('technical_score', 0))
    presentation = float(data.get('presentation_score', 0))
    feedback = data.get('feedback', '').strip()

    if not project_id:
        return jsonify({'success': False, 'message': 'Project ID is required.'}), 400

    # Bounds validation
    for name, val in [('Innovation', innovation), ('Feasibility', feasibility), ('Technical', technical), ('Presentation', presentation)]:
        if val < 0 or val > 25:
            return jsonify({'success': False, 'message': f'{name} score must be between 0 and 25.'}), 400

    # Execute Stored Procedure sp_record_evaluation
    with get_db(commit=True) as (cursor, conn):
        try:
            cursor.callproc('sp_record_evaluation', [
                int(project_id),
                judge_user_id,
                innovation,
                feasibility,
                technical,
                presentation,
                feedback,
                0.00,  # OUT p_out_total
                ''     # OUT p_status_message
            ])

            # Query updated evaluation
            cursor.execute("""
                SELECT total_score, evaluated_at 
                FROM evaluations 
                WHERE project_id = %s AND judge_user_id = %s;
            """, (project_id, judge_user_id))
            recorded_eval = cursor.fetchone()

            total_score = recorded_eval['total_score'] if recorded_eval else (innovation + feasibility + technical + presentation)

            return jsonify({
                'success': True,
                'message': 'Evaluation and scoring recorded successfully!',
                'total_score': float(total_score)
            })

        except Exception as e:
            return jsonify({'success': False, 'message': f'Evaluation error: {str(e)}'}), 400


# -----------------------------------------------------------------------------
# Attendance Tracking APIs
# -----------------------------------------------------------------------------
@evaluations_bp.route('/attendance/<int:hackathon_id>', methods=['GET'])
@login_required
@role_required('Admin', 'College Coordinator', 'Judge')
def get_hackathon_attendance(hackathon_id):
    """Fetches attendance roster for a specific hackathon."""
    attendance_records = query_all("""
        SELECT 
            hr.user_id, hr.status AS registration_status,
            u.full_name, u.email,
            c.college_name,
            pp.roll_number, pp.branch,
            t.team_name,
            att.attendance_id,
            COALESCE(att.attendance_status, 'Absent') AS attendance_status,
            att.check_in_time
        FROM hackathon_registrations hr
        JOIN users u ON hr.user_id = u.user_id
        LEFT JOIN colleges c ON u.college_id = c.college_id
        LEFT JOIN participant_profiles pp ON u.user_id = pp.user_id
        LEFT JOIN team_members tm ON u.user_id = tm.user_id
        LEFT JOIN teams t ON tm.team_id = t.team_id AND t.hackathon_id = hr.hackathon_id
        LEFT JOIN attendance att ON hr.hackathon_id = att.hackathon_id AND hr.user_id = att.user_id
        WHERE hr.hackathon_id = %s
        ORDER BY u.full_name ASC;
    """, (hackathon_id,))

    return jsonify({'success': True, 'attendance': attendance_records})


@evaluations_bp.route('/attendance/mark', methods=['POST'])
@login_required
@role_required('Admin', 'College Coordinator')
def mark_attendance():
    """Marks or updates attendance for a participant in a hackathon."""
    data = request.get_json() or {}
    hackathon_id = data.get('hackathon_id')
    user_id = data.get('user_id')
    status = data.get('attendance_status', 'Present')

    if not hackathon_id or not user_id:
        return jsonify({'success': False, 'message': 'Hackathon ID and User ID are required.'}), 400

    execute_dml("""
        INSERT INTO attendance (hackathon_id, user_id, attendance_status, marked_by, check_in_time)
        VALUES (%s, %s, %s, %s, NOW())
        ON DUPLICATE KEY UPDATE
            attendance_status = VALUES(attendance_status),
            marked_by = VALUES(marked_by),
            check_in_time = NOW();
    """, (hackathon_id, user_id, status, session['user_id']))

    return jsonify({'success': True, 'message': f'Attendance marked as {status}.'})


@evaluations_bp.route('/my-attendance', methods=['GET'])
@login_required
def get_my_attendance():
    """Fetches attendance records for the logged-in student across all hackathons."""
    user_id = session['user_id']
    records = query_all("""
        SELECT 
            h.hackathon_id, h.title AS hackathon_title, h.theme, h.start_date, h.end_date, h.mode, h.venue,
            COALESCE(c.college_name, 'National Opportunity') AS host_college,
            COALESCE(att.attendance_status, 'Present') AS attendance_status,
            COALESCE(att.check_in_time, hr.registered_at) AS check_in_time,
            COALESCE(u_marked.full_name, 'Event Organizing Committee') AS marked_by_name
        FROM hackathon_registrations hr
        JOIN hackathons h ON hr.hackathon_id = h.hackathon_id
        LEFT JOIN colleges c ON h.college_id = c.college_id
        LEFT JOIN attendance att ON hr.hackathon_id = att.hackathon_id AND hr.user_id = att.user_id
        LEFT JOIN users u_marked ON att.marked_by = u_marked.user_id
        WHERE hr.user_id = %s
        ORDER BY h.start_date DESC;
    """, (user_id,))
    return jsonify({'success': True, 'attendance': records})

