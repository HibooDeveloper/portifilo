"""app/api/services.py — Services API"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app import db, limiter
from app.models import Service
from app.utils.rbac import roles_required, is_admin_request
from app.utils.audit import log_action
import json

services_bp = Blueprint('services', __name__)

@services_bp.route('/', methods=['GET'])
@limiter.limit('200 per hour')
def list_services():
    lang     = request.args.get('lang', 'en')
    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 24))
    admin    = is_admin_request()

    q = Service.query
    if not admin:
        q = q.filter_by(is_active=True)
    q = q.order_by(Service.sort_order)
    paginated = q.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'items': [s.to_dict(lang, include_raw=admin) for s in paginated.items],
        'total': paginated.total, 'pages': paginated.pages, 'page': page,
    }), 200

@services_bp.route('/', methods=['POST'])
@jwt_required()
@roles_required('admin','super_admin')
def create_service():
    d = request.get_json(silent=True) or {}
    s = Service(icon=d.get('icon',''), title_ar=d.get('title_ar',''),
                title_en=d.get('title_en',''), desc_ar=d.get('desc_ar'),
                desc_en=d.get('desc_en'), tags=json.dumps(d.get('tags',[])),
                sort_order=d.get('sort_order',0))
    db.session.add(s); db.session.flush()
    log_action('service_created','service',s.id); db.session.commit()
    return jsonify(s.to_dict(request.args.get('lang','en'), include_raw=True)), 201

@services_bp.route('/<int:sid>', methods=['PUT'])
@jwt_required()
@roles_required('admin','super_admin','editor')
def update_service(sid):
    s = Service.query.get_or_404(sid)
    d = request.get_json(silent=True) or {}
    for f in ['icon','title_ar','title_en','desc_ar','desc_en','sort_order','is_active']:
        if f in d: setattr(s, f, d[f])
    if 'tags' in d: s.tags = json.dumps(d['tags'])
    log_action('service_updated','service',s.id); db.session.commit()
    return jsonify(s.to_dict(request.args.get('lang','en'), include_raw=True)), 200

@services_bp.route('/<int:sid>', methods=['DELETE'])
@jwt_required()
@roles_required('super_admin')
def delete_service(sid):
    s = Service.query.get_or_404(sid)
    db.session.delete(s); db.session.commit()
    return jsonify({'message': 'Deleted'}), 200
