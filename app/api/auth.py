"""
app/api/auth.py
Authentication — JWT, 2FA TOTP, refresh tokens, recovery codes
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from datetime import datetime
import pyotp, secrets, hashlib, json

from app import db, limiter
from app.models import User, RefreshToken
from app.utils.validators import validate_email, validate_password
from app.utils.audit import log_action
from app.utils.turnstile import verify_turnstile

auth_bp = Blueprint('auth', __name__)

def _ip():  return request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
def _ua():  return request.headers.get('User-Agent', '')[:512]

def _issue_tokens(user):
    access  = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    refresh = create_refresh_token(identity=str(user.id))
    jti = secrets.token_hex(32)
    rt  = RefreshToken(user_id=user.id, jti=jti, device=_ua()[:200], ip_address=_ip(),
                       expires_at=datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'])
    db.session.add(rt); db.session.commit()
    return access, refresh

@auth_bp.route('/register', methods=['POST'])
@limiter.limit('10 per hour')
def register():
    d = request.get_json(silent=True) or {}
    name, email, pw = d.get('name','').strip(), d.get('email','').strip().lower(), d.get('password','')
    if current_app.config.get('CF_TURNSTILE_SECRET') and not verify_turnstile(d.get('cf_turnstile_token',''), _ip()):
        return jsonify({'error': 'Turnstile failed'}), 400
    if len(name) < 2: return jsonify({'error': 'Name too short'}), 422
    if not validate_email(email): return jsonify({'error': 'Invalid email'}), 422
    err = validate_password(pw)
    if err: return jsonify({'error': err}), 422
    if User.query.filter_by(email=email).first(): return jsonify({'error': 'Email taken'}), 409
    u = User(name=name, email=email, role='viewer')
    u.set_password(pw); db.session.add(u); db.session.flush()
    log_action('user_registered', 'user', u.id, ip=_ip(), ua=_ua()); db.session.commit()
    a, r = _issue_tokens(u)
    return jsonify({'user': u.to_dict(include_private=True), 'access_token': a, 'refresh_token': r}), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit('5 per minute')
def login():
    d = request.get_json(silent=True) or {}
    email, pw, code = d.get('email','').strip().lower(), d.get('password',''), d.get('totp_code','')
    if current_app.config.get('CF_TURNSTILE_SECRET') and not verify_turnstile(d.get('cf_turnstile_token',''), _ip()):
        return jsonify({'error': 'Turnstile failed'}), 400
    u = User.query.filter_by(email=email, is_active=True).first()
    if not u or not u.check_password(pw):
        log_action('login_failed', 'user', None, ip=_ip(), ua=_ua(), extra={'email': email})
        return jsonify({'error': 'Invalid credentials'}), 401
    if u.totp_enabled:
        if not code: return jsonify({'requires_2fa': True}), 200
        if not pyotp.TOTP(u.totp_secret).verify(code, valid_window=1):
            if not _use_recovery(u, code):
                log_action('2fa_failed','user',u.id,ip=_ip(),ua=_ua())
                return jsonify({'error': 'Invalid 2FA code'}), 401
    u.last_login_at = datetime.utcnow(); u.last_login_ip = _ip()
    log_action('login_success','user',u.id,ip=_ip(),ua=_ua()); db.session.commit()
    a, r = _issue_tokens(u)
    return jsonify({'user': u.to_dict(include_private=True), 'access_token': a, 'refresh_token': r}), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    u = User.query.get_or_404(get_jwt_identity())
    if not u.is_active: return jsonify({'error': 'Account disabled'}), 403
    return jsonify({'access_token': create_access_token(identity=u.id, additional_claims={'role': u.role})}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def logout():
    jti = get_jwt().get('jti')
    rt  = RefreshToken.query.filter_by(jti=jti).first()
    if rt: rt.revoked = True; db.session.commit()
    log_action('logout','user',get_jwt_identity(),ip=_ip(),ua=_ua())
    return jsonify({'message': 'Logged out'}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    return jsonify(User.query.get_or_404(get_jwt_identity()).to_dict(include_private=True)), 200

@auth_bp.route('/2fa/setup', methods=['POST'])
@jwt_required()
def setup_2fa():
    u = User.query.get_or_404(get_jwt_identity())
    s = pyotp.random_base32(); u.totp_secret = s; db.session.commit()
    uri = pyotp.TOTP(s).provisioning_uri(name=u.email, issuer_name='Abubaker Portfolio')
    return jsonify({'secret': s, 'uri': uri}), 200

@auth_bp.route('/2fa/verify', methods=['POST'])
@jwt_required()
def verify_2fa():
    u = User.query.get_or_404(get_jwt_identity())
    code = (request.get_json(silent=True) or {}).get('code','')
    if not u.totp_secret: return jsonify({'error': '2FA not set up'}), 400
    if not pyotp.TOTP(u.totp_secret).verify(code, valid_window=1): return jsonify({'error': 'Invalid code'}), 400
    raw = [secrets.token_hex(8) for _ in range(10)]
    u.totp_enabled = True
    u.recovery_codes = json.dumps([hashlib.sha256(c.encode()).hexdigest() for c in raw])
    db.session.commit(); log_action('2fa_enabled','user',u.id,ip=_ip(),ua=_ua())
    return jsonify({'message': '2FA enabled', 'recovery_codes': raw}), 200

@auth_bp.route('/2fa/disable', methods=['POST'])
@jwt_required()
def disable_2fa():
    u = User.query.get_or_404(get_jwt_identity())
    if not u.check_password((request.get_json(silent=True) or {}).get('password','')): return jsonify({'error': 'Wrong password'}), 401
    u.totp_enabled = False; u.totp_secret = None; u.recovery_codes = None; db.session.commit()
    log_action('2fa_disabled','user',u.id,ip=_ip(),ua=_ua())
    return jsonify({'message': '2FA disabled'}), 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    u = User.query.get_or_404(get_jwt_identity())
    d = request.get_json(silent=True) or {}
    if not u.check_password(d.get('old_password','')): return jsonify({'error': 'Wrong password'}), 401
    err = validate_password(d.get('new_password',''))
    if err: return jsonify({'error': err}), 422
    u.set_password(d['new_password']); db.session.commit()
    log_action('password_changed','user',u.id,ip=_ip(),ua=_ua())
    return jsonify({'message': 'Password updated'}), 200

def _use_recovery(user, code):
    if not user.recovery_codes: return False
    codes = json.loads(user.recovery_codes)
    h = hashlib.sha256(code.encode()).hexdigest()
    if h in codes:
        codes.remove(h); user.recovery_codes = json.dumps(codes); db.session.commit(); return True
    return False
