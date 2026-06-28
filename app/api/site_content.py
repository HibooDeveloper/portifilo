"""app/api/site_content.py — editable bilingual homepage text content"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db, limiter
from app.models import SiteContent
from app.utils.rbac import roles_required
from app.utils.audit import log_action

site_content_bp = Blueprint('site_content', __name__)


@site_content_bp.route('/', methods=['GET'])
@limiter.limit('400 per hour')
def get_content():
    """Return every override as { key: {ar, en} }. Public — the homepage reads
    this to overlay admin edits on top of the bundled defaults."""
    items = SiteContent.query.all()
    return jsonify({c.key: {'ar': c.value_ar, 'en': c.value_en} for c in items}), 200


@site_content_bp.route('/', methods=['PUT'])
@jwt_required()
@roles_required('admin', 'super_admin', 'editor')
def update_content():
    """Upsert a batch of overrides. Body: { "updates": { key: {ar, en}, … } }
    (a bare { key: {ar, en} } map is also accepted)."""
    d = request.get_json(silent=True) or {}
    updates = d.get('updates', d)
    if not isinstance(updates, dict):
        return jsonify({'error': 'Invalid payload'}), 400

    for key, val in updates.items():
        if not key or not isinstance(val, dict):
            continue
        c = SiteContent.query.filter_by(key=key).first()
        if not c:
            c = SiteContent(key=key)
            db.session.add(c)
        if 'ar' in val:
            c.value_ar = val['ar']
        if 'en' in val:
            c.value_en = val['en']

    log_action('site_content_updated', 'site_content', None)
    db.session.commit()
    return jsonify({'message': 'Saved'}), 200
