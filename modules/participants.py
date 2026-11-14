"""
InnoSphere Participant Management Module
Handles student profile lifecycle, academic info, skills, and participation history.
"""

from flask import Blueprint, request, jsonify, session
from modules.db import query_one, query_all, execute_dml, get_db
from modules.auth import login_required

participants_bp = Blueprint('participants', __name__, url_prefix='/api/participants')


@participants_bp.route('/profile', methods=['GET'])
@login_required
def get_my_profile():
    """
    Fetches the profile for the current logged-in participant.
    Uses vw_participant_summary view and calls stored function fn_calculate_profile_completion.
    """
    user_id = session['user_id']
    profile = query_one("""
        SELECT * FROM vw_participant_summary WHERE user_id = %s;
    """, (user_id,))

    if not profile:
        # Fallback to query users table if profile view is empty (e.g. if non-participant)
        user = query_one("SELECT user_id, full_name, email, role, college_id FROM users WHERE user_id = %s;", (user_id,))
        return jsonify({'success': True, 'profile': user, 'is_participant': False})

    # Call stored function to ensure real-time dynamic completion calculation
    comp_calc = query_one("SELECT fn_calculate_profile_completion(%s) AS dynamic_completion;", (user_id,))
    if comp_calc:
        profile['profile_completion_pct'] = comp_calc['dynamic_completion']

    return jsonify({'success': True, 'profile': profile, 'is_participant': True})


@participants_bp.route('/profile/<int:target_user_id>', methods=['GET'])
def get_public_profile(target_user_id):
    """Fetches public profile of a participant by user_id."""
    profile = query_one("""
        SELECT 
            u.user_id, u.full_name, u.role,
            c.college_name, d.department_name,
            pp.roll_number, pp.branch, pp.year_of_study, pp.semester,
            pp.technical_skills, pp.interests, pp.github_url, pp.linkedin_url,
            pp.portfolio_url, pp.bio, pp.profile_completion_pct
        FROM users u
        LEFT JOIN colleges c ON u.college_id = c.college_id
        LEFT JOIN participant_profiles pp ON u.user_id = pp.user_id
        LEFT JOIN departments d ON pp.department_id = d.department_id
        WHERE u.user_id = %s AND u.role = 'Participant';
    """, (target_user_id,))

    if not profile:
        return jsonify({'success': False, 'message': 'Participant profile not found.'}), 404

    # Fetch achievements / certificates
    certs = query_all("""
        SELECT cert.certificate_code, cert.certificate_type, cert.issue_date,
               h.title AS hackathon_title
        FROM certificates cert
        JOIN hackathons h ON cert.hackathon_id = h.hackathon_id
        WHERE cert.user_id = %s;
    """, (target_user_id,))
    profile['certificates'] = certs

    return jsonify({'success': True, 'profile': profile})


@participants_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """
    Updates the participant profile and automatically recalculates completion percentage.
    """
    user_id = session['user_id']
    data = request.get_json() or {}

    roll_number = data.get('roll_number', '').strip()
    department_id = data.get('department_id')
    branch = data.get('branch', '').strip()
    year_of_study = data.get('year_of_study')
    semester = data.get('semester')
    phone_number = data.get('phone_number', '').strip()
    technical_skills = data.get('technical_skills', '').strip()
    interests = data.get('interests', '').strip()
    github_url = data.get('github_url', '').strip()
    linkedin_url = data.get('linkedin_url', '').strip()
    portfolio_url = data.get('portfolio_url', '').strip()
    bio = data.get('bio', '').strip()

    # Ensure profile row exists
    existing = query_one("SELECT profile_id FROM participant_profiles WHERE user_id = %s;", (user_id,))
    if not existing:
        execute_dml("INSERT INTO participant_profiles (user_id) VALUES (%s);", (user_id,))

    # Update profile fields
    execute_dml("""
        UPDATE participant_profiles SET
            roll_number = %s,
            department_id = %s,
            branch = %s,
            year_of_study = %s,
            semester = %s,
            phone_number = %s,
            technical_skills = %s,
            interests = %s,
            github_url = %s,
            linkedin_url = %s,
            portfolio_url = %s,
            bio = %s
        WHERE user_id = %s;
    """, (
        roll_number or None,
        department_id if department_id else None,
        branch or None,
        int(year_of_study) if year_of_study else None,
        int(semester) if semester else None,
        phone_number or None,
        technical_skills or None,
        interests or None,
        github_url or None,
        linkedin_url or None,
        portfolio_url or None,
        bio or None,
        user_id
    ))

    # Calculate new completion percentage using Stored Function fn_calculate_profile_completion
    comp_row = query_one("SELECT fn_calculate_profile_completion(%s) AS new_pct;", (user_id,))
    new_pct = comp_row['new_pct'] if comp_row else 50

    # Persist the calculated percentage
    execute_dml("UPDATE participant_profiles SET profile_completion_pct = %s WHERE user_id = %s;", (new_pct, user_id))

    return jsonify({
        'success': True,
        'message': 'Profile updated successfully!',
        'profile_completion_pct': new_pct
    })


@participants_bp.route('/history', methods=['GET'])
@login_required
def get_participation_history():
    """
    Fetches full participation history:
    - Registered hackathons & status
    - Teams joined and roles
    - Project submissions
    - Certificates won
    """
    user_id = session['user_id']

    # Registered Hackathons
    registrations = query_all("""
        SELECT hr.registration_id, hr.status AS registration_status, hr.registered_at,
               h.hackathon_id, h.title AS hackathon_title, h.hackathon_type,
               h.start_date, h.end_date, h.status AS hackathon_status,
               COALESCE(c.college_name, 'National / External') AS college_name
        FROM hackathon_registrations hr
        JOIN hackathons h ON hr.hackathon_id = h.hackathon_id
        LEFT JOIN colleges c ON h.college_id = c.college_id
        WHERE hr.user_id = %s
        ORDER BY hr.registered_at DESC;
    """, (user_id,))

    # Teams Joined
    teams = query_all("""
        SELECT t.team_id, t.team_name, t.invitation_code, tm.role_in_team, tm.joined_at,
               h.hackathon_id, h.title AS hackathon_title,
               p.project_id, p.title AS project_title, p.submission_status
        FROM team_members tm
        JOIN teams t ON tm.team_id = t.team_id
        JOIN hackathons h ON t.hackathon_id = h.hackathon_id
        LEFT JOIN projects p ON t.team_id = p.team_id
        WHERE tm.user_id = %s
        ORDER BY tm.joined_at DESC;
    """, (user_id,))

    # Certificates Earned
    certificates = query_all("""
        SELECT cert.certificate_id, cert.certificate_code, cert.certificate_type,
               cert.issue_date, cert.verified_count,
               h.title AS hackathon_title, t.team_name
        FROM certificates cert
        JOIN hackathons h ON cert.hackathon_id = h.hackathon_id
        LEFT JOIN teams t ON cert.team_id = t.team_id
        WHERE cert.user_id = %s
        ORDER BY cert.issue_date DESC;
    """, (user_id,))

    return jsonify({
        'success': True,
        'registrations': registrations,
        'teams': teams,
        'certificates': certificates
    })


@participants_bp.route('/applications', methods=['GET'])
@login_required
def get_my_applications():
    """
    Fetches full list of hackathon applications and approval status for current user.
    """
    user_id = session['user_id']
    status_filter = request.args.get('status')

    sql = """
        SELECT 
            hr.registration_id, hr.status AS application_status, hr.registered_at,
            h.hackathon_id, h.title AS hackathon_title, h.theme, h.hackathon_type,
            h.mode, h.venue, h.registration_deadline, h.start_date, h.end_date,
            h.prize_pool, h.status AS hackathon_status, h.external_url,
            COALESCE(c.college_name, 'National / External Opportunity') AS host_college,
            t.team_id, t.team_name, t.invitation_code, tm.role_in_team
        FROM hackathon_registrations hr
        JOIN hackathons h ON hr.hackathon_id = h.hackathon_id
        LEFT JOIN colleges c ON h.college_id = c.college_id
        LEFT JOIN team_members tm ON tm.user_id = hr.user_id
        LEFT JOIN teams t ON tm.team_id = t.team_id AND t.hackathon_id = h.hackathon_id
        WHERE hr.user_id = %s
    """
    params = [user_id]
    if status_filter and status_filter != 'All':
        sql += " AND hr.status = %s"
        params.append(status_filter)

    sql += " ORDER BY hr.registered_at DESC;"
    applications = query_all(sql, params)

    return jsonify({'success': True, 'applications': applications})


@participants_bp.route('/applications/<int:reg_id>', methods=['DELETE'])
@login_required
def withdraw_application(reg_id):
    """Allows participant to withdraw an application if no active team is formed."""
    user_id = session['user_id']
    reg = query_one("""
        SELECT registration_id, hackathon_id 
        FROM hackathon_registrations 
        WHERE registration_id = %s AND user_id = %s;
    """, (reg_id, user_id))

    if not reg:
        return jsonify({'success': False, 'message': 'Application not found or unauthorized.'}), 404

    # Check if user has an active team in this hackathon
    team = query_one("""
        SELECT tm.team_member_id FROM team_members tm
        JOIN teams t ON tm.team_id = t.team_id
        WHERE t.hackathon_id = %s AND tm.user_id = %s;
    """, (reg['hackathon_id'], user_id))
    if team:
        return jsonify({
            'success': False, 
            'message': 'Cannot withdraw application while you are a member of an active team. Please leave or disband the team first.'
        }), 400

    execute_dml("DELETE FROM hackathon_registrations WHERE registration_id = %s;", (reg_id,))
    return jsonify({'success': True, 'message': 'Application withdrawn successfully.'})


@participants_bp.route('/mentors', methods=['GET'])
@login_required
def get_available_mentors():
    """Fetches list of registered faculty guides and mentors."""
    mentors = query_all("""
        SELECT u.user_id, u.full_name, u.email, u.role,
               COALESCE(c.college_name, 'Affiliated Institution Expert') AS college_name,
               COALESCE(c.city, 'Pune') AS city,
               COALESCE(pp.technical_skills, 'AI/ML, Web Systems, Cloud, Database Architecture') AS expertise,
               COALESCE(pp.bio, 'Experienced academician and hackathon jury mentor.') AS bio
        FROM users u
        LEFT JOIN colleges c ON u.college_id = c.college_id
        LEFT JOIN participant_profiles pp ON u.user_id = pp.user_id
        WHERE u.role = 'Mentor' AND u.is_active = TRUE
        ORDER BY u.full_name ASC;
    """)
    return jsonify({'success': True, 'mentors': mentors})


@participants_bp.route('/results', methods=['GET'])
@login_required
def get_participant_results():
    """Fetches performance scores, ranks, and certificates for the logged-in student."""
    user_id = session['user_id']
    results = query_all("""
        SELECT 
            p.project_id, p.title AS project_title, p.abstract, p.submission_status,
            t.team_id, t.team_name,
            h.hackathon_id, h.title AS hackathon_title, h.theme, h.status AS hackathon_status,
            COALESCE(ROUND(AVG(e.total_score), 2), 0) AS final_score,
            COUNT(e.evaluation_id) AS total_reviews,
            cert.certificate_code, cert.certificate_type, cert.issue_date
        FROM team_members tm
        JOIN teams t ON tm.team_id = t.team_id
        JOIN hackathons h ON t.hackathon_id = h.hackathon_id
        LEFT JOIN projects p ON t.team_id = p.team_id
        LEFT JOIN evaluations e ON p.project_id = e.project_id
        LEFT JOIN certificates cert ON cert.hackathon_id = h.hackathon_id AND cert.user_id = %s
        WHERE tm.user_id = %s
        GROUP BY p.project_id, t.team_id, h.hackathon_id, cert.certificate_id
        ORDER BY h.start_date DESC;
    """, (user_id, user_id))
    return jsonify({'success': True, 'results': results})


