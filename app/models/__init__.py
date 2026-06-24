"""
app/models/__init__.py
SQLAlchemy models for Abubaker Portfolio Platform
"""

from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import json


# ─── Role constants (NOT a DB model) ─────────────────────────

class UserRole:
    """Plain constants class — not a SQLAlchemy model."""
    SUPER_ADMIN = 'super_admin'
    ADMIN       = 'admin'
    EDITOR      = 'editor'
    VIEWER      = 'viewer'
    CLIENT      = 'client'

    ALL = [SUPER_ADMIN, ADMIN, EDITOR, VIEWER, CLIENT]


# ─── User ─────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), nullable=False)
    email         = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(20), default='viewer', nullable=False)
    is_active     = db.Column(db.Boolean, default=True)
    is_verified   = db.Column(db.Boolean, default=False)
    avatar_url    = db.Column(db.String(512))
    phone         = db.Column(db.String(30))        # encrypted in service layer
    totp_secret   = db.Column(db.String(64))
    totp_enabled  = db.Column(db.Boolean, default=False)
    recovery_codes= db.Column(db.Text)              # JSON array, hashed
    last_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    audit_logs    = db.relationship('AuditLog', back_populates='user', lazy='dynamic')
    messages      = db.relationship('Message', back_populates='user', lazy='dynamic')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256:600000')

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_private=False):
        data = {
            'id': self.id, 'name': self.name, 'role': self.role,
            'is_active': self.is_active, 'is_verified': self.is_verified,
            'avatar_url': self.avatar_url, 'created_at': self.created_at.isoformat(),
        }
        if include_private:
            data['email'] = self.email
            data['phone'] = self.phone
            data['totp_enabled'] = self.totp_enabled
            data['last_login_at'] = self.last_login_at.isoformat() if self.last_login_at else None
        return data

    def __repr__(self):
        return f'<User {self.email} [{self.role}]>'


# ─── Refresh Token ────────────────────────────────────────────

class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    jti        = db.Column(db.String(64), unique=True, nullable=False, index=True)
    device     = db.Column(db.String(200))
    ip_address = db.Column(db.String(45))
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='refresh_tokens')


# ─── Project ──────────────────────────────────────────────────

class Project(db.Model):
    __tablename__ = 'projects'

    id            = db.Column(db.Integer, primary_key=True)
    slug          = db.Column(db.String(120), unique=True, nullable=False, index=True)
    title_ar      = db.Column(db.String(200), nullable=False)
    title_en      = db.Column(db.String(200), nullable=False)
    desc_ar       = db.Column(db.Text)
    desc_en       = db.Column(db.Text)
    challenge_ar  = db.Column(db.Text)
    challenge_en  = db.Column(db.Text)
    solution_ar   = db.Column(db.Text)
    solution_en   = db.Column(db.Text)
    results_ar    = db.Column(db.Text)
    results_en    = db.Column(db.Text)
    category      = db.Column(db.String(30), nullable=False)   # mobile|web|backend|ai
    status        = db.Column(db.String(20), default='published')  # draft|published|archived
    cover_url     = db.Column(db.String(512))
    gallery       = db.Column(db.Text)   # JSON array of image URLs
    tech_stack    = db.Column(db.Text)   # JSON array
    live_url      = db.Column(db.String(512))
    github_url    = db.Column(db.String(512))
    case_study_url= db.Column(db.String(512))
    is_featured   = db.Column(db.Boolean, default=False)
    sort_order    = db.Column(db.Integer, default=0)
    view_count    = db.Column(db.Integer, default=0)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_gallery(self):
        return json.loads(self.gallery) if self.gallery else []

    def get_tech_stack(self):
        return json.loads(self.tech_stack) if self.tech_stack else []

    def to_dict(self, lang='en', include_raw=False):
        data = {
            'id': self.id, 'slug': self.slug,
            'title': self.title_ar if lang == 'ar' else self.title_en,
            'description': self.desc_ar if lang == 'ar' else self.desc_en,
            'challenge': self.challenge_ar if lang == 'ar' else self.challenge_en,
            'solution': self.solution_ar if lang == 'ar' else self.solution_en,
            'results': self.results_ar if lang == 'ar' else self.results_en,
            'category': self.category, 'status': self.status,
            'cover_url': self.cover_url, 'gallery': self.get_gallery(),
            'tech_stack': self.get_tech_stack(),
            'live_url': self.live_url, 'github_url': self.github_url,
            'case_study_url': self.case_study_url,
            'is_featured': self.is_featured, 'sort_order': self.sort_order,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_raw:
            data.update({
                'title_ar': self.title_ar, 'title_en': self.title_en,
                'desc_ar': self.desc_ar, 'desc_en': self.desc_en,
                'challenge_ar': self.challenge_ar, 'challenge_en': self.challenge_en,
                'solution_ar': self.solution_ar, 'solution_en': self.solution_en,
                'results_ar': self.results_ar, 'results_en': self.results_en,
            })
        return data


# ─── Service ──────────────────────────────────────────────────

class Service(db.Model):
    __tablename__ = 'services'

    id          = db.Column(db.Integer, primary_key=True)
    icon        = db.Column(db.String(10))
    title_ar    = db.Column(db.String(200), nullable=False)
    title_en    = db.Column(db.String(200), nullable=False)
    desc_ar     = db.Column(db.Text)
    desc_en     = db.Column(db.Text)
    tags        = db.Column(db.Text)   # JSON array
    sort_order  = db.Column(db.Integer, default=0)
    is_active   = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, lang='en', include_raw=False):
        data = {
            'id': self.id, 'icon': self.icon,
            'title': self.title_ar if lang == 'ar' else self.title_en,
            'description': self.desc_ar if lang == 'ar' else self.desc_en,
            'tags': json.loads(self.tags) if self.tags else [],
            'sort_order': self.sort_order, 'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_raw:
            data.update({
                'title_ar': self.title_ar, 'title_en': self.title_en,
                'desc_ar': self.desc_ar, 'desc_en': self.desc_en,
            })
        return data


# ─── Blog Post ────────────────────────────────────────────────

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id              = db.Column(db.Integer, primary_key=True)
    slug            = db.Column(db.String(200), unique=True, nullable=False, index=True)
    title_ar        = db.Column(db.String(300), nullable=False)
    title_en        = db.Column(db.String(300), nullable=False)
    excerpt_ar      = db.Column(db.Text)
    excerpt_en      = db.Column(db.Text)
    content_ar      = db.Column(db.Text)
    content_en      = db.Column(db.Text)
    cover_url       = db.Column(db.String(512))
    category        = db.Column(db.String(50))
    tags            = db.Column(db.Text)   # JSON array
    status          = db.Column(db.String(20), default='draft')  # draft|published
    is_featured     = db.Column(db.Boolean, default=False)
    read_time_min   = db.Column(db.Integer, default=5)
    view_count      = db.Column(db.Integer, default=0)
    seo_title_ar    = db.Column(db.String(300))
    seo_title_en    = db.Column(db.String(300))
    seo_desc_ar     = db.Column(db.Text)
    seo_desc_en     = db.Column(db.Text)
    published_at    = db.Column(db.DateTime)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id       = db.Column(db.Integer, db.ForeignKey('users.id'))

    author   = db.relationship('User', backref='blog_posts')
    comments = db.relationship('BlogComment', back_populates='post', lazy='dynamic')

    def to_dict(self, lang='en', include_content=False, include_raw=False):
        data = {
            'id': self.id, 'slug': self.slug,
            'title': self.title_ar if lang == 'ar' else self.title_en,
            'excerpt': self.excerpt_ar if lang == 'ar' else self.excerpt_en,
            'cover_url': self.cover_url, 'category': self.category,
            'tags': json.loads(self.tags) if self.tags else [],
            'status': self.status, 'is_featured': self.is_featured,
            'read_time_min': self.read_time_min, 'view_count': self.view_count,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author': self.author.to_dict() if self.author else None,
        }
        if include_content:
            data['content'] = self.content_ar if lang == 'ar' else self.content_en
        if include_raw:
            data.update({
                'title_ar': self.title_ar, 'title_en': self.title_en,
                'excerpt_ar': self.excerpt_ar, 'excerpt_en': self.excerpt_en,
                'content_ar': self.content_ar, 'content_en': self.content_en,
                'seo_title_ar': self.seo_title_ar, 'seo_title_en': self.seo_title_en,
                'seo_desc_ar': self.seo_desc_ar, 'seo_desc_en': self.seo_desc_en,
            })
        return data


class BlogComment(db.Model):
    __tablename__ = 'blog_comments'

    id         = db.Column(db.Integer, primary_key=True)
    post_id    = db.Column(db.Integer, db.ForeignKey('blog_posts.id', ondelete='CASCADE'))
    author     = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(255), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    is_approved= db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    post = db.relationship('BlogPost', back_populates='comments')


# ─── Testimonial ──────────────────────────────────────────────

class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    id          = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(120), nullable=False)
    client_role_ar = db.Column(db.String(200))
    client_role_en = db.Column(db.String(200))
    text_ar     = db.Column(db.Text, nullable=False)
    text_en     = db.Column(db.Text, nullable=False)
    avatar_url  = db.Column(db.String(512))
    rating      = db.Column(db.Integer, default=5)
    is_active   = db.Column(db.Boolean, default=True)
    sort_order  = db.Column(db.Integer, default=0)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, lang='en', include_raw=False):
        data = {
            'id': self.id, 'client_name': self.client_name,
            'client_role': self.client_role_ar if lang == 'ar' else self.client_role_en,
            'text': self.text_ar if lang == 'ar' else self.text_en,
            'avatar_url': self.avatar_url, 'rating': self.rating,
            'is_active': self.is_active, 'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_raw:
            data.update({
                'client_role_ar': self.client_role_ar, 'client_role_en': self.client_role_en,
                'text_ar': self.text_ar, 'text_en': self.text_en,
            })
        return data


# ─── Contact Message ─────────────────────────────────────────

class Message(db.Model):
    __tablename__ = 'messages'

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name        = db.Column(db.String(120), nullable=False)
    email       = db.Column(db.String(255), nullable=False)  # encrypted
    phone       = db.Column(db.String(50))                   # encrypted
    subject     = db.Column(db.String(300))
    body        = db.Column(db.Text, nullable=False)
    status      = db.Column(db.String(20), default='new')    # new|read|replied|archived
    ip_address  = db.Column(db.String(45))
    is_spam     = db.Column(db.Boolean, default=False)
    replied_at  = db.Column(db.DateTime)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='messages')

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'email': self.email,
            'phone': self.phone, 'subject': self.subject, 'body': self.body,
            'status': self.status, 'created_at': self.created_at.isoformat(),
        }


# ─── Analytics Event ─────────────────────────────────────────

class AnalyticsEvent(db.Model):
    __tablename__ = 'analytics_events'

    id          = db.Column(db.Integer, primary_key=True)
    event_type  = db.Column(db.String(50), nullable=False, index=True)   # page_view|project_view|contact_click|etc
    path        = db.Column(db.String(512))
    referrer    = db.Column(db.String(512))
    country     = db.Column(db.String(5))
    city        = db.Column(db.String(100))
    device      = db.Column(db.String(20))   # desktop|mobile|tablet
    browser     = db.Column(db.String(50))
    os          = db.Column(db.String(50))
    ip_address  = db.Column(db.String(45))   # hashed for privacy
    session_id  = db.Column(db.String(64))
    user_agent  = db.Column(db.String(512))
    lang        = db.Column(db.String(5))    # ar|en
    meta        = db.Column(db.Text)         # JSON extra data
    created_at  = db.Column(db.DateTime, default=datetime.utcnow, index=True)


# ─── Media ────────────────────────────────────────────────────

class MediaFile(db.Model):
    __tablename__ = 'media_files'

    id           = db.Column(db.Integer, primary_key=True)
    filename     = db.Column(db.String(255), nullable=False)
    original_name= db.Column(db.String(255))
    file_path    = db.Column(db.String(512), nullable=False)
    url          = db.Column(db.String(512), nullable=False)
    mime_type    = db.Column(db.String(100))
    file_size    = db.Column(db.Integer)
    width        = db.Column(db.Integer)
    height       = db.Column(db.Integer)
    alt_ar       = db.Column(db.String(300))
    alt_en       = db.Column(db.String(300))
    folder       = db.Column(db.String(100), default='general')
    uploaded_by  = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    uploader = db.relationship('User', backref='media_files')

    def to_dict(self, lang='en'):
        return {
            'id': self.id, 'filename': self.filename,
            'url': self.url, 'mime_type': self.mime_type,
            'file_size': self.file_size, 'width': self.width, 'height': self.height,
            'alt': self.alt_ar if lang == 'ar' else self.alt_en,
            'folder': self.folder, 'created_at': self.created_at.isoformat(),
        }


# ─── Audit Log ────────────────────────────────────────────────

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action      = db.Column(db.String(100), nullable=False, index=True)
    resource    = db.Column(db.String(100))
    resource_id = db.Column(db.Integer)
    old_value   = db.Column(db.Text)   # JSON snapshot before
    new_value   = db.Column(db.Text)   # JSON snapshot after
    ip_address  = db.Column(db.String(45))
    user_agent  = db.Column(db.String(512))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', back_populates='audit_logs')

    def to_dict(self):
        return {
            'id': self.id, 'action': self.action,
            'resource': self.resource, 'resource_id': self.resource_id,
            'ip_address': self.ip_address,
            'user': self.user.to_dict() if self.user else None,
            'created_at': self.created_at.isoformat(),
        }
