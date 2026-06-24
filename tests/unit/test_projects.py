"""tests/unit/test_projects.py"""

def test_list_projects_empty(client):
    r = client.get('/api/projects/')
    assert r.status_code == 200
    assert r.json['items'] == []

def test_create_project_requires_auth(client):
    r = client.post('/api/projects/', json={'title_en':'Test','category':'web'})
    assert r.status_code == 401

def test_create_and_list_project(client, auth_headers):
    payload = {
        'title_en': 'Test Project', 'title_ar': 'مشروع اختبار',
        'desc_en': 'A test project', 'desc_ar': 'مشروع للاختبار',
        'category': 'web', 'status': 'published',
        'tech_stack': ['Flask', 'MySQL'],
    }
    r = client.post('/api/projects/', json=payload, headers=auth_headers)
    assert r.status_code == 201
    assert r.json['slug']
    r2 = client.get('/api/projects/?lang=ar')
    assert r2.status_code == 200
    assert r2.json['items'][0]['title'] == 'مشروع اختبار'
