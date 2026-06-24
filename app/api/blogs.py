"""app/api/blogs.py — Blog API"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db, limiter
from app.models import BlogPost, BlogComment
from app.utils.rbac import roles_required, is_admin_request
from app.utils.audit import log_action
import json, re

blogs_bp = Blueprint('blogs', __name__)

def _slug(t): return re.sub(r'[^a-z0-9-]','',re.sub(r'\s+','-',t.lower().strip()))

@blogs_bp.route('/', methods=['GET'])
@limiter.limit('200 per hour')
def list_blogs():
    lang     = request.args.get('lang','en')
    category = request.args.get('category')
    search   = request.args.get('q')
    page     = int(request.args.get('page',1))
    per_page = int(request.args.get('per_page', current_app.config['ITEMS_PER_PAGE']))
    admin    = is_admin_request()

    q = BlogPost.query
    if not admin:
        q = q.filter_by(status='published')
    if category: q = q.filter_by(category=category)
    if search:
        like = f'%{search}%'
        q = q.filter((BlogPost.title_en.ilike(like)) | (BlogPost.title_ar.ilike(like)) |
                     (BlogPost.content_en.ilike(like)) | (BlogPost.content_ar.ilike(like)))
    q = q.order_by(BlogPost.published_at.desc())
    paginated = q.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [p.to_dict(lang, include_raw=admin) for p in paginated.items],
        'total': paginated.total, 'pages': paginated.pages, 'page': page,
    }), 200

@blogs_bp.route('/<slug>', methods=['GET'])
def get_blog(slug):
    lang  = request.args.get('lang','en')
    admin = is_admin_request()
    q = BlogPost.query.filter_by(slug=slug)
    if not admin:
        q = q.filter_by(status='published')
    p = q.first_or_404()
    p.view_count += 1; db.session.commit()
    return jsonify(p.to_dict(lang, include_content=True, include_raw=admin)), 200

@blogs_bp.route('/', methods=['POST'])
@jwt_required()
@roles_required('admin','super_admin','editor')
def create_blog():
    d  = request.get_json(silent=True) or {}
    uid = get_jwt_identity()
    slug = d.get('slug') or _slug(d.get('title_en',''))
    if BlogPost.query.filter_by(slug=slug).first(): slug += f"-{__import__('secrets').token_hex(3)}"
    p = BlogPost(
        slug=slug, author_id=uid,
        title_ar=d.get('title_ar',''), title_en=d.get('title_en',''),
        excerpt_ar=d.get('excerpt_ar'), excerpt_en=d.get('excerpt_en'),
        content_ar=d.get('content_ar'), content_en=d.get('content_en'),
        cover_url=d.get('cover_url'), category=d.get('category'),
        tags=json.dumps(d.get('tags',[])), status=d.get('status','draft'),
        read_time_min=d.get('read_time_min',5), is_featured=d.get('is_featured',False),
        seo_title_ar=d.get('seo_title_ar'), seo_title_en=d.get('seo_title_en'),
        seo_desc_ar=d.get('seo_desc_ar'), seo_desc_en=d.get('seo_desc_en'),
    )
    if d.get('status') == 'published': p.published_at = datetime.utcnow()
    db.session.add(p); db.session.flush()
    log_action('blog_created','blog',p.id); db.session.commit()
    return jsonify(p.to_dict(request.args.get('lang','en'), include_content=True, include_raw=True)), 201

@blogs_bp.route('/<int:pid>', methods=['PUT'])
@jwt_required()
@roles_required('admin','super_admin','editor')
def update_blog(pid):
    p = BlogPost.query.get_or_404(pid)
    d = request.get_json(silent=True) or {}
    fields = ['title_ar','title_en','excerpt_ar','excerpt_en','content_ar','content_en',
              'cover_url','category','status','read_time_min','is_featured',
              'seo_title_ar','seo_title_en','seo_desc_ar','seo_desc_en']
    for f in fields:
        if f in d: setattr(p, f, d[f])
    if 'tags' in d: p.tags = json.dumps(d['tags'])
    if d.get('status') == 'published' and not p.published_at: p.published_at = datetime.utcnow()
    log_action('blog_updated','blog',p.id); db.session.commit()
    return jsonify(p.to_dict(request.args.get('lang','en'), include_content=True, include_raw=True)), 200

@blogs_bp.route('/<int:pid>', methods=['DELETE'])
@jwt_required()
@roles_required('super_admin','admin')
def delete_blog(pid):
    p = BlogPost.query.get_or_404(pid)
    log_action('blog_deleted','blog',p.id)
    db.session.delete(p); db.session.commit()
    return jsonify({'message': 'Deleted'}), 200

@blogs_bp.route('/<int:pid>/comments', methods=['GET'])
def list_comments(pid):
    BlogPost.query.get_or_404(pid)
    items = BlogComment.query.filter_by(post_id=pid, is_approved=True).order_by(BlogComment.created_at).all()
    return jsonify([{'id':c.id,'author':c.author,'content':c.content,'created_at':c.created_at.isoformat()} for c in items]), 200

@blogs_bp.route('/<int:pid>/comments', methods=['POST'])
@limiter.limit('10 per hour')
def add_comment(pid):
    BlogPost.query.get_or_404(pid)
    d = request.get_json(silent=True) or {}
    c = BlogComment(post_id=pid, author=d.get('author','').strip()[:120],
                    email=d.get('email','').strip()[:255], content=d.get('content','').strip())
    if not c.author or not c.email or not c.content: return jsonify({'error': 'Missing fields'}), 422
    db.session.add(c); db.session.commit()
    return jsonify({'message': 'Comment submitted for review'}), 201
