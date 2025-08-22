from datetime import datetime
from main import db

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    color = db.Column(db.String(50))
    vehicle_type = db.Column(db.String(50), nullable=False)  # car, motorcycle, bus, etc.
    seating_capacity = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(db.String(20))
    transmission = db.Column(db.String(20))
    daily_rate = db.Column(db.Numeric(10, 2))
    hourly_rate = db.Column(db.Numeric(10, 2))
    is_available = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    carsharing_bookings = db.relationship('CarsharingBooking', backref='vehicle', lazy=True)
    detailing_bookings = db.relationship('DetailingBooking', backref='vehicle', lazy=True)
    reviews = db.relationship('Review', backref='vehicle', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'license_plate': self.license_plate,
            'color': self.color,
            'type': self.vehicle_type,
            'seating_capacity': self.seating_capacity,
            'fuel_type': self.fuel_type,
            'transmission': self.transmission,
            'rates': {
                'daily': float(self.daily_rate) if self.daily_rate else None,
                'hourly': float(self.hourly_rate) if self.hourly_rate else None
            },
            'availability': self.is_available,
            'approved': self.is_approved,
            'location': {
                'lat': self.latitude,
                'lng': self.longitude
            } if self.latitude and self.longitude else None
        }

class BusAgency(db.Model):
    __tablename__ = 'bus_agencies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    routes = db.relationship('BusRoute', backref='agency', lazy=True)

class BusRoute(db.Model):
    __tablename__ = 'bus_routes'
    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('bus_agencies.id'), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    seats = db.relationship('BusSeat', backref='route', lazy=True)

class BusSeat(db.Model):
    __tablename__ = 'bus_seats'
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('bus_routes.id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    is_booked = db.Column(db.Boolean, default=False)
    booked_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    booked_at = db.Column(db.DateTime)