"""app/api/messages.py — Contact messages API"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app import db, limiter
from app.models import Message
from app.utils.rbac import roles_required
from app.utils.turnstile import verify_turnstile
from app.utils.validators import validate_email
from app.services.mail_service import send_contact_notification

messages_bp = Blueprint('messages', __name__)

def _ip(): return request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

@messages_bp.route('/', methods=['POST'])
@limiter.limit('5 per hour')
def send_message():
    d = request.get_json(silent=True) or {}
    if current_app.config.get('CF_TURNSTILE_SECRET') and not verify_turnstile(d.get('cf_turnstile_token',''), _ip()):
        return jsonify({'error': 'Verification failed'}), 400

    name = (d.get('name') or '').strip()[:120]
    email = (d.get('email') or '').strip().lower()[:255]
    body  = (d.get('message') or d.get('body') or '').strip()
    phone = (d.get('phone') or '').strip()[:50]

    if not name or not email or not body:
        return jsonify({'error': 'Name, email and message are required'}), 422
    if not validate_email(email):
        return jsonify({'error': 'Invalid email'}), 422

    m = Message(name=name, email=email, body=body, phone=phone,
                subject=d.get('subject','Contact from portfolio')[:300],
                ip_address=_ip())
    db.session.add(m); db.session.commit()
    try:
        send_contact_notification(m)
    except Exception:
        current_app.logger.exception('Failed to send contact notification for message id=%s', m.id)
    return jsonify({'message': 'Message sent successfully'}), 201

@messages_bp.route('/', methods=['GET'])
@jwt_required()
@roles_required('admin','super_admin')
def list_messages():
    status = request.args.get('status')
    page   = int(request.args.get('page',1))
    q = Message.query.filter_by(is_spam=False)
    if status: q = q.filter_by(status=status)
    pag = q.order_by(Message.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return jsonify({'items': [m.to_dict() for m in pag.items], 'total': pag.total, 'pages': pag.pages}), 200

@messages_bp.route('/<int:mid>', methods=['PATCH'])
@jwt_required()
@roles_required('admin','super_admin')
def update_message_status(mid):
    m = Message.query.get_or_404(mid)
    d = request.get_json(silent=True) or {}
    if 'status' in d: m.status = d['status']
    if 'is_spam' in d: m.is_spam = d['is_spam']
    db.session.commit()
    return jsonify(m.to_dict()), 200
