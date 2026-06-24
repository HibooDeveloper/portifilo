"""app/utils/turnstile.py — Cloudflare Turnstile verification"""
import requests
from flask import current_app

def verify_turnstile(token: str, ip: str = None) -> bool:
    secret = current_app.config.get('CF_TURNSTILE_SECRET')
    if not secret: return True
    if not token:  return False
    try:
        r = requests.post(
            current_app.config.get('CF_TURNSTILE_VERIFY_URL',
                'https://challenges.cloudflare.com/turnstile/v0/siteverify'),
            data={'secret': secret, 'response': token, 'remoteip': ip},
            timeout=5,
        )
        return r.json().get('success', False)
    except Exception:
        return False
