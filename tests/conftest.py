import pytest
from main import create_app, db
from config import Config
from models.user import User
from models.vehicle import Vehicle
from models.service import DetailingService

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Create a test user fixture and return user id"""
    with app.app_context():
        user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone='+1234567890'
        )
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        return user.id

@pytest.fixture
def test_driver(app, test_user):
    """Create a test driver fixture and return driver id"""
    with app.app_context():
        user = User.query.get(test_user)
        user.is_driver = True
        db.session.commit()
        return user.id

@pytest.fixture
def test_detailing_provider(app):
    """Create a test detailing provider fixture and return provider id"""
    with app.app_context():
        provider = User(
            email='provider@example.com',
            first_name='Test',
            last_name='Provider',
            phone='+1987654321',
            is_detailing_provider=True,
            service_radius_km=20
        )
        provider.set_password('providerpass')
        db.session.add(provider)
        db.session.commit()
        return provider.id

@pytest.fixture
def test_vehicle(app, test_driver):
    """Create a test vehicle fixture and return vehicle id"""
    with app.app_context():
        vehicle = Vehicle(
            owner_id=test_driver,
            make='Toyota',
            model='Camry',
            year=2020,
            license_plate='ABC123',
            vehicle_type='sedan',
            seating_capacity=5,
            daily_rate=50.00,
            hourly_rate=10.00,
            is_available=True,
            is_approved=True
        )
        db.session.add(vehicle)
        db.session.commit()
        return vehicle.id

@pytest.fixture
def test_detailing_service(app):
    """Create a test detailing service fixture and return service id"""
    with app.app_context():
        service = DetailingService(
            name='Basic Wash',
            description='Exterior wash and interior vacuum',
            base_price=25.00,
            duration=30,
            is_active=True
        )
        db.session.add(service)
        db.session.commit()
        return service.id