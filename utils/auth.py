import secrets
from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt_identity
from models.user import User
from main import db

def generate_password_reset_token(user, expires_in=3600) -> str:
    """Generate a password reset token for the user"""
    user.password_reset_token = secrets.token_urlsafe(32)
    user.password_reset_expires = datetime.utcnow() + timedelta(seconds=expires_in)
    db.session.commit()
    return user.password_reset_token

def verify_password_reset_token(user, token) -> bool:
    """Verify if a password reset token is valid"""
    if (user.password_reset_token != token or 
        user.password_reset_expires < datetime.utcnow()):
        return False
    return True

def get_current_user():
    """Get the current authenticated user"""
    user_id = get_jwt_identity()
    return User.query.get(user_id)