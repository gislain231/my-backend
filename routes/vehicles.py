from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.vehicle import Vehicle, BusAgency, BusRoute, BusSeat
from models.booking import BusSeatBooking
from main import db
from datetime import datetime

vehicles_bp = Blueprint('vehicles', __name__)

@vehicles_bp.route('/', methods=['POST'])
@jwt_required()
def add_vehicle():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['make', 'model', 'year', 'license_plate', 'vehicle_type', 'seating_capacity']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    vehicle = Vehicle(
        owner_id=user_id,
        make=data['make'],
        model=data['model'],
        year=data['year'],
        license_plate=data['license_plate'],
        vehicle_type=data['vehicle_type'],
        seating_capacity=data['seating_capacity'],
        color=data.get('color'),
        fuel_type=data.get('fuel_type'),
        transmission=data.get('transmission'),
        daily_rate=data.get('daily_rate'),
        hourly_rate=data.get('hourly_rate')
    )
    
    db.session.add(vehicle)
    db.session.commit()
    
    return jsonify(vehicle.to_dict()), 201

@vehicles_bp.route('/', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.filter_by(is_available=True, is_approved=True).all()
    return jsonify([v.to_dict() for v in vehicles])

@vehicles_bp.route('/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return jsonify(vehicle.to_dict())

@vehicles_bp.route('/mine', methods=['GET'])
@jwt_required()
def get_my_vehicles():
    user_id = get_jwt_identity()
    vehicles = Vehicle.query.filter_by(owner_id=user_id).all()
    return jsonify([v.to_dict() for v in vehicles])

@vehicles_bp.route('/bus/agencies', methods=['GET'])
def get_bus_agencies():
    agencies = BusAgency.query.filter_by(approved=True).all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'email': a.email,
        'phone': a.phone
    } for a in agencies])

@vehicles_bp.route('/bus/agencies', methods=['POST'])
@jwt_required()
def register_bus_agency():
    data = request.get_json()
    required = ['name', 'email', 'phone']
    if not all(k in data for k in required):
        return jsonify({'message': 'Missing required fields'}), 400
    agency = BusAgency(name=data['name'], email=data['email'], phone=data['phone'], approved=False)
    db.session.add(agency)
    db.session.commit()
    return jsonify({'message': 'Bus agency registered, pending approval.'}), 201

@vehicles_bp.route('/bus/routes', methods=['GET'])
def get_bus_routes():
    routes = BusRoute.query.all()
    return jsonify([{
        'id': r.id,
        'agency_id': r.agency_id,
        'origin': r.origin,
        'destination': r.destination,
        'departure_time': r.departure_time.isoformat(),
        'available_seats': r.available_seats,
        'price': float(r.price)
    } for r in routes])

@vehicles_bp.route('/bus/routes', methods=['POST'])
@jwt_required()
def add_bus_route():
    data = request.get_json()
    required = ['agency_id', 'origin', 'destination', 'departure_time', 'available_seats', 'price']
    if not all(k in data for k in required):
        return jsonify({'message': 'Missing required fields'}), 400
    try:
        departure_time = datetime.fromisoformat(data['departure_time'])
    except Exception:
        return jsonify({'message': 'Invalid departure_time'}), 400
    route = BusRoute(
        agency_id=data['agency_id'],
        origin=data['origin'],
        destination=data['destination'],
        departure_time=departure_time,
        available_seats=data['available_seats'],
        price=data['price']
    )
    db.session.add(route)
    db.session.commit()
    return jsonify({'message': 'Bus route added.'}), 201

@vehicles_bp.route('/bus/seats', methods=['GET'])
def get_bus_seats():
    route_id = request.args.get('route_id')
    if not route_id:
        return jsonify({'message': 'Missing route_id'}), 400
    seats = BusSeat.query.filter_by(route_id=route_id).all()
    return jsonify([{
        'id': s.id,
        'seat_number': s.seat_number,
        'is_booked': s.is_booked
    } for s in seats])

@vehicles_bp.route('/bus/seats/book', methods=['POST'])
@jwt_required()
def book_bus_seat():
    user_id = get_jwt_identity()
    data = request.get_json()
    required = ['route_id', 'seat_id']
    if not all(k in data for k in required):
        return jsonify({'message': 'Missing required fields'}), 400
    seat = BusSeat.query.get(data['seat_id'])
    if not seat or seat.is_booked:
        return jsonify({'message': 'Seat not available'}), 400
    seat.is_booked = True
    seat.booked_by = user_id
    seat.booked_at = datetime.utcnow()
    booking = BusSeatBooking(
        user_id=user_id,
        service_type='bus_seat',
        status='pending',
        start_time=seat.route.departure_time,
        end_time=None,
        total_price=seat.route.price,
        route_id=seat.route_id,
        seat_id=seat.id,
        agency_id=seat.route.agency_id
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({'message': 'Bus seat booked!', 'booking': booking.to_dict()}), 201