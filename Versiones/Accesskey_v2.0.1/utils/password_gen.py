# utils/password_gen.py
import secrets
import string

def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!#$%&"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
