"""app/utils/rbac.py — Role-based access control decorator"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

ROLE_HIERARCHY = {'super_admin': 4, 'admin': 3, 'editor': 2, 'viewer': 1, 'client': 0}

ADMIN_ROLES = {'super_admin', 'admin', 'editor'}


def is_admin_request():
    """Check if the incoming request has a valid JWT with admin+ role.

    Call this inside an endpoint function (not as a decorator).
    Returns True only if a valid JWT is present AND the role is admin+.
    """
    try:
        verify_jwt_in_request(optional=True)
        claims = get_jwt()
        role = claims.get('role', 'viewer')
        return role in ADMIN_ROLES
    except Exception:
        return False


def roles_required(*roles):
    """Decorator: allow access if JWT role is in `roles`."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role   = claims.get('role', 'viewer')
            if role not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def min_role(min_role_name: str):
    """Allow if user's role level >= min level."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role  = get_jwt().get('role','viewer')
            if ROLE_HIERARCHY.get(role, 0) < ROLE_HIERARCHY.get(min_role_name, 0):
                return jsonify({'error': 'Insufficient permissions'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
