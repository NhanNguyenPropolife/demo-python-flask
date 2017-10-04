'''Algorithm for encrypt'''
import bcrypt

def encrypt_password(password):
    """Encrypt password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(encoding='utf-8'), salt)
