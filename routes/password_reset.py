from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from main import db
from utils.emails import send_password_reset_email
from datetime import datetime, timedelta
import secrets

password_reset_bp = Blueprint('password_reset', __name__)

@password_reset_bp.route('/request-reset', methods=['POST'])
def request_password_reset():
    email = request.json.get('email')
    if not email:
        return jsonify({'message': 'Email is required'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        # Don't reveal whether user exists for security
        return jsonify({'message': 'If this email exists, a reset link has been sent'}), 200
    
    # Generate token and send email
    token = user.generate_reset_token()
    reset_link = f"https://yourapp.com/reset-password?token={token}&email={user.email}"
    
    # Send email (implementation below)
    send_password_reset_email(user.email, reset_link)
    
    return jsonify({'message': 'If this email exists, a reset link has been sent'}), 200

@password_reset_bp.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.json.get('email')
    token = request.json.get('token')
    new_password = request.json.get('new_password')
    
    if not all([email, token, new_password]):
        return jsonify({'message': 'Email, token and new password are required'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Invalid email'}), 400
    
    if not user.verify_reset_token(token):
        return jsonify({'message': 'Invalid or expired token'}), 400
    
    # Update password and clear token
    user.set_password(new_password)
    user.password_reset_token = None
    user.password_reset_expires = None
    db.session.commit()
    
    return jsonify({'message': 'Password updated successfully'}), 200

@password_reset_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')
    
    if not all([current_password, new_password]):
        return jsonify({'message': 'Current and new password are required'}), 400
    
    user = User.query.get(user_id)
    if not user.check_password(current_password):
        return jsonify({'message': 'Current password is incorrect'}), 400
    
    user.set_password(new_password)
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200