from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from celery import Celery
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app, message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'])
    celery.conf.update(app.config)
    
    # Ensure db is bound to app context
    with app.app_context():
        db.create_all()

    # Register blueprints
    from routes.auth import auth_bp
    from routes.bookings import bookings_bp
    from routes.vehicles import vehicles_bp
    from routes.payments import payments_bp
    from routes.reviews import reviews_bp
    from routes.notifications import notifications_bp
    from routes.admin import admin_bp
    from routes.detailing import detailing_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(bookings_bp, url_prefix='/bookings')
    app.register_blueprint(vehicles_bp, url_prefix='/vehicles')
    app.register_blueprint(payments_bp, url_prefix='/payments')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(detailing_bp, url_prefix='/detailing')

    # Add a simple root route
    @app.route('/')
    def index():
        return {'message': 'Car Sharing & Detailing API - Rent cars or share rides with travelers', 'status': 'running'}

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)