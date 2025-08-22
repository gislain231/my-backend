from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.vehicle import Vehicle
from models.booking import CarsharingBooking
from services.carsharing import find_available_vehicles, calculate_booking_price
from main import db
from datetime import datetime

carsharing_bp = Blueprint('carsharing', __name__)

@carsharing_bp.route('/available', methods=['GET'])
def get_available_vehicles():
    try:
        start_time = datetime.fromisoformat(request.args.get('start_time'))
        end_time = datetime.fromisoformat(request.args.get('end_time'))
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid parameters'}), 400
    
    vehicles = find_available_vehicles(start_time, end_time, (lat, lng))
    return jsonify([v.to_dict() for v in vehicles])

@carsharing_bp.route('/calculate-price', methods=['GET'])
def calculate_price():
    vehicle_id = request.args.get('vehicle_id')
    try:
        start_time = datetime.fromisoformat(request.args.get('start_time'))
        end_time = datetime.fromisoformat(request.args.get('end_time'))
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid date format'}), 400
    
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404
    
    price = calculate_booking_price(vehicle, start_time, end_time)
    return jsonify({'price': price})