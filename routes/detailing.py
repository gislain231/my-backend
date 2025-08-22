from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.service import DetailingService
from models.booking import DetailingBooking
from services.detailing import find_available_providers, create_detailing_booking
from main import db
from datetime import datetime

detailing_bp = Blueprint('detailing', __name__)

@detailing_bp.route('/services', methods=['GET'])
def get_services():
    services = DetailingService.query.filter_by(is_active=True).all()
    return jsonify([s.to_dict() for s in services])

@detailing_bp.route('/available', methods=['GET'])
def get_available_providers():
    service_id = request.args.get('service_id')
    try:
        start_time = datetime.fromisoformat(request.args.get('start_time'))
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid parameters'}), 400
    
    providers = find_available_providers(service_id, start_time, (lat, lng))
    return jsonify([{
        'provider': p['provider'].to_dict(),
        'service': p['service'].to_dict(),
        'estimated_price': p['estimated_price']
    } for p in providers])

@detailing_bp.route('/book', methods=['POST'])
@jwt_required()
def book_detailing():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['service_id', 'provider_id', 'vehicle_id', 'start_time', 'location']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        start_time = datetime.fromisoformat(data['start_time'])
    except ValueError:
        return jsonify({'message': 'Invalid date format'}), 400
    
    try:
        booking = create_detailing_booking(
            user_id=user_id,
            service_id=data['service_id'],
            provider_id=data['provider_id'],
            vehicle_id=data['vehicle_id'],
            start_time=start_time,
            location=data['location']
        )
        
        return jsonify(booking.to_dict()), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400