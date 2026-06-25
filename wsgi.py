"""wsgi.py — Gunicorn entry point"""
import os
from app import create_app, celery_app  # celery_app is referenced by `celery -A wsgi:celery_app`

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    app.run()
