# File: utils/validators.py
import re

def validate_username(username):
    """Username must be alphanumeric (letters and numbers only)"""
    if not username.isalnum():
        return False, "Username must contain only letters and numbers (no special characters)."
    return True, ""

def validate_email(email):
    """Checks for standard email format"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        return False, "Invalid email format."
    return True, ""

def validate_password(password):
    """
    Checks: 8 chars, 1 Upper, 1 Lower, 1 Number, 1 Special Char
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[@$!%*?&#]", password):
        return False, "Password must contain at least one special character (@$!%*?&#)."
    
    return True, ""