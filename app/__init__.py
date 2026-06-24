"""
app/__init__.py
Flask application factory — Abubaker Portfolio Platform
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from celery import Celery
import redis
import os

# ─── Extensions ──────────────────────────────────────────────
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)
celery_app = Celery()


def create_app(config_name: str = None) -> Flask:
    """Application factory."""
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # ── Config ────────────────────────────────────────────────
    env = config_name or os.getenv('FLASK_ENV', 'development')
    from config.settings import config_map
    app.config.from_object(config_map[env])

    # ── Extensions init ───────────────────────────────────────
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    CORS(app, resources={r'/api/*': {'origins': app.config['CORS_ORIGINS']}})

    # ── Redis ─────────────────────────────────────────────────
    app.redis = redis.from_url(app.config['REDIS_URL'])

    # ── Celery ────────────────────────────────────────────────
    celery_app.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
    )

    # ── Blueprints ────────────────────────────────────────────
    from app.api.auth import auth_bp
    from app.api.projects import projects_bp
    from app.api.services import services_bp
    from app.api.blogs import blogs_bp
    from app.api.testimonials import testimonials_bp
    from app.api.messages import messages_bp
    from app.api.analytics import analytics_bp
    from app.api.media import media_bp
    from app.api.users import users_bp

    app.register_blueprint(auth_bp,         url_prefix='/api/auth')
    app.register_blueprint(projects_bp,     url_prefix='/api/projects')
    app.register_blueprint(services_bp,     url_prefix='/api/services')
    app.register_blueprint(blogs_bp,        url_prefix='/api/blogs')
    app.register_blueprint(testimonials_bp, url_prefix='/api/testimonials')
    app.register_blueprint(messages_bp,     url_prefix='/api/messages')
    app.register_blueprint(analytics_bp,    url_prefix='/api/analytics')
    app.register_blueprint(media_bp,        url_prefix='/api/media')
    app.register_blueprint(users_bp,        url_prefix='/api/users')

    # ── Frontend route ────────────────────────────────────────
    from flask import render_template

    @app.route('/')
    @app.route('/<path:path>')
    def index(path=''):
        return render_template('index.html')

    # ── Dev-only: serve uploads ───────────────────────────────
    @app.route('/uploads/<path:filepath>')
    def serve_uploads(filepath):
        from flask import send_from_directory
        import os
        upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
        return send_from_directory(upload_dir, filepath)

    # ── Health check ──────────────────────────────────────────
    @app.route('/health')
    def health():
        return {'status': 'ok', 'env': env}, 200

    # ── Shell context ─────────────────────────────────────────
    @app.shell_context_processor
    def make_shell_context():
        from app.models import user, project, service, blog, testimonial, message, audit_log
        return dict(db=db, app=app)

    return app
