"""tests/unit/test_auth.py"""

def test_register_success(client):
    r = client.post('/api/auth/register', json={
        'name': 'Test User', 'email': 'test@example.com', 'password': 'Test@12345!'
    })
    assert r.status_code == 201
    assert 'access_token' in r.json

def test_register_duplicate_email(client):
    client.post('/api/auth/register', json={'name':'A','email':'dup@ex.com','password':'Test@12345!'})
    r = client.post('/api/auth/register', json={'name':'B','email':'dup@ex.com','password':'Test@12345!'})
    assert r.status_code == 409

def test_register_weak_password(client):
    r = client.post('/api/auth/register', json={'name':'X','email':'x@ex.com','password':'weak'})
    assert r.status_code == 422

def test_login_success(client, admin_user):
    r = client.post('/api/auth/login', json={'email':'admin@test.com','password':'Admin@12345!'})
    assert r.status_code == 200
    assert 'access_token' in r.json

def test_login_wrong_password(client, admin_user):
    r = client.post('/api/auth/login', json={'email':'admin@test.com','password':'wrong'})
    assert r.status_code == 401

def test_me_requires_auth(client):
    r = client.get('/api/auth/me')
    assert r.status_code == 401

def test_me_with_auth(client, auth_headers):
    r = client.get('/api/auth/me', headers=auth_headers)
    assert r.status_code == 200
    assert r.json['role'] == 'super_admin'
