"""
InnoSphere Authentication & Authorization Module
Handles login, registration, role-based session management, and decorators.
"""

from functools import wraps
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from modules.db import query_one, execute_dml, get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def login_required(f):
    """Decorator to protect routes requiring authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Authentication required. Please log in.'}), 401
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """Decorator to enforce role-based access control."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'success': False, 'message': 'Authentication required.'}), 401
            user_role = session.get('role')
            if user_role not in allowed_roles:
                return jsonify({
                    'success': False, 
                    'message': f'Access denied. Required role: {", ".join(allowed_roles)}. Your role: {user_role}'
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user account.
    Trigger trg_after_user_insert automatically creates participant profile if role is Participant.
    """
    data = request.get_json() or {}
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    role = data.get('role', 'Participant').strip()
    college_id = data.get('college_id')

    # Basic validations
    if not full_name or not email or not password:
        return jsonify({'success': False, 'message': 'Full name, email, and password are required.'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters long.'}), 400

    valid_roles = ['Admin', 'College Coordinator', 'Participant', 'Mentor', 'Judge']
    if role not in valid_roles:
        return jsonify({'success': False, 'message': f'Invalid role. Allowed roles: {", ".join(valid_roles)}'}), 400

    # Check for existing email
    existing_user = query_one("SELECT user_id FROM users WHERE email = %s;", (email,))
    if existing_user:
        return jsonify({'success': False, 'message': 'An account with this email address already exists.'}), 409

    # Hash password securely
    hashed_password = generate_password_hash(password)

    try:
        user_id, _ = execute_dml("""
            INSERT INTO users (college_id, full_name, email, password_hash, role)
            VALUES (%s, %s, %s, %s, %s);
        """, (college_id if college_id else None, full_name, email, hashed_password, role))

        # Automatically log user in
        session['user_id'] = user_id
        session['full_name'] = full_name
        session['email'] = email
        session['role'] = role
        session['college_id'] = college_id

        # Determine dashboard redirect
        redirect_url = '/dashboard'

        return jsonify({
            'success': True,
            'message': 'Account registered successfully!',
            'user': {
                'user_id': user_id,
                'full_name': full_name,
                'email': email,
                'role': role,
                'college_id': college_id
            },
            'redirect': redirect_url
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'message': f'Database error during registration: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user and starts a session.
    """
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required.'}), 400

    user = query_one("""
        SELECT u.user_id, u.college_id, u.full_name, u.email, u.password_hash, u.role, u.is_active,
               c.college_name
        FROM users u
        LEFT JOIN colleges c ON u.college_id = c.college_id
        WHERE u.email = %s;
    """, (email,))

    if not user:
        return jsonify({'success': False, 'message': 'Invalid email or password.'}), 401

    if not user['is_active']:
        return jsonify({'success': False, 'message': 'Your account has been deactivated. Contact the administrator.'}), 403

    if not check_password_hash(user['password_hash'], password):
        return jsonify({'success': False, 'message': 'Invalid email or password.'}), 401

    # Establish session
    session['user_id'] = user['user_id']
    session['full_name'] = user['full_name']
    session['email'] = user['email']
    session['role'] = user['role']
    session['college_id'] = user['college_id']
    session['college_name'] = user['college_name']

    return jsonify({
        'success': True,
        'message': f'Welcome back, {user["full_name"]}!',
        'user': {
            'user_id': user['user_id'],
            'full_name': user['full_name'],
            'email': user['email'],
            'role': user['role'],
            'college_id': user['college_id'],
            'college_name': user['college_name']
        },
        'redirect': '/dashboard'
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Clears current user session."""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully.', 'redirect': '/login'})


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Returns the authenticated user's profile and notifications count."""
    if 'user_id' not in session:
        return jsonify({'success': False, 'authenticated': False}), 200

    user_id = session['user_id']
    user = query_one("""
        SELECT u.user_id, u.college_id, u.full_name, u.email, u.role, u.is_active,
               c.college_name, c.college_code
        FROM users u
        LEFT JOIN colleges c ON u.college_id = c.college_id
        WHERE u.user_id = %s;
    """, (user_id,))

    if not user:
        session.clear()
        return jsonify({'success': False, 'authenticated': False}), 200

    # Unread notifications count
    notif_stat = query_one("""
        SELECT COUNT(*) AS unread_count 
        FROM notifications 
        WHERE user_id = %s AND is_read = FALSE;
    """, (user_id,))

    user['unread_notifications'] = notif_stat['unread_count'] if notif_stat else 0
    user['authenticated'] = True

    return jsonify({'success': True, 'authenticated': True, 'user': user})
