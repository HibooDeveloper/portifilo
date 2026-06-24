"""tests/conftest.py — Pytest fixtures"""
import pytest
from app import create_app, db as _db

@pytest.fixture(scope='session')
def app():
    app = create_app('development')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-jwt-secret',
        'SECRET_KEY': 'test-secret',
        'RATELIMIT_ENABLED': False,
        'CF_TURNSTILE_SECRET': '',
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        yield _db
        _db.session.rollback()

@pytest.fixture
def admin_user(db):
    from app.models import User
    u = User(name='Admin', email='admin@test.com', role='super_admin',
             is_active=True, is_verified=True)
    u.set_password('Admin@12345!')
    db.session.add(u); db.session.commit()
    return u

@pytest.fixture
def auth_headers(client, admin_user):
    resp = client.post('/api/auth/login', json={
        'email': 'admin@test.com', 'password': 'Admin@12345!'
    })
    token = resp.json['access_token']
    return {'Authorization': f'Bearer {token}'}
