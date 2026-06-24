"""app/services/mail_service.py"""
from flask import current_app, render_template_string
from flask_mail import Message as MailMsg
from app import mail

CONTACT_TEMPLATE = """
Subject: New Contact Message — {{ m.name }}

Name:    {{ m.name }}
Email:   {{ m.email }}
Phone:   {{ m.phone or 'N/A' }}
Subject: {{ m.subject or 'N/A' }}

Message:
{{ m.body }}

---
Received: {{ m.created_at }}
IP: {{ m.ip_address }}
"""

def send_contact_notification(message):
    body = render_template_string(CONTACT_TEMPLATE, m=message)
    msg  = MailMsg(
        subject=f"[Portfolio] New message from {message.name}",
        recipients=[current_app.config['CONTACT_EMAIL']],
        body=body,
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
    )
    mail.send(msg)

def send_otp_email(user, otp: str):
    msg = MailMsg(
        subject='Your verification code — Abubaker Portfolio',
        recipients=[user.email],
        body=f"Your OTP code is: {otp}\n\nValid for 10 minutes.",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
    )
    mail.send(msg)
