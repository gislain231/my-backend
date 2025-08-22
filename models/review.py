from datetime import datetime
from main import db

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    review_type = db.Column(db.String(20), nullable=False)  # carsharing/detailing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'reviewer': self.reviewer.to_dict(),
            'target_user': self.target_user.to_dict(),
            'vehicle': self.vehicle.to_dict() if self.vehicle else None,
            'rating': self.rating,
            'comment': self.comment,
            'type': self.review_type,
            'created_at': self.created_at.isoformat()
        }