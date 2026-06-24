"""app/utils/audit.py — Audit log helper"""
from flask import request
from app import db
from app.models import AuditLog
import json

def log_action(action: str, resource: str = None, resource_id: int = None,
               ip: str = None, ua: str = None, extra: dict = None):
    try:
        al = AuditLog(
            action=action, resource=resource, resource_id=resource_id,
            ip_address=ip or request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip(),
            user_agent=(ua or request.headers.get('User-Agent',''))[:512],
            new_value=json.dumps(extra) if extra else None,
        )
        db.session.add(al)
    except Exception:
        pass
