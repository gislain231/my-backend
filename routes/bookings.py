from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.booking import Booking, CarsharingBooking, DetailingBooking
from models.user import User
from main import db
from decimal import Decimal

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/upcoming', methods=['GET'])
@jwt_required()
def get_upcoming_bookings():
    user_id = get_jwt_identity()
    
    carsharing = CarsharingBooking.query.filter(
        CarsharingBooking.user_id == user_id,
        CarsharingBooking.status.in_(['confirmed', 'pending'])
    ).all()
    
    detailing = DetailingBooking.query.filter(
        DetailingBooking.user_id == user_id,
        DetailingBooking.status.in_(['confirmed', 'pending'])
    ).all()
    
    return jsonify({
        'carsharing': [b.to_dict() for b in carsharing],
        'detailing': [b.to_dict() for b in detailing]
    })

@bookings_bp.route('/history', methods=['GET'])
@jwt_required()
def get_booking_history():
    user_id = get_jwt_identity()
    
    bookings = Booking.query.filter(
        Booking.user_id == user_id,
        Booking.status.in_(['completed', 'canceled'])
    ).order_by(Booking.start_time.desc()).limit(20).all()
    
    return jsonify([b.to_dict() for b in bookings])

@bookings_bp.route('/carsharing/book', methods=['POST'])
@jwt_required()
def create_carsharing_booking():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['vehicle_id', 'start_time', 'pickup']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        from datetime import datetime
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.fromisoformat(data.get('end_time', '')) if data.get('end_time') else None
    except ValueError:
        return jsonify({'message': 'Invalid date format'}), 400
    
    # Get vehicle to find the driver
    from models.vehicle import Vehicle
    vehicle = Vehicle.query.get(data['vehicle_id'])
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404
    
    # Calculate total price (simplified calculation)
    total_price = Decimal('0.0')
    if end_time:
        duration_hours = (end_time - start_time).total_seconds() / 3600
        total_price = vehicle.hourly_rate * Decimal(str(duration_hours))
    else:
        # Default to 1 hour if no end time
        total_price = vehicle.hourly_rate
    
    # Create booking
    booking = CarsharingBooking(
        user_id=user_id,
        vehicle_id=data['vehicle_id'],
        driver_id=vehicle.owner_id,  # The vehicle owner is the driver
        start_time=start_time,
        end_time=end_time,
        pickup_address=data['pickup']['address'],
        pickup_latitude=data['pickup']['lat'],
        pickup_longitude=data['pickup']['lng'],
        status='pending',
        total_price=total_price
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify(booking.to_dict()), 201

@bookings_bp.route('/<int:booking_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_booking(booking_id):
    user_id = get_jwt_identity()
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
    
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404
    
    booking.status = 'canceled'
    db.session.commit()
    
    return jsonify({'message': 'Booking canceled successfully'}), 200