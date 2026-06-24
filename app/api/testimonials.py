"""app/api/testimonials.py"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app import db
from app.models import Testimonial
from app.utils.rbac import roles_required, is_admin_request

testimonials_bp = Blueprint('testimonials', __name__)

@testimonials_bp.route('/', methods=['GET'])
def list_testimonials():
    lang     = request.args.get('lang', 'en')
    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 24))
    admin    = is_admin_request()

    q = Testimonial.query
    if not admin:
        q = q.filter_by(is_active=True)
    q = q.order_by(Testimonial.sort_order)
    paginated = q.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'items': [t.to_dict(lang, include_raw=admin) for t in paginated.items],
        'total': paginated.total, 'pages': paginated.pages, 'page': page,
    }), 200

@testimonials_bp.route('/', methods=['POST'])
@jwt_required()
@roles_required('admin','super_admin')
def create_testimonial():
    d = request.get_json(silent=True) or {}
    t = Testimonial(
        client_name=d.get('client_name',''),
        client_role_ar=d.get('client_role_ar'), client_role_en=d.get('client_role_en'),
        text_ar=d.get('text_ar',''), text_en=d.get('text_en',''),
        avatar_url=d.get('avatar_url'), rating=d.get('rating',5),
        sort_order=d.get('sort_order',0)
    )
    db.session.add(t); db.session.commit()
    return jsonify(t.to_dict(request.args.get('lang','en'), include_raw=True)), 201

@testimonials_bp.route('/<int:tid>', methods=['PUT'])
@jwt_required()
@roles_required('admin','super_admin')
def update_testimonial(tid):
    t = Testimonial.query.get_or_404(tid)
    d = request.get_json(silent=True) or {}
    for f in ['client_name','client_role_ar','client_role_en','text_ar','text_en','avatar_url','rating','sort_order','is_active']:
        if f in d: setattr(t, f, d[f])
    db.session.commit()
    return jsonify(t.to_dict(request.args.get('lang','en'), include_raw=True)), 200

@testimonials_bp.route('/<int:tid>', methods=['DELETE'])
@jwt_required()
@roles_required('super_admin')
def delete_testimonial(tid):
    t = Testimonial.query.get_or_404(tid)
    db.session.delete(t); db.session.commit()
    return jsonify({'message': 'Deleted'}), 200
