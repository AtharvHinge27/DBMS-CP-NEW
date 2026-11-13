"""
InnoSphere – Unified Innovation, Hackathon & Research Management Portal
Main Flask Application Entry Point
Architecture: Modular Blueprints, MySQL Connector, REST APIs & Fetch UI
"""

import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from config import Config

# Import Blueprints
from modules.auth import auth_bp
from modules.participants import participants_bp
from modules.hackathons import hackathons_bp
from modules.teams import teams_bp
from modules.evaluations import evaluations_bp
from modules.certificates import certificates_bp
from modules.admin import admin_bp
from modules.notifications import notifications_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(participants_bp)
app.register_blueprint(hackathons_bp)
app.register_blueprint(teams_bp)
app.register_blueprint(evaluations_bp)
app.register_blueprint(certificates_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(notifications_bp)


# -----------------------------------------------------------------------------
# Global Template Context Processor
# -----------------------------------------------------------------------------
@app.context_processor
def inject_global_data():
    """Provides current user session data and system metadata to all Jinja2 templates."""
    return {
        'current_user': {
            'user_id': session.get('user_id'),
            'full_name': session.get('full_name'),
            'email': session.get('email'),
            'role': session.get('role'),
            'college_id': session.get('college_id'),
            'college_name': session.get('college_name')
        },
        'is_authenticated': 'user_id' in session,
        'app_name': 'InnoSphere',
        'portal_tagline': 'Unified Innovation, Hackathon & Research Management Portal'
    }


# -----------------------------------------------------------------------------
# Frontend HTML Routes
# -----------------------------------------------------------------------------
@app.route('/')
def home_page():
    """Public Landing Page."""
    return render_template('index.html')


@app.route('/login')
def login_page():
    """User Login Page."""
    if 'user_id' in session:
        return redirect(url_for('dashboard_page'))
    return render_template('login.html')


@app.route('/register')
def register_page():
    """User Registration Page."""
    if 'user_id' in session:
        return redirect(url_for('dashboard_page'))
    return render_template('register.html')


@app.route('/dashboard')
def dashboard_page():
    """Role-adaptive dashboard page."""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html')


@app.route('/profile')
def profile_page():
    """Student / Participant Profile Management Page."""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('profile.html')


@app.route('/hackathons')
def hackathons_page():
    """Hackathon Discovery and Opportunity Hub."""
    return render_template('hackathons.html')


@app.route('/hackathons/<int:hackathon_id>')
def hackathon_detail_page(hackathon_id):
    """Detailed view for a specific hackathon."""
    return render_template('hackathon_detail.html', hackathon_id=hackathon_id)


@app.route('/teams')
def teams_page():
    """Team Workspace and Project Submission Page."""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('teams.html')


@app.route('/evaluations')
def evaluations_page():
    """Judge Evaluation Rubric and Project Scoring Page."""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('evaluations.html')


@app.route('/leaderboard')
def leaderboard_page():
    """Real-Time Hackathon Project Leaderboard."""
    return render_template('leaderboard.html')


@app.route('/certificates')
def certificates_page():
    """My Certificates and Download Portal."""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('certificates.html')


@app.route('/verify-certificate')
def verify_certificate_page():
    """Public Certificate Verification Portal."""
    code = request.args.get('code', '')
    return render_template('verify_certificate.html', initial_code=code)


@app.route('/admin')
def admin_page():
    """Super Administrator Portal."""
    if 'user_id' not in session or session.get('role') != 'Admin':
        return redirect(url_for('dashboard_page'))
    return render_template('admin.html')


@app.route('/coordinator')
def coordinator_page():
    """College Coordinator Portal."""
    if 'user_id' not in session or session.get('role') not in ['College Coordinator', 'Admin']:
        return redirect(url_for('dashboard_page'))
    return render_template('coordinator.html')


# -----------------------------------------------------------------------------
# Error Handlers
# -----------------------------------------------------------------------------
@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'message': 'Resource or API route not found.'}), 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'message': 'Internal server error occurred.'}), 500
    return render_template('500.html'), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
