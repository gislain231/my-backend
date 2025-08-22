# Initialize all route blueprints
from routes.auth import auth_bp
from routes.vehicles import vehicles_bp
from routes.bookings import bookings_bp
from routes.payments import payments_bp
from routes.reviews import reviews_bp
from routes.notifications import notifications_bp
from routes.admin import admin_bp
from routes.carsharing import carsharing_bp
from routes.detailing import detailing_bp
from flask import Blueprint

# Create a main blueprint that will group all API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

def register_blueprints(app):
    """Register all route blueprints with the Flask application"""
    
    # Register individual blueprints under the main API blueprint
    api_bp.register_blueprint(auth_bp)
    api_bp.register_blueprint(vehicles_bp)
    api_bp.register_blueprint(bookings_bp)
    api_bp.register_blueprint(payments_bp)
    api_bp.register_blueprint(reviews_bp)
    api_bp.register_blueprint(notifications_bp)
    api_bp.register_blueprint(admin_bp)
    api_bp.register_blueprint(carsharing_bp)
    api_bp.register_blueprint(detailing_bp)
    
    # Register the main API blueprint with the app
    app.register_blueprint(api_bp)
    
# Export all blueprints for individual access if needed
__all__ = [
    'auth_bp',
    'vehicles_bp',
    'bookings_bp',
    'payments_bp',
    'reviews_bp',
    'notifications_bp',
    'admin_bp',
    'carsharing_bp',
    'detailing_bp'
]
