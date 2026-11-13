"""
InnoSphere Admin & Coordinator Management Module
Handles college directory, user roles, judge assignments, analytics, and institutional reports.
"""

from flask import Blueprint, request, jsonify, session
from modules.db import query_one, query_all, execute_dml
from modules.auth import login_required, role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@admin_bp.route('/stats', methods=['GET'])
@login_required
@role_required('Admin', 'College Coordinator')
def get_admin_dashboard_stats():
    """
    Returns high-level institutional metrics:
    - Counts of colleges, departments, users, participants, hackathons, teams, projects, evaluations, certificates
    - Comprehensive hackathon statistics from vw_hackathon_statistics
    - Top colleges by student participation
    """
    college_id = session.get('college_id')
    user_role = session.get('role')

    # Total counts
    total_colleges = query_one("SELECT COUNT(*) AS count FROM colleges;")['count']
    total_depts = query_one("SELECT COUNT(*) AS count FROM departments;")['count']
    total_users = query_one("SELECT COUNT(*) AS count FROM users;")['count']
    total_participants = query_one("SELECT COUNT(*) AS count FROM users WHERE role = 'Participant';")['count']
    total_judges = query_one("SELECT COUNT(*) AS count FROM users WHERE role = 'Judge';")['count']
    total_hackathons = query_one("SELECT COUNT(*) AS count FROM hackathons;")['count']
    total_teams = query_one("SELECT COUNT(*) AS count FROM teams;")['count']
    total_projects = query_one("SELECT COUNT(*) AS count FROM projects;")['count']
    total_evaluations = query_one("SELECT COUNT(*) AS count FROM evaluations;")['count']
    total_certificates = query_one("SELECT COUNT(*) AS count FROM certificates;")['count']

    # Hackathon detailed stats from view
    hackathon_stats = query_all("SELECT * FROM vw_hackathon_statistics;")

    # College participation distribution (DBMS GROUP BY + COUNT + HAVING demonstration)
    college_stats = query_all("""
        SELECT 
            c.college_id, c.college_name, c.city,
            COUNT(u.user_id) AS total_students
        FROM colleges c
        LEFT JOIN users u ON c.college_id = u.college_id AND u.role = 'Participant'
        GROUP BY c.college_id, c.college_name, c.city
        ORDER BY total_students DESC;
    """)

    # Recent Audit Logs
    recent_logs = query_all("""
        SELECT l.*, u.full_name, u.email
        FROM audit_logs l
        LEFT JOIN users u ON l.user_id = u.user_id
        ORDER BY l.created_at DESC
        LIMIT 10;
    """)

    return jsonify({
        'success': True,
        'metrics': {
            'total_colleges': total_colleges,
            'total_departments': total_depts,
            'total_users': total_users,
            'total_participants': total_participants,
            'total_judges': total_judges,
            'total_hackathons': total_hackathons,
            'total_teams': total_teams,
            'total_projects': total_projects,
            'total_evaluations': total_evaluations,
            'total_certificates': total_certificates
        },
        'hackathon_stats': hackathon_stats,
        'college_stats': college_stats,
        'recent_logs': recent_logs
    })


@admin_bp.route('/colleges', methods=['GET', 'POST'])
def manage_colleges():
    """Lists or adds colleges."""
    if request.method == 'GET':
        colleges = query_all("SELECT * FROM colleges ORDER BY college_name ASC;")
        return jsonify({'success': True, 'colleges': colleges})

    # POST: Add College (Admin only)
    if 'user_id' not in session or session.get('role') != 'Admin':
        return jsonify({'success': False, 'message': 'Admin privilege required.'}), 403

    data = request.get_json() or {}
    code = data.get('college_code', '').strip().upper()
    name = data.get('college_name', '').strip()
    city = data.get('city', '').strip()
    state = data.get('state', '').strip()
    website = data.get('website', '').strip()

    if not code or not name or not city or not state:
        return jsonify({'success': False, 'message': 'Code, Name, City, and State are required.'}), 400

    try:
        college_id, _ = execute_dml("""
            INSERT INTO colleges (college_code, college_name, city, state, website)
            VALUES (%s, %s, %s, %s, %s);
        """, (code, name, city, state, website or None))

        return jsonify({'success': True, 'message': 'College added successfully!', 'college_id': college_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error adding college: {str(e)}'}), 400


@admin_bp.route('/departments', methods=['GET', 'POST'])
def manage_departments():
    """Lists departments (optionally filtered by college_id) or adds a new department."""
    if request.method == 'GET':
        college_id = request.args.get('college_id')
        if college_id:
            departments = query_all("""
                SELECT d.*, c.college_name 
                FROM departments d
                JOIN colleges c ON d.college_id = c.college_id
                WHERE d.college_id = %s
                ORDER BY d.department_name ASC;
            """, (college_id,))
        else:
            departments = query_all("""
                SELECT d.*, c.college_name 
                FROM departments d
                JOIN colleges c ON d.college_id = c.college_id
                ORDER BY c.college_name ASC, d.department_name ASC;
            """)
        return jsonify({'success': True, 'departments': departments})

    # POST: Add Department (Admin or Coordinator)
    if 'user_id' not in session or session.get('role') not in ['Admin', 'College Coordinator']:
        return jsonify({'success': False, 'message': 'Admin or Coordinator privilege required.'}), 403

    data = request.get_json() or {}
    college_id = data.get('college_id') or session.get('college_id')
    dept_code = data.get('department_code', '').strip().upper()
    dept_name = data.get('department_name', '').strip()

    if not college_id or not dept_code or not dept_name:
        return jsonify({'success': False, 'message': 'College ID, Department Code, and Department Name are required.'}), 400

    try:
        dept_id, _ = execute_dml("""
            INSERT INTO departments (college_id, department_code, department_name)
            VALUES (%s, %s, %s);
        """, (college_id, dept_code, dept_name))

        return jsonify({'success': True, 'message': 'Department created successfully!', 'department_id': dept_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error creating department: {str(e)}'}), 400


@admin_bp.route('/assign-judge', methods=['POST'])
@login_required
@role_required('Admin', 'College Coordinator')
def assign_judge():
    """Assigns an authorized Judge to a Hackathon."""
    data = request.get_json() or {}
    hackathon_id = data.get('hackathon_id')
    judge_user_id = data.get('judge_user_id')

    if not hackathon_id or not judge_user_id:
        return jsonify({'success': False, 'message': 'Hackathon ID and Judge User ID are required.'}), 400

    # Verify user is a Judge
    judge = query_one("SELECT user_id, full_name FROM users WHERE user_id = %s AND role = 'Judge';", (judge_user_id,))
    if not judge:
        return jsonify({'success': False, 'message': 'User is not registered as a Judge.'}), 400

    try:
        execute_dml("""
            INSERT INTO judge_assignments (hackathon_id, judge_user_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE assigned_at = NOW();
        """, (hackathon_id, judge_user_id))

        # Notify Judge
        execute_dml("""
            INSERT INTO notifications (user_id, title, message, link)
            VALUES (%s, 'New Judge Assignment', 'You have been assigned to evaluate projects for a hackathon.', '/evaluations');
        """, (judge_user_id,))

        return jsonify({'success': True, 'message': f'Judge {judge["full_name"]} assigned successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error assigning judge: {str(e)}'}), 400


@admin_bp.route('/judges', methods=['GET'])
@login_required
def list_available_judges():
    """Lists all registered Judges."""
    judges = query_all("""
        SELECT u.user_id, u.full_name, u.email, c.college_name
        FROM users u
        LEFT JOIN colleges c ON u.college_id = c.college_id
        WHERE u.role = 'Judge' AND u.is_active = TRUE
        ORDER BY u.full_name ASC;
    """)
    return jsonify({'success': True, 'judges': judges})


@admin_bp.route('/users', methods=['GET'])
@login_required
@role_required('Admin', 'College Coordinator')
def list_all_users():
    """Lists users with optional role filtering."""
    role = request.args.get('role')
    sql = """
        SELECT 
            u.user_id, u.full_name, u.email, u.role, u.is_active, u.created_at,
            c.college_name,
            pp.roll_number, pp.branch, pp.profile_completion_pct
        FROM users u
        LEFT JOIN colleges c ON u.college_id = c.college_id
        LEFT JOIN participant_profiles pp ON u.user_id = pp.user_id
        WHERE 1=1
    """
    params = []
    if role and role != 'All':
        sql += " AND u.role = %s"
        params.append(role)

    sql += " ORDER BY u.created_at DESC;"
    users = query_all(sql, params)
    return jsonify({'success': True, 'users': users})
