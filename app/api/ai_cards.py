"""app/api/ai_cards.py — AI Cards API"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db, limiter
from app.models import AICard
from app.utils.rbac import roles_required, is_admin_request
from app.utils.audit import log_action

ai_cards_bp = Blueprint('ai_cards', __name__)


@ai_cards_bp.route('/', methods=['GET'])
@limiter.limit('200 per hour')
def list_ai_cards():
    lang     = request.args.get('lang', 'en')
    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    admin    = is_admin_request()

    q = AICard.query
    if not admin:
        q = q.filter_by(is_active=True)
    q = q.order_by(AICard.sort_order)
    paginated = q.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'items': [c.to_dict(lang, include_raw=admin) for c in paginated.items],
        'total': paginated.total, 'pages': paginated.pages, 'page': page,
    }), 200


@ai_cards_bp.route('/', methods=['POST'])
@jwt_required()
@roles_required('admin', 'super_admin')
def create_ai_card():
    d = request.get_json(silent=True) or {}
    c = AICard(icon=d.get('icon', ''), title_ar=d.get('title_ar', ''),
               title_en=d.get('title_en', ''), desc_ar=d.get('desc_ar'),
               desc_en=d.get('desc_en'), sort_order=d.get('sort_order', 0),
               is_active=d.get('is_active', True))
    db.session.add(c); db.session.flush()
    log_action('ai_card_created', 'ai_card', c.id); db.session.commit()
    return jsonify(c.to_dict(request.args.get('lang', 'en'), include_raw=True)), 201


@ai_cards_bp.route('/<int:cid>', methods=['PUT'])
@jwt_required()
@roles_required('admin', 'super_admin', 'editor')
def update_ai_card(cid):
    c = AICard.query.get_or_404(cid)
    d = request.get_json(silent=True) or {}
    for f in ['icon', 'title_ar', 'title_en', 'desc_ar', 'desc_en', 'sort_order', 'is_active']:
        if f in d:
            setattr(c, f, d[f])
    log_action('ai_card_updated', 'ai_card', c.id); db.session.commit()
    return jsonify(c.to_dict(request.args.get('lang', 'en'), include_raw=True)), 200


@ai_cards_bp.route('/<int:cid>', methods=['DELETE'])
@jwt_required()
@roles_required('super_admin')
def delete_ai_card(cid):
    c = AICard.query.get_or_404(cid)
    db.session.delete(c); db.session.commit()
    return jsonify({'message': 'Deleted'}), 200
