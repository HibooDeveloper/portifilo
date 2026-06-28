"""
app/__init__.py
Flask application factory — Abubaker Portfolio Platform
"""

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
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

    # ── Trust Nginx's X-Forwarded-* headers (https scheme, host) ──
    # Required so url_for/redirects use https behind the proxy and
    # avoid http→https redirect loops.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

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
    from app.api.skills import skills_bp
    from app.api.ai_cards import ai_cards_bp

    app.register_blueprint(auth_bp,         url_prefix='/api/auth')
    app.register_blueprint(projects_bp,     url_prefix='/api/projects')
    app.register_blueprint(services_bp,     url_prefix='/api/services')
    app.register_blueprint(blogs_bp,        url_prefix='/api/blogs')
    app.register_blueprint(testimonials_bp, url_prefix='/api/testimonials')
    app.register_blueprint(messages_bp,     url_prefix='/api/messages')
    app.register_blueprint(analytics_bp,    url_prefix='/api/analytics')
    app.register_blueprint(media_bp,        url_prefix='/api/media')
    app.register_blueprint(users_bp,        url_prefix='/api/users')
    app.register_blueprint(skills_bp,       url_prefix='/api/skills')
    app.register_blueprint(ai_cards_bp,     url_prefix='/api/ai-cards')

    # ── Frontend routes (language-prefixed) ───────────────────
    from flask import Blueprint, g, redirect, render_template

    SUPPORTED_LANGS = ('ar', 'en')
    DEFAULT_LANG = 'ar'

    site_bp = Blueprint('site', __name__)

    @site_bp.url_value_preprocessor
    def _pull_lang(endpoint, values):
        # Extract the language segment so views don't each take a `lang` arg.
        g.lang = (values or {}).pop('lang', DEFAULT_LANG)

    @site_bp.url_defaults
    def _inject_lang(endpoint, values):
        # Auto-carry the current language into url_for('site.*') links.
        if 'lang' not in values and getattr(g, 'lang', None):
            values['lang'] = g.lang

    @site_bp.route('/', strict_slashes=False)
    @site_bp.route('/<path:path>')
    def page(path=''):
        return render_template(
            'index.html',
            lang=g.lang,
            site_url=app.config.get('SITE_URL', ''),
        )

    # All content lives under /ar/... and /en/...  static, /api, /health and
    # /.well-known are excluded because <any(ar,en)> matches only those two words.
    app.register_blueprint(site_bp, url_prefix='/<any(ar,en):lang>')

    # Root → always Arabic. Fixed 302, never reads Accept-Language.
    @app.route('/')
    def root_redirect():
        return redirect('/ar', code=302)

    # Any other non-prefixed path → its Arabic equivalent.
    @app.route('/<path:path>')
    def legacy_redirect(path):
        return redirect(f'/ar/{path}', code=302)

    # ── Dev-only: serve uploads ───────────────────────────────
    @app.route('/uploads/<path:filepath>')
    def serve_uploads(filepath):
        from flask import send_from_directory
        import os
        upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
        return send_from_directory(upload_dir, filepath)

    # ── SEO: robots.txt & sitemap.xml ─────────────────────────
    @app.route('/robots.txt')
    def robots_txt():
        from flask import Response
        site_url = app.config.get('SITE_URL', '').rstrip('/')
        body = (
            "User-agent: *\n"
            "Allow: /\n"
            "Disallow: /api/\n"
            "Disallow: /uploads/\n"
            f"Sitemap: {site_url}/sitemap.xml\n"
        )
        return Response(body, mimetype='text/plain')

    @app.route('/sitemap.xml')
    def sitemap_xml():
        from flask import Response
        site_url = app.config.get('SITE_URL', '').rstrip('/')
        urls = []
        for lang in SUPPORTED_LANGS:
            loc = f"{site_url}/{lang}"
            alts = ''.join(
                f'<xhtml:link rel="alternate" hreflang="{l}" href="{site_url}/{l}"/>'
                for l in SUPPORTED_LANGS
            )
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{site_url}/{DEFAULT_LANG}"/>'
            urls.append(
                f'<url><loc>{loc}</loc>{alts}'
                f'<changefreq>weekly</changefreq><priority>1.0</priority></url>'
            )
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
            + ''.join(urls) +
            '</urlset>'
        )
        return Response(xml, mimetype='application/xml')

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
