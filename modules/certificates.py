"""
InnoSphere Certificate Generation and Public Verification Module
Provides verifiable cryptographic codes and downloadable PDF certificates.
"""

import io
from flask import Blueprint, request, jsonify, session, send_file
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from modules.db import query_one, query_all, execute_dml, get_db
from modules.auth import login_required, role_required

certificates_bp = Blueprint('certificates', __name__, url_prefix='/api/certificates')


@certificates_bp.route('', methods=['GET'])
@login_required
def get_my_certificates():
    """Lists all certificates issued to the current user."""
    user_id = session['user_id']
    certs = query_all("""
        SELECT 
            c.certificate_id, c.certificate_code, c.certificate_type,
            c.issue_date, c.verified_count,
            h.title AS hackathon_title, h.hackathon_type,
            t.team_name,
            col.college_name
        FROM certificates c
        JOIN hackathons h ON c.hackathon_id = h.hackathon_id
        LEFT JOIN teams t ON c.team_id = t.team_id
        LEFT JOIN colleges col ON h.college_id = col.college_id
        WHERE c.user_id = %s
        ORDER BY c.issue_date DESC;
    """, (user_id,))

    return jsonify({'success': True, 'certificates': certs})


@certificates_bp.route('/verify/<string:certificate_code>', methods=['GET'])
def verify_certificate(certificate_code):
    """
    Public Verification API endpoint.
    Anyone can verify the authenticity of an InnoSphere certificate by code.
    Increments verified_count upon successful verification.
    """
    cert = query_one("""
        SELECT 
            c.certificate_id, c.certificate_code, c.certificate_type,
            c.issue_date, c.verified_count,
            u.full_name AS recipient_name, u.email AS recipient_email,
            h.title AS hackathon_title, h.theme, h.hackathon_type,
            h.start_date, h.end_date,
            t.team_name,
            COALESCE(col.college_name, 'InnoSphere Unified Innovation Council') AS issuing_institution
        FROM certificates c
        JOIN users u ON c.user_id = u.user_id
        JOIN hackathons h ON c.hackathon_id = h.hackathon_id
        LEFT JOIN teams t ON c.team_id = t.team_id
        LEFT JOIN colleges col ON h.college_id = col.college_id
        WHERE c.certificate_code = %s;
    """, (certificate_code.strip().upper(),))

    if not cert:
        return jsonify({
            'success': False, 
            'verified': False, 
            'message': 'Certificate code not found or invalid.'
        }), 404

    # Increment verification count
    execute_dml("""
        UPDATE certificates SET verified_count = verified_count + 1 WHERE certificate_id = %s;
    """, (cert['certificate_id'],))

    cert['verified_count'] += 1
    cert['verified'] = True

    return jsonify({'success': True, 'verified': True, 'certificate': cert})


@certificates_bp.route('/issue', methods=['POST'])
@login_required
@role_required('Admin', 'College Coordinator')
def issue_certificate():
    """
    Issues a certificate using Stored Procedure sp_issue_certificate.
    """
    data = request.get_json() or {}
    user_id = data.get('user_id')
    hackathon_id = data.get('hackathon_id')
    team_id = data.get('team_id')
    cert_type = data.get('certificate_type', 'Participation')

    if not user_id or not hackathon_id:
        return jsonify({'success': False, 'message': 'User ID and Hackathon ID are required.'}), 400

    with get_db(commit=True) as (cursor, conn):
        try:
            cursor.callproc('sp_issue_certificate', [
                int(user_id),
                int(hackathon_id),
                int(team_id) if team_id else None,
                cert_type,
                '',  # OUT p_out_code
                ''   # OUT p_status_message
            ])

            # Query certificate by user and hackathon
            cursor.execute("""
                SELECT certificate_code, certificate_type, issue_date
                FROM certificates 
                WHERE user_id = %s AND hackathon_id = %s AND certificate_type = %s;
            """, (user_id, hackathon_id, cert_type))
            cert = cursor.fetchone()

            return jsonify({
                'success': True,
                'message': f'Certificate issued successfully!',
                'certificate_code': cert['certificate_code'] if cert else 'ISSUED'
            }), 201

        except Exception as e:
            return jsonify({'success': False, 'message': f'Certificate issue error: {str(e)}'}), 400


@certificates_bp.route('/download/<string:certificate_code>', methods=['GET'])
def download_pdf_certificate(certificate_code):
    """
    Generates and serves a publication-grade PDF certificate on the fly.
    """
    cert = query_one("""
        SELECT 
            c.certificate_code, c.certificate_type, c.issue_date,
            u.full_name AS recipient_name,
            h.title AS hackathon_title, h.theme,
            t.team_name,
            COALESCE(col.college_name, 'InnoSphere Unified Innovation Council') AS college_name
        FROM certificates c
        JOIN users u ON c.user_id = u.user_id
        JOIN hackathons h ON c.hackathon_id = h.hackathon_id
        LEFT JOIN teams t ON c.team_id = t.team_id
        LEFT JOIN colleges col ON h.college_id = col.college_id
        WHERE c.certificate_code = %s;
    """, (certificate_code.strip().upper(),))

    if not cert:
        return jsonify({'success': False, 'message': 'Certificate not found.'}), 404

    # Build PDF in memory using ReportLab
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Decorative Borders
    p.setStrokeColor(colors.HexColor('#0f2b5c'))
    p.setLineWidth(6)
    p.rect(20, 20, width - 40, height - 40)

    p.setStrokeColor(colors.HexColor('#d97706'))
    p.setLineWidth(2)
    p.rect(28, 28, width - 56, height - 56)

    # Header
    p.setFont("Helvetica-Bold", 18)
    p.setFillColor(colors.HexColor('#0f2b5c'))
    p.drawCentredString(width / 2.0, height - 70, "INNOSPHERE INNOVATION & RESEARCH PORTAL")

    p.setFont("Helvetica", 11)
    p.setFillColor(colors.HexColor('#475569'))
    p.drawCentredString(width / 2.0, height - 90, f"Affiliated with {cert['college_name']}")

    # Title
    p.setFont("Helvetica-Bold", 30)
    p.setFillColor(colors.HexColor('#1e3a8a'))
    p.drawCentredString(width / 2.0, height - 140, "CERTIFICATE OF ACHIEVEMENT")

    # Type Banner
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.HexColor('#d97706'))
    p.drawCentredString(width / 2.0, height - 165, f"— {cert['certificate_type'].upper()} —")

    # Presentation text
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.HexColor('#334155'))
    p.drawCentredString(width / 2.0, height - 210, "This is proudly presented to")

    # Recipient Name
    p.setFont("Helvetica-Bold", 26)
    p.setFillColor(colors.HexColor('#0f2b5c'))
    p.drawCentredString(width / 2.0, height - 250, cert['recipient_name'])

    # Detail text
    team_str = f" as a valued member of Team {cert['team_name']}" if cert['team_name'] else ""
    desc_text = f"for exemplary performance and innovation{team_str} in the hackathon:"
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.HexColor('#334155'))
    p.drawCentredString(width / 2.0, height - 290, desc_text)

    # Hackathon Title
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.HexColor('#059669'))
    p.drawCentredString(width / 2.0, height - 320, f'"{cert["hackathon_title"]}"')

    # Date and Verification Code
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.HexColor('#64748b'))
    p.drawString(50, 60, f"Issued Date: {cert['issue_date']}")
    p.drawRightString(width - 50, 60, f"Verification Code: {cert['certificate_code']}")

    # Signatures line
    p.setLineWidth(1)
    p.setStrokeColor(colors.HexColor('#94a3b8'))
    p.line(100, 110, 260, 110)
    p.line(width - 260, 110, width - 100, 110)

    p.setFont("Helvetica", 10)
    p.setFillColor(colors.HexColor('#475569'))
    p.drawCentredString(180, 95, "Authorized Signatory")
    p.drawCentredString(width - 180, 95, "Convener / Principal")

    p.showPage()
    p.save()

    buffer.seek(0)
    filename = f"InnoSphere_Certificate_{cert['certificate_code']}.pdf"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )
