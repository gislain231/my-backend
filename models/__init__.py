from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_models(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# Import all models to ensure they're registered with SQLAlchemy
from models.user import User
from models.vehicle import Vehicle, BusAgency, BusRoute, BusSeat
from models.booking import Booking, CarsharingBooking, DetailingBooking, BusSeatBooking
from models.payment import Payment
from models.review import Review
from models.notification import Notification
from models.service import DetailingService