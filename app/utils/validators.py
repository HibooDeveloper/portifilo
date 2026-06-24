"""app/utils/validators.py"""
import re

EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

def validate_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email)) if email else False

def validate_password(pw: str) -> str | None:
    """Return error string or None if valid."""
    if not pw or len(pw) < 8:
        return 'Password must be at least 8 characters'
    if not re.search(r'[A-Z]', pw):
        return 'Password must contain an uppercase letter'
    if not re.search(r'[0-9]', pw):
        return 'Password must contain a number'
    if not re.search(r'[^a-zA-Z0-9]', pw):
        return 'Password must contain a special character'
    return None

def validate_slug(slug: str) -> bool:
    return bool(re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', slug)) if slug else False
