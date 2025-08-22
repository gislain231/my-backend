from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.payment import Payment
from models.booking import Booking
from services.payment import process_payment
from main import db

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/create-intent', methods=['POST'])
@jwt_required()
def create_payment_intent():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    booking = Booking.query.get(data['booking_id'])
    if not booking or booking.user_id != user_id:
        return jsonify({'message': 'Invalid booking'}), 400
    
    if booking.status != 'pending':
        return jsonify({'message': 'Booking already processed'}), 400
    
    result = process_payment(booking, data['payment_method'])
    if not result['success']:
        return jsonify({'message': result['message']}), 400
    
    return jsonify({
        'client_secret': result['client_secret'],
        'payment_id': result['payment_id']
    })

@payments_bp.route('/confirm', methods=['POST'])
@jwt_required()
def confirm_payment():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    payment = Payment.query.get(data['payment_id'])
    if not payment or payment.user_id != user_id:
        return jsonify({'message': 'Invalid payment'}), 400
    
    if payment.status != 'pending':
        return jsonify({'message': 'Payment already processed'}), 400
    
    payment.status = 'completed'
    payment.booking.status = 'confirmed'
    db.session.commit()
    
    return jsonify({'message': 'Payment confirmed successfully'})