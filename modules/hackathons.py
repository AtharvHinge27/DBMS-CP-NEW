"""
InnoSphere Hackathon Management Module
Manages internal and external hackathons, discovery filters, and registrations.
"""

from flask import Blueprint, request, jsonify, session
from modules.db import query_one, query_all, execute_dml
from modules.auth import login_required, role_required

hackathons_bp = Blueprint('hackathons', __name__, url_prefix='/api/hackathons')


@hackathons_bp.route('', methods=['GET'])
def list_hackathons():
    """
    Lists hackathons with dynamic search and filtering:
    - type: 'Internal', 'External', or 'All'
    - status: 'Open', 'Completed', etc.
    - search: search keyword matching title, theme, description, or organizer
    """
    hackathon_type = request.args.get('type')
    status = request.args.get('status')
    search = request.args.get('search', '').strip()

    sql = """
        SELECT 
            h.hackathon_id, h.college_id, h.title, h.theme, h.description,
            h.hackathon_type, h.mode, h.venue, h.organizer_name, h.eligibility,
            h.external_url, h.registration_deadline, h.start_date, h.end_date,
            h.min_team_size, h.max_team_size, h.prize_pool, h.status,
            COALESCE(c.college_name, 'National / External Opportunity') AS host_college,
            (SELECT COUNT(*) FROM hackathon_registrations hr WHERE hr.hackathon_id = h.hackathon_id) AS total_registrations,
            (SELECT COUNT(*) FROM teams t WHERE t.hackathon_id = h.hackathon_id) AS total_teams
        FROM hackathons h
        LEFT JOIN colleges c ON h.college_id = c.college_id
        WHERE 1=1
    """
    params = []

    if hackathon_type and hackathon_type != 'All':
        sql += " AND h.hackathon_type = %s"
        params.append(hackathon_type)

    if status and status != 'All':
        sql += " AND h.status = %s"
        params.append(status)

    if search:
        sql += " AND (h.title LIKE %s OR h.theme LIKE %s OR h.organizer_name LIKE %s)"
        like_search = f"%{search}%"
        params.extend([like_search, like_search, like_search])

    sql += " ORDER BY h.registration_deadline ASC;"

    hackathons = query_all(sql, params)

    # If user is logged in, attach their registration status
    user_id = session.get('user_id')
    if user_id and hackathons:
        user_regs = query_all("""
            SELECT hackathon_id, status FROM hackathon_registrations WHERE user_id = %s;
        """, (user_id,))
        reg_map = {r['hackathon_id']: r['status'] for r in user_regs}

        for h in hackathons:
            h['user_registration_status'] = reg_map.get(h['hackathon_id'], None)

    return jsonify({'success': True, 'hackathons': hackathons})


@hackathons_bp.route('/<int:hackathon_id>', methods=['GET'])
def get_hackathon_detail(hackathon_id):
    """
    Fetches comprehensive hackathon detail including:
    - Event metadata & timeline
    - Evaluation criteria
    - Teams registered
    - User's registration and team status if logged in
    """
    hackathon = query_one("""
        SELECT 
            h.*, 
            COALESCE(c.college_name, 'External / National Platform') AS host_college,
            COALESCE(c.college_code, 'EXT') AS host_college_code
        FROM hackathons h
        LEFT JOIN colleges c ON h.college_id = c.college_id
        WHERE h.hackathon_id = %s;
    """, (hackathon_id,))

    if not hackathon:
        return jsonify({'success': False, 'message': 'Hackathon not found.'}), 404

    # Evaluation criteria
    criteria = query_all("""
        SELECT criteria_id, criteria_name, max_score, weight_pct
        FROM evaluation_criteria
        WHERE hackathon_id = %s;
    """, (hackathon_id,))
    hackathon['evaluation_criteria'] = criteria

    # Teams list
    teams = query_all("""
        SELECT t.team_id, t.team_name, u.full_name AS leader_name,
               COUNT(tm.team_member_id) AS member_count,
               p.project_id, p.title AS project_title, p.submission_status
        FROM teams t
        JOIN users u ON t.leader_user_id = u.user_id
        LEFT JOIN team_members tm ON t.team_id = tm.team_id
        LEFT JOIN projects p ON t.team_id = p.team_id
        WHERE t.hackathon_id = %s
        GROUP BY t.team_id, t.team_name, u.full_name, p.project_id, p.title, p.submission_status;
    """, (hackathon_id,))
    hackathon['teams'] = teams

    # Logged-in user context
    user_id = session.get('user_id')
    user_context = {'registered': False, 'registration_status': None, 'team': None}
    if user_id:
        reg = query_one("""
            SELECT status FROM hackathon_registrations 
            WHERE hackathon_id = %s AND user_id = %s;
        """, (hackathon_id, user_id))
        if reg:
            user_context['registered'] = True
            user_context['registration_status'] = reg['status']

        my_team = query_one("""
            SELECT t.team_id, t.team_name, t.invitation_code, tm.role_in_team
            FROM team_members tm
            JOIN teams t ON tm.team_id = t.team_id
            WHERE t.hackathon_id = %s AND tm.user_id = %s;
        """, (hackathon_id, user_id))
        user_context['team'] = my_team

    hackathon['user_context'] = user_context

    return jsonify({'success': True, 'hackathon': hackathon})


@hackathons_bp.route('/register', methods=['POST'])
@login_required
def register_for_hackathon():
    """
    Submits an application / registration for a hackathon.
    """
    user_id = session['user_id']
    data = request.get_json() or {}
    hackathon_id = data.get('hackathon_id')

    if not hackathon_id:
        return jsonify({'success': False, 'message': 'Hackathon ID is required.'}), 400

    # Check hackathon validity and deadline
    hackathon = query_one("""
        SELECT hackathon_id, title, status, registration_deadline 
        FROM hackathons 
        WHERE hackathon_id = %s;
    """, (hackathon_id,))

    if not hackathon:
        return jsonify({'success': False, 'message': 'Hackathon does not exist.'}), 404

    # Check if already registered
    existing = query_one("""
        SELECT registration_id, status FROM hackathon_registrations 
        WHERE hackathon_id = %s AND user_id = %s;
    """, (hackathon_id, user_id))

    if existing:
        return jsonify({
            'success': False, 
            'message': f'You have already registered for this hackathon (Status: {existing["status"]}).'
        }), 409

    # Insert registration
    reg_id, _ = execute_dml("""
        INSERT INTO hackathon_registrations (hackathon_id, user_id, status)
        VALUES (%s, %s, 'Approved');
    """, (hackathon_id, user_id))

    # Send confirmation notification
    execute_dml("""
        INSERT INTO notifications (user_id, title, message, link)
        VALUES (%s, %s, %s, %s);
    """, (
        user_id,
        'Registration Confirmed',
        f'You have successfully registered for "{hackathon["title"]}". Create or join a team to begin.',
        f'/hackathons/{hackathon_id}'
    ))

    return jsonify({
        'success': True,
        'message': f'Successfully registered for "{hackathon["title"]}"!',
        'registration_id': reg_id
    }), 201


@hackathons_bp.route('', methods=['POST'])
@login_required
@role_required('Admin', 'College Coordinator')
def create_hackathon():
    """
    Creates a new hackathon (Internal or External).
    Restricted to Admins and College Coordinators.
    """
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    theme = data.get('theme', '').strip()
    description = data.get('description', '').strip()
    hackathon_type = data.get('hackathon_type', 'Internal')
    mode = data.get('mode', 'Online')
    venue = data.get('venue', 'Campus / Virtual')
    organizer_name = data.get('organizer_name', '').strip()
    eligibility = data.get('eligibility', '').strip()
    external_url = data.get('external_url', '').strip()
    reg_deadline = data.get('registration_deadline')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    min_size = int(data.get('min_team_size', 1))
    max_size = int(data.get('max_team_size', 4))
    prize_pool = data.get('prize_pool', 'Certificates')
    college_id = data.get('college_id') or session.get('college_id')

    if not title or not theme or not description or not reg_deadline or not start_date or not end_date:
        return jsonify({'success': False, 'message': 'Please provide all mandatory hackathon fields.'}), 400

    if start_date > end_date:
        return jsonify({'success': False, 'message': 'End date must be greater than or equal to start date.'}), 400

    try:
        hackathon_id, _ = execute_dml("""
            INSERT INTO hackathons (
                college_id, title, theme, description, hackathon_type,
                mode, venue, organizer_name, eligibility, external_url,
                registration_deadline, start_date, end_date,
                min_team_size, max_team_size, prize_pool, status, created_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Open', %s);
        """, (
            college_id if hackathon_type == 'Internal' else None,
            title, theme, description, hackathon_type,
            mode, venue, organizer_name, eligibility,
            external_url if external_url else None,
            reg_deadline, start_date, end_date,
            min_size, max_size, prize_pool, session['user_id']
        ))

        # Seed standard evaluation criteria for the new hackathon
        criteria_list = [
            ('Innovation & Originality', 25.00),
            ('Feasibility & Practical Utility', 25.00),
            ('Technical Execution & DB Design', 25.00),
            ('UI/UX & Final Presentation', 25.00)
        ]
        for name, max_score in criteria_list:
            execute_dml("""
                INSERT INTO evaluation_criteria (hackathon_id, criteria_name, max_score, weight_pct)
                VALUES (%s, %s, %s, 25.00);
            """, (hackathon_id, name, max_score))

        return jsonify({
            'success': True,
            'message': f'Hackathon "{title}" created successfully!',
            'hackathon_id': hackathon_id
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error creating hackathon: {str(e)}'}), 500
