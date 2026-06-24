"""tests/unit/test_validators.py"""
from app.utils.validators import validate_email, validate_password

def test_valid_emails():
    assert validate_email('user@example.com') is True
    assert validate_email('user+tag@sub.domain.co') is True

def test_invalid_emails():
    assert validate_email('notanemail') is False
    assert validate_email('@domain.com') is False
    assert validate_email('') is False

def test_strong_password():
    assert validate_password('Strong@1234') is None

def test_weak_password_short():
    assert validate_password('Sh@1') is not None

def test_weak_password_no_upper():
    assert validate_password('alllower1!') is not None

def test_weak_password_no_special():
    assert validate_password('NoSpecial123') is not None
