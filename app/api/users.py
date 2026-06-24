"""app/api/users.py — User management"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import User, AuditLog
from app.utils.rbac import roles_required
from app.utils.audit import log_action

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@jwt_required()
@roles_required('super_admin','admin')
def list_users():
    page = int(request.args.get('page',1))
    pag  = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return jsonify({'items': [u.to_dict(include_private=True) for u in pag.items], 'total': pag.total}), 200

@users_bp.route('/<int:uid>', methods=['GET'])
@jwt_required()
@roles_required('super_admin','admin')
def get_user(uid):
    return jsonify(User.query.get_or_404(uid).to_dict(include_private=True)), 200

@users_bp.route('/<int:uid>', methods=['PUT'])
@jwt_required()
@roles_required('super_admin')
def update_user(uid):
    u = User.query.get_or_404(uid)
    d = request.get_json(silent=True) or {}
    for f in ['name','role','is_active','is_verified','avatar_url']:
        if f in d: setattr(u, f, d[f])
    log_action('user_updated','user',uid)
    db.session.commit()
    return jsonify(u.to_dict(include_private=True)), 200

@users_bp.route('/<int:uid>', methods=['DELETE'])
@jwt_required()
@roles_required('super_admin')
def delete_user(uid):
    u = User.query.get_or_404(uid)
    log_action('user_deleted','user',uid)
    db.session.delete(u); db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

@users_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
@roles_required('super_admin','admin')
def audit_logs():
    page = int(request.args.get('page',1))
    pag  = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=30, error_out=False)
    return jsonify({'items': [l.to_dict() for l in pag.items], 'total': pag.total, 'pages': pag.pages}), 200
