"""
InnoSphere Notifications Module
Handles real-time system alerts, event reminders, and status notices.
"""

from flask import Blueprint, request, jsonify, session
from modules.db import query_one, query_all, execute_dml
from modules.auth import login_required

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')


@notifications_bp.route('', methods=['GET'])
@login_required
def get_user_notifications():
    """Fetches notifications for the authenticated user."""
    user_id = session['user_id']
    notifications = query_all("""
        SELECT notification_id, title, message, link, is_read, created_at
        FROM notifications
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 25;
    """, (user_id,))

    unread_count = sum(1 for n in notifications if not n['is_read'])

    return jsonify({
        'success': True,
        'notifications': notifications,
        'unread_count': unread_count
    })


@notifications_bp.route('/read-all', methods=['POST'])
@login_required
def mark_all_read():
    """Marks all notifications as read for current user."""
    user_id = session['user_id']
    execute_dml("UPDATE notifications SET is_read = TRUE WHERE user_id = %s;", (user_id,))
    return jsonify({'success': True, 'message': 'All notifications marked as read.'})


@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_single_read(notification_id):
    """Marks a single notification as read."""
    user_id = session['user_id']
    execute_dml("UPDATE notifications SET is_read = TRUE WHERE notification_id = %s AND user_id = %s;", (notification_id, user_id))
    return jsonify({'success': True, 'message': 'Notification marked as read.'})
