"""
InnoSphere Team and Project Management Module
Handles team creation, invitation codes, member management, and project submissions.
"""

import random
import string
from flask import Blueprint, request, jsonify, session
from modules.db import query_one, query_all, execute_dml, get_db
from modules.auth import login_required

teams_bp = Blueprint('teams', __name__, url_prefix='/api/teams')


def generate_invitation_code(team_name):
    """Generates a clean, unique 10-char uppercase invitation code."""
    prefix = ''.join(c for c in team_name if c.isalnum())[:4].upper()
    if len(prefix) < 3:
        prefix = "INNO"
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{prefix}-{suffix}"


@teams_bp.route('', methods=['GET'])
@login_required
def list_my_teams():
    """
    Returns all teams that the logged-in user belongs to or leads,
    along with project submission details.
    """
    user_id = session['user_id']
    teams = query_all("""
        SELECT 
            t.team_id, t.hackathon_id, t.team_name, t.invitation_code,
            t.leader_user_id, t.created_at,
            h.title AS hackathon_title, h.max_team_size, h.status AS hackathon_status,
            tm.role_in_team,
            (CASE WHEN t.leader_user_id = %s THEN TRUE ELSE FALSE END) AS is_leader,
            p.project_id, p.title AS project_title, p.submission_status,
            p.github_repo_url, p.documentation_url, p.demo_video_url,
            (SELECT COUNT(*) FROM team_members WHERE team_id = t.team_id) AS current_members_count
        FROM team_members tm
        JOIN teams t ON tm.team_id = t.team_id
        JOIN hackathons h ON t.hackathon_id = h.hackathon_id
        LEFT JOIN projects p ON t.team_id = p.team_id
        WHERE tm.user_id = %s
        ORDER BY t.created_at DESC;
    """, (user_id, user_id))

    return jsonify({'success': True, 'teams': teams})


@teams_bp.route('/<int:team_id>', methods=['GET'])
@login_required
def get_team_detail(team_id):
    """
    Returns full details of a specific team:
    - Team info, leader info, invitation code
    - Full list of team members with colleges and departments
    - Project submission details
    """
    team = query_one("""
        SELECT 
            t.team_id, t.hackathon_id, t.team_name, t.invitation_code,
            t.leader_user_id, t.created_at,
            u.full_name AS leader_name, u.email AS leader_email,
            h.title AS hackathon_title, h.max_team_size, h.min_team_size,
            h.status AS hackathon_status
        FROM teams t
        JOIN users u ON t.leader_user_id = u.user_id
        JOIN hackathons h ON t.hackathon_id = h.hackathon_id
        WHERE t.team_id = %s;
    """, (team_id,))

    if not team:
        return jsonify({'success': False, 'message': 'Team not found.'}), 404

    # Fetch team members
    members = query_all("""
        SELECT 
            tm.team_member_id, tm.user_id, tm.role_in_team, tm.joined_at,
            u.full_name, u.email,
            c.college_name, d.department_name,
            pp.roll_number, pp.branch, pp.year_of_study, pp.technical_skills
        FROM team_members tm
        JOIN users u ON tm.user_id = u.user_id
        LEFT JOIN colleges c ON u.college_id = c.college_id
        LEFT JOIN participant_profiles pp ON u.user_id = pp.user_id
        LEFT JOIN departments d ON pp.department_id = d.department_id
        WHERE tm.team_id = %s
        ORDER BY tm.joined_at ASC;
    """, (team_id,))

    # Fetch project details
    project = query_one("""
        SELECT 
            p.*,
            (SELECT COUNT(*) FROM evaluations e WHERE e.project_id = p.project_id) AS evaluation_count,
            (SELECT ROUND(AVG(e.total_score), 2) FROM evaluations e WHERE e.project_id = p.project_id) AS avg_score
        FROM projects p
        WHERE p.team_id = %s;
    """, (team_id,))

    # User membership status
    user_id = session['user_id']
    is_member = any(m['user_id'] == user_id for m in members)
    is_leader = (team['leader_user_id'] == user_id)

    return jsonify({
        'success': True,
        'team': team,
        'members': members,
        'project': project,
        'user_status': {
            'is_member': is_member,
            'is_leader': is_leader
        }
    })


@teams_bp.route('/create', methods=['POST'])
@login_required
def create_team():
    """
    Creates a new team using Stored Procedure sp_create_team_with_leader.
    Demonstrates ACID transactions:
    - Inserts team
    - Inserts leader into team_members
    - Auto-registers for hackathon
    - Emits notifications & audit logs
    """
    user_id = session['user_id']
    data = request.get_json() or {}
    hackathon_id = data.get('hackathon_id')
    team_name = data.get('team_name', '').strip()

    if not hackathon_id or not team_name:
        return jsonify({'success': False, 'message': 'Hackathon and team name are required.'}), 400

    invitation_code = generate_invitation_code(team_name)

    # Call Stored Procedure sp_create_team_with_leader
    with get_db(commit=True) as (cursor, conn):
        try:
            cursor.callproc('sp_create_team_with_leader', [
                int(hackathon_id),
                team_name,
                invitation_code,
                user_id,
                0,  # OUT p_out_team_id
                ''  # OUT p_status_message
            ])

            # Retrieve OUT parameter from the created team directly
            cursor.execute("SELECT team_id FROM teams WHERE invitation_code = %s;", (invitation_code,))
            created_team = cursor.fetchone()

            if not created_team:
                return jsonify({'success': False, 'message': 'Team creation failed or you are already in a team for this hackathon.'}), 400

            new_team_id = created_team['team_id']

            return jsonify({
                'success': True,
                'message': f'Team "{team_name}" created successfully!',
                'team_id': new_team_id,
                'invitation_code': invitation_code
            }), 201

        except Exception as e:
            return jsonify({'success': False, 'message': f'Database procedure error: {str(e)}'}), 400


@teams_bp.route('/join', methods=['POST'])
@login_required
def join_team():
    """
    Joins a team using invitation code and Stored Procedure sp_join_team_by_code.
    """
    user_id = session['user_id']
    data = request.get_json() or {}
    invitation_code = data.get('invitation_code', '').strip().upper()
    role_in_team = data.get('role_in_team', 'Member').strip()

    if not invitation_code:
        return jsonify({'success': False, 'message': 'Please provide a valid invitation code.'}), 400

    with get_db(commit=True) as (cursor, conn):
        try:
            cursor.callproc('sp_join_team_by_code', [
                invitation_code,
                user_id,
                role_in_team,
                0,
                ''
            ])

            # Check if user was added to team_members
            cursor.execute("""
                SELECT tm.team_id, t.team_name 
                FROM team_members tm
                JOIN teams t ON tm.team_id = t.team_id
                WHERE t.invitation_code = %s AND tm.user_id = %s;
            """, (invitation_code, user_id))
            membership = cursor.fetchone()

            if not membership:
                return jsonify({
                    'success': False, 
                    'message': 'Failed to join team. The code may be invalid, the team is full, or you are already registered in this hackathon.'
                }), 400

            return jsonify({
                'success': True,
                'message': f'Successfully joined team "{membership["team_name"]}"!',
                'team_id': membership['team_id']
            })

        except Exception as e:
            return jsonify({'success': False, 'message': f'Procedure error: {str(e)}'}), 400


@teams_bp.route('/<int:team_id>/project', methods=['POST', 'PUT'])
@login_required
def submit_project(team_id):
    """
    Submits or updates a team's project submission.
    Only the team leader or an active member can submit.
    """
    user_id = session['user_id']
    data = request.get_json() or {}

    title = data.get('title', '').strip()
    abstract = data.get('abstract', '').strip()
    tech_stack = data.get('tech_stack', '').strip()
    github_repo_url = data.get('github_repo_url', '').strip()
    documentation_url = data.get('documentation_url', '').strip()
    demo_video_url = data.get('demo_video_url', '').strip()

    if not title or not abstract:
        return jsonify({'success': False, 'message': 'Project title and abstract are required.'}), 400

    # Verify user is a member of this team
    membership = query_one("""
        SELECT tm.role_in_team, t.hackathon_id 
        FROM team_members tm
        JOIN teams t ON tm.team_id = t.team_id
        WHERE tm.team_id = %s AND tm.user_id = %s;
    """, (team_id, user_id))

    if not membership:
        return jsonify({'success': False, 'message': 'Unauthorized. You are not a member of this team.'}), 403

    hackathon_id = membership['hackathon_id']

    # Check if project already exists for this team
    existing_project = query_one("SELECT project_id FROM projects WHERE team_id = %s;", (team_id,))

    if existing_project:
        # Update existing project
        execute_dml("""
            UPDATE projects SET
                title = %s,
                abstract = %s,
                tech_stack = %s,
                github_repo_url = %s,
                documentation_url = %s,
                demo_video_url = %s,
                submission_status = 'Submitted',
                submitted_at = NOW()
            WHERE team_id = %s;
        """, (title, abstract, tech_stack, github_repo_url, documentation_url, demo_video_url, team_id))

        return jsonify({'success': True, 'message': 'Project submission updated successfully!'})
    else:
        # Insert new project submission
        # Trigger trg_after_project_insert will notify team members and log audit trail
        project_id, _ = execute_dml("""
            INSERT INTO projects (
                team_id, hackathon_id, title, abstract,
                tech_stack, github_repo_url, documentation_url,
                demo_video_url, submission_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Submitted');
        """, (team_id, hackathon_id, title, abstract, tech_stack, github_repo_url, documentation_url, demo_video_url))

        return jsonify({
            'success': True,
            'message': 'Project submitted successfully!',
            'project_id': project_id
        }), 201


@teams_bp.route('/my-projects', methods=['GET'])
@login_required
def get_my_projects():
    """
    Fetches all projects associated with teams the current user belongs to,
    including submission links, progress, evaluation scores, and judge feedback.
    """
    user_id = session['user_id']
    projects = query_all("""
        SELECT 
            p.project_id, p.team_id, p.hackathon_id, p.title AS project_title,
            p.abstract, p.tech_stack, p.github_repo_url, p.documentation_url,
            p.demo_video_url, p.submission_status, p.submitted_at,
            t.team_name, t.invitation_code, t.leader_user_id,
            u.full_name AS leader_name,
            h.title AS hackathon_title, h.theme AS hackathon_theme,
            h.status AS hackathon_status,
            (CASE WHEN t.leader_user_id = %s THEN TRUE ELSE FALSE END) AS is_leader,
            (SELECT COUNT(*) FROM evaluations e WHERE e.project_id = p.project_id) AS evaluation_count,
            (SELECT ROUND(AVG(e.total_score), 2) FROM evaluations e WHERE e.project_id = p.project_id) AS avg_score
        FROM projects p
        JOIN teams t ON p.team_id = t.team_id
        JOIN team_members tm ON t.team_id = tm.team_id
        JOIN users u ON t.leader_user_id = u.user_id
        JOIN hackathons h ON p.hackathon_id = h.hackathon_id
        WHERE tm.user_id = %s
        ORDER BY p.submitted_at DESC;
    """, (user_id, user_id))

    # Fetch individual evaluation rubrics for each project
    for proj in projects:
        evals = query_all("""
            SELECT e.evaluation_id, e.total_score, e.innovation_score,
                   e.feasibility_score, e.technical_score, e.presentation_score,
                   e.feedback, e.evaluated_at, u.full_name AS judge_name
            FROM evaluations e
            JOIN users u ON e.judge_user_id = u.user_id
            WHERE e.project_id = %s;
        """, (proj['project_id'],))
        proj['evaluations_list'] = evals

    return jsonify({'success': True, 'projects': projects})

