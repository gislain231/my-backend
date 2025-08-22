from datetime import datetime
from main import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_type = db.Column(db.String(20), nullable=False)  # 'carsharing' or 'detailing'
    status = db.Column(db.String(20), default='pending')  # pending/confirmed/completed/canceled
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payment = db.relationship('Payment', backref='booking', uselist=False, lazy=True)
    review = db.relationship('Review', backref='booking', uselist=False, lazy=True)
    
    __mapper_args__ = {
        'polymorphic_on': service_type,
        'polymorphic_identity': 'booking'
    }

    def to_dict(self):
        return {
            'id': self.id,
            'service_type': self.service_type,
            'status': self.status,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'total_price': float(self.total_price),
            'created_at': self.created_at.isoformat()
        }

class CarsharingBooking(Booking):
    __tablename__ = 'carsharing_bookings'
    
    id = db.Column(db.Integer, db.ForeignKey('bookings.id'), primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pickup_address = db.Column(db.String(255), nullable=False)
    pickup_latitude = db.Column(db.Float, nullable=False)
    pickup_longitude = db.Column(db.Float, nullable=False)
    dropoff_address = db.Column(db.String(255))
    dropoff_latitude = db.Column(db.Float)
    dropoff_longitude = db.Column(db.Float)
    distance_km = db.Column(db.Float)
    estimated_duration = db.Column(db.Integer)  # in minutes
    
    __mapper_args__ = {
        'polymorphic_identity': 'carsharing'
    }

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'vehicle': self.vehicle.to_dict(),
            'driver': self.driver.to_dict(),
            'pickup_location': {
                'address': self.pickup_address,
                'lat': self.pickup_latitude,
                'lng': self.pickup_longitude
            },
            'dropoff_location': {
                'address': self.dropoff_address,
                'lat': self.dropoff_latitude,
                'lng': self.dropoff_longitude
            } if self.dropoff_address else None,
            'distance_km': self.distance_km,
            'estimated_duration': self.estimated_duration
        })
        return base_dict

class DetailingBooking(Booking):
    __tablename__ = 'detailing_bookings'
    
    id = db.Column(db.Integer, db.ForeignKey('bookings.id'), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('detailing_services.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    
    __mapper_args__ = {
        'polymorphic_identity': 'detailing'
    }

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'service': self.service.to_dict(),
            'provider': self.provider.to_dict(),
            'vehicle': self.vehicle.to_dict(),
            'location': {
                'address': self.address,
                'lat': self.latitude,
                'lng': self.longitude
            },
            'notes': self.notes
        })
        return base_dict

class BusSeatBooking(Booking):
    __tablename__ = 'bus_seat_bookings'
    id = db.Column(db.Integer, db.ForeignKey('bookings.id'), primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('bus_routes.id'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('bus_seats.id'), nullable=False)
    agency_id = db.Column(db.Integer, db.ForeignKey('bus_agencies.id'), nullable=False)
    notes = db.Column(db.Text)

    __mapper_args__ = {
        'polymorphic_identity': 'bus_seat'
    }

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'route_id': self.route_id,
            'seat_id': self.seat_id,
            'agency_id': self.agency_id,
            'notes': self.notes
        })
        return base_dict