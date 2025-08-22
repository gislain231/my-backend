import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User
from main import db
from utils.emails import send_password_reset_email
from utils.response import error_response

class AuthService:
    @staticmethod
    def register_user(email, password, first_name, last_name, phone):
        """Register a new user with the system"""
        if User.query.filter_by(email=email).first():
            return error_response("Email already registered", 400)

        try:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            return {
                'user': new_user.to_dict(),
                'tokens': AuthService._generate_tokens(new_user.id)
            }
        except Exception as e:
            db.session.rollback()
            return error_response(str(e), 500)

    @staticmethod
    def authenticate_user(email, password):
        """Authenticate a user and return tokens"""
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return error_response("Invalid credentials", 401)
        
        return {
            'user': user.to_dict(),
            'tokens': AuthService._generate_tokens(user.id)
        }

    @staticmethod
    def refresh_token(user_id):
        """Generate new access token using refresh token"""
        return {
            'access_token': create_access_token(identity=user_id)
        }

    @staticmethod
    def initiate_password_reset(email):
        """Start password reset process by generating token and sending email"""
        user = User.query.filter_by(email=email).first()
        if not user:
            # Don't reveal whether user exists for security
            return {'message': 'If this email exists, a reset link has been sent'}
        
        reset_token = secrets.token_urlsafe(32)
        user.password_reset_token = reset_token
        user.password_reset_expires = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()
        
        # Send email with reset link
        reset_link = f"https://yourapp.com/reset-password?token={reset_token}&email={email}"
        send_password_reset_email(email, reset_link)
        
        return {'message': 'Password reset link sent'}

    @staticmethod
    def complete_password_reset(email, token, new_password):
        """Complete password reset process"""
        user = User.query.filter_by(email=email).first()
        if not user:
            return error_response("Invalid email", 400)
        
        if (not user.password_reset_token or 
            user.password_reset_token != token or
            user.password_reset_expires < datetime.utcnow()):
            return error_response("Invalid or expired token", 400)
        
        user.set_password(new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        db.session.commit()
        
        return {'message': 'Password updated successfully'}

    @staticmethod
    def _generate_tokens(user_id):
        """Generate JWT tokens for authenticated user"""
        return {
            'access_token': create_access_token(identity=user_id),
            'refresh_token': create_refresh_token(identity=user_id)
        }

    @staticmethod
    def get_current_user(user_id):
        """Get full user details for authenticated user"""
        user = User.query.get(user_id)
        if not user:
            return error_response("User not found", 404)
        return user.to_dict()