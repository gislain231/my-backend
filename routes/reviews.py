from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.review import Review
from models.booking import Booking
from models.user import User
from main import db

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    booking = Booking.query.get(data['booking_id'])
    if not booking or booking.user_id != user_id:
        return jsonify({'message': 'Invalid booking'}), 400
    
    if booking.status != 'completed':
        return jsonify({'message': 'Cannot review incomplete booking'}), 400
    
    if Review.query.filter_by(booking_id=booking.id).first():
        return jsonify({'message': 'Review already submitted'}), 400
    
    review = Review(
        booking_id=booking.id,
        reviewer_id=user_id,
        target_id=booking.driver_id if booking.service_type == 'carsharing' else booking.provider_id,
        vehicle_id=booking.vehicle_id,
        rating=data['rating'],
        comment=data.get('comment'),
        review_type=booking.service_type
    )
    
    db.session.add(review)
    db.session.commit()
    
    # Update user ratings
    update_user_ratings(review.target_id, review.review_type)
    
    return jsonify(review.to_dict()), 201

def update_user_ratings(user_id, review_type):
    """Update user's average rating"""
    reviews = Review.query.filter_by(
        target_id=user_id,
        review_type=review_type
    ).all()
    
    if not reviews:
        return
    
    avg_rating = sum(r.rating for r in reviews) / len(reviews)
    
    user = User.query.get(user_id)
    if review_type == 'carsharing':
        user.driver_rating = avg_rating
    else:
        user.detailing_rating = avg_rating
    
    db.session.commit()