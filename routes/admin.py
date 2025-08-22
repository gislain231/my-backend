from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.vehicle import Vehicle
from models.booking import Booking
from main import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    
    stats = {
        'total_users': User.query.count(),
        'total_vehicles': Vehicle.query.count(),
        'total_bookings': Booking.query.count(),
        'pending_approvals': Vehicle.query.filter_by(is_approved=False).count()
    }
    
    return jsonify(stats)

@admin_bp.route('/vehicles/pending', methods=['GET'])
@jwt_required()
def pending_vehicle_approvals():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    
    vehicles = Vehicle.query.filter_by(is_approved=False).all()
    return jsonify([v.to_dict() for v in vehicles])

@admin_bp.route('/vehicles/<int:vehicle_id>/approve', methods=['POST'])
@jwt_required()
def approve_vehicle(vehicle_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user.is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
    
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    vehicle.is_approved = True
    db.session.commit()
    
    return jsonify({'message': 'Vehicle approved successfully'})