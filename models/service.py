from datetime import datetime
from main import db
from utils.translation import translate_field, get_current_lang

class DetailingService(db.Model):
    __tablename__ = 'detailing_services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('DetailingBooking', backref='service', lazy=True)

    def to_dict(self, lang=None):
        if not lang:
            lang = get_current_lang()

        return {
            'id': self.id,
            'name': translate_field(self.name, lang),
            'description': translate_field(self.description, lang),
            'base_price': float(self.base_price),
            'duration': self.duration,
            'is_active': self.is_active
        }