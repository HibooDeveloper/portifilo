"""app/api/skills.py — Skills API"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db, limiter
from app.models import Skill
from app.utils.rbac import roles_required, is_admin_request
from app.utils.audit import log_action

skills_bp = Blueprint('skills', __name__)


@skills_bp.route('/', methods=['GET'])
@limiter.limit('200 per hour')
def list_skills():
    lang     = request.args.get('lang', 'en')
    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    admin    = is_admin_request()

    q = Skill.query
    if not admin:
        q = q.filter_by(is_active=True)
    q = q.order_by(Skill.sort_order)
    paginated = q.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'items': [s.to_dict(lang, include_raw=admin) for s in paginated.items],
        'total': paginated.total, 'pages': paginated.pages, 'page': page,
    }), 200


@skills_bp.route('/', methods=['POST'])
@jwt_required()
@roles_required('admin', 'super_admin')
def create_skill():
    d = request.get_json(silent=True) or {}
    s = Skill(icon=d.get('icon', ''), name_ar=d.get('name_ar', ''),
              name_en=d.get('name_en', ''), percent=d.get('percent', 80),
              sort_order=d.get('sort_order', 0), is_active=d.get('is_active', True))
    db.session.add(s); db.session.flush()
    log_action('skill_created', 'skill', s.id); db.session.commit()
    return jsonify(s.to_dict(request.args.get('lang', 'en'), include_raw=True)), 201


@skills_bp.route('/<int:sid>', methods=['PUT'])
@jwt_required()
@roles_required('admin', 'super_admin', 'editor')
def update_skill(sid):
    s = Skill.query.get_or_404(sid)
    d = request.get_json(silent=True) or {}
    for f in ['icon', 'name_ar', 'name_en', 'percent', 'sort_order', 'is_active']:
        if f in d:
            setattr(s, f, d[f])
    log_action('skill_updated', 'skill', s.id); db.session.commit()
    return jsonify(s.to_dict(request.args.get('lang', 'en'), include_raw=True)), 200


@skills_bp.route('/<int:sid>', methods=['DELETE'])
@jwt_required()
@roles_required('super_admin')
def delete_skill(sid):
    s = Skill.query.get_or_404(sid)
    db.session.delete(s); db.session.commit()
    return jsonify({'message': 'Deleted'}), 200
