"""
config/settings.py
Environment-specific configuration for Abubaker Portfolio Platform
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Shared configuration across all environments."""

    # ── Security ──────────────────────────────────────────────
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-change-me')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # ── HTTPS / cookies ───────────────────────────────────────
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    # PREFERRED_URL_SCHEME=https and SESSION_COOKIE_SECURE are enabled in
    # staging/production only (behind Nginx), so local http dev keeps working.
    SESSION_COOKIE_SECURE = False

    # ── Database ──────────────────────────────────────────────
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20,
    }

    # ── Redis ─────────────────────────────────────────────────
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # ── Celery ────────────────────────────────────────────────
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')

    # ── Mail ──────────────────────────────────────────────────
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@hibbo.tech')
    CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'abubaker@example.com')

    # ── Storage ───────────────────────────────────────────────
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'pdf'}
    BLOCKED_EXTENSIONS = {'exe', 'bat', 'sh', 'php', 'js', 'py', 'rb'}

    # ── Rate limiting ─────────────────────────────────────────
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    RATELIMIT_DEFAULT = '200 per day;50 per hour'
    RATELIMIT_LOGIN = '5 per minute'
    RATELIMIT_API = '100 per hour'

    # ── CORS ──────────────────────────────────────────────────
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # ── Pagination ────────────────────────────────────────────
    ITEMS_PER_PAGE = 12

    # ── Site metadata ─────────────────────────────────────────
    SITE_NAME = 'Abubaker Hobeldeen — Portfolio'
    SITE_URL = os.getenv('SITE_URL', 'https://hibbo.tech')
    SITE_DESCRIPTION = 'Software Engineer, Flutter Developer, AI Solutions Specialist based in Cairo, Egypt'

    # ── Encryption (for sensitive DB fields) ─────────────────
    FIELD_ENCRYPTION_KEY = os.getenv('FIELD_ENCRYPTION_KEY', '')

    # ── Cloudflare Turnstile ──────────────────────────────────
    CF_TURNSTILE_SECRET = os.getenv('CF_TURNSTILE_SECRET', '')
    CF_TURNSTILE_VERIFY_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # Use DATABASE_URL if set, otherwise SQLite in Flask's instance folder
    _default_db = os.getenv('DATABASE_URL')
    if not _default_db:
        _instance_path = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), 'instance')
        os.makedirs(_instance_path, exist_ok=True)
        _default_db = f"sqlite:///{_instance_path}/portfolio_dev.db"
    SQLALCHEMY_DATABASE_URI = _default_db
    # SQLite doesn't support connection pools — override BaseConfig
    SQLALCHEMY_ENGINE_OPTIONS = {}
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)  # Longer for dev
    CORS_ORIGINS = ['*']


class StagingConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://staging.hibbo.tech').split(',')
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'

    # Force strong secrets in production
    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app) if hasattr(BaseConfig, 'init_app') else None
        assert os.getenv('SECRET_KEY'), 'SECRET_KEY must be set in production'
        assert os.getenv('JWT_SECRET_KEY'), 'JWT_SECRET_KEY must be set in production'
        assert os.getenv('DATABASE_URL'), 'DATABASE_URL must be set in production'


config_map = {
    'development': DevelopmentConfig,
    'staging':     StagingConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig,
}
