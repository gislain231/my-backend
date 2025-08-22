from datetime import datetime, timedelta
from main import db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Roles
    is_admin = db.Column(db.Boolean, default=False)
    is_driver = db.Column(db.Boolean, default=False)
    is_detailing_provider = db.Column(db.Boolean, default=False)
    
    # Driver-specific fields
    driver_license = db.Column(db.String(50))
    driver_verified = db.Column(db.Boolean, default=False)
    driver_rating = db.Column(db.Float, default=5.0)
    
    # Detailing-specific fields
    detailing_rating = db.Column(db.Float, default=5.0)
    service_radius_km = db.Column(db.Integer, default=10)
    detailing_bio = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Relationships
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)
    carsharing_bookings = db.relationship('CarsharingBooking', foreign_keys='CarsharingBooking.user_id', backref='user', lazy=True)
    driver_bookings = db.relationship('CarsharingBooking', foreign_keys='CarsharingBooking.driver_id', backref='driver', lazy=True)
    detailing_bookings = db.relationship('DetailingBooking', foreign_keys='DetailingBooking.user_id', backref='customer', lazy=True)
    provider_bookings = db.relationship('DetailingBooking', foreign_keys='DetailingBooking.provider_id', backref='provider', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    reviews_given = db.relationship('Review', foreign_keys='Review.reviewer_id', backref='reviewer', lazy=True)
    reviews_received = db.relationship('Review', foreign_keys='Review.target_id', backref='target_user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    password_reset_token = db.Column(db.String(100))
    password_reset_expires = db.Column(db.DateTime)
    
    def generate_reset_token(self, expires_in=3600):
        self.password_reset_token = secrets.token_urlsafe(32)
        self.password_reset_expires = datetime.utcnow() + timedelta(seconds=expires_in)
        db.session.commit()
        return self.password_reset_token
    
    def verify_reset_token(self, token):
        if (self.password_reset_token != token or 
            self.password_reset_expires < datetime.utcnow()):
            return False
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'roles': {
                'admin': self.is_admin,
                'driver': self.is_driver,
                'detailing_provider': self.is_detailing_provider
            },
            'driver_info': {
                'license': self.driver_license,
                'verified': self.driver_verified,
                'rating': self.driver_rating
            } if self.is_driver else None,
            'detailing_info': {
                'rating': self.detailing_rating,
                'service_radius': self.service_radius_km,
                'bio': self.detailing_bio
            } if self.is_detailing_provider else None,
            'location': {
                'lat': self.latitude,
                'lng': self.longitude
            } if self.latitude and self.longitude else None
        }