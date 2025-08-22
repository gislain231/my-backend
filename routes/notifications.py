from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.notification import Notification
from main import db

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    limit = request.args.get('limit', default=10, type=int)
    
    notifications = Notification.query.filter_by(
        user_id=user_id
    ).order_by(
        Notification.created_at.desc()
    ).limit(limit).all()
    
    return jsonify([n.to_dict() for n in notifications])

@notifications_bp.route('/mark-read', methods=['POST'])
@jwt_required()
def mark_notifications_read():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'notification_ids' in data:
        # Mark specific notifications as read
        Notification.query.filter(
            Notification.id.in_(data['notification_ids']),
            Notification.user_id == user_id
        ).update({'is_read': True})
    else:
        # Mark all notifications as read
        Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).update({'is_read': True})
    
    db.session.commit()
    return jsonify({'message': 'Notifications marked as read'})