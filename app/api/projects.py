"""app/api/projects.py — Projects REST API"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt
from app import db, limiter
from app.models import Project
from app.utils.audit import log_action
from app.utils.rbac import roles_required, is_admin_request
import json, re

projects_bp = Blueprint('projects', __name__)

def _slug(text):
    return re.sub(r'[^a-z0-9-]', '', re.sub(r'\s+', '-', text.lower().strip()))

@projects_bp.route('/', methods=['GET'])
@limiter.limit('100 per hour')
def list_projects():
    lang     = request.args.get('lang', 'en')
    category = request.args.get('category')
    featured = request.args.get('featured')
    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', current_app.config['ITEMS_PER_PAGE']))
    admin    = is_admin_request()

    q = Project.query
    if not admin:
        q = q.filter_by(status='published')
    if category: q = q.filter_by(category=category)
    if featured:  q = q.filter_by(is_featured=True)
    q = q.order_by(Project.sort_order, Project.created_at.desc())
    paginated = q.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'items': [p.to_dict(lang, include_raw=admin) for p in paginated.items],
        'total': paginated.total, 'pages': paginated.pages, 'page': page,
    }), 200

@projects_bp.route('/<slug>', methods=['GET'])
def get_project(slug):
    lang  = request.args.get('lang', 'en')
    admin = is_admin_request()
    q = Project.query.filter_by(slug=slug)
    if not admin:
        q = q.filter_by(status='published')
    p = q.first_or_404()
    p.view_count += 1; db.session.commit()
    return jsonify(p.to_dict(lang, include_raw=admin)), 200

@projects_bp.route('/', methods=['POST'])
@jwt_required()
@roles_required('admin', 'super_admin')
def create_project():
    d    = request.get_json(silent=True) or {}
    lang = request.args.get('lang','en')
    slug = d.get('slug') or _slug(d.get('title_en', ''))
    if Project.query.filter_by(slug=slug).first():
        slug = f"{slug}-{__import__('secrets').token_hex(3)}"
    p = Project(
        slug=slug,
        title_ar=d.get('title_ar',''), title_en=d.get('title_en',''),
        desc_ar=d.get('desc_ar'), desc_en=d.get('desc_en'),
        challenge_ar=d.get('challenge_ar'), challenge_en=d.get('challenge_en'),
        solution_ar=d.get('solution_ar'), solution_en=d.get('solution_en'),
        results_ar=d.get('results_ar'), results_en=d.get('results_en'),
        category=d.get('category','web'), status=d.get('status','draft'),
        cover_url=d.get('cover_url'), live_url=d.get('live_url'),
        github_url=d.get('github_url'), case_study_url=d.get('case_study_url'),
        tech_stack=json.dumps(d.get('tech_stack',[])),
        gallery=json.dumps(d.get('gallery',[])),
        is_featured=d.get('is_featured', False),
        sort_order=d.get('sort_order', 0),
    )
    db.session.add(p); db.session.flush()
    log_action('project_created','project',p.id)
    db.session.commit()
    return jsonify(p.to_dict(lang, include_raw=True)), 201

@projects_bp.route('/<int:pid>', methods=['PUT'])
@jwt_required()
@roles_required('admin','super_admin','editor')
def update_project(pid):
    p = Project.query.get_or_404(pid)
    d = request.get_json(silent=True) or {}
    fields = ['title_ar','title_en','desc_ar','desc_en','challenge_ar','challenge_en',
              'solution_ar','solution_en','results_ar','results_en','category','status',
              'cover_url','live_url','github_url','case_study_url','is_featured','sort_order']
    for f in fields:
        if f in d: setattr(p, f, d[f])
    if 'tech_stack' in d: p.tech_stack = json.dumps(d['tech_stack'])
    if 'gallery'    in d: p.gallery    = json.dumps(d['gallery'])
    log_action('project_updated','project',p.id)
    db.session.commit()
    return jsonify(p.to_dict(request.args.get('lang','en'), include_raw=True)), 200

@projects_bp.route('/<int:pid>', methods=['DELETE'])
@jwt_required()
@roles_required('super_admin')
def delete_project(pid):
    p = Project.query.get_or_404(pid)
    log_action('project_deleted','project',p.id)
    db.session.delete(p); db.session.commit()
    return jsonify({'message': 'Deleted'}), 200
