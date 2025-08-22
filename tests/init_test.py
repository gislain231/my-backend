import pytest
from main import create_app
from models import db as _db
from config import Config

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(Config)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def db(app):
    """Provide database access for tests."""
    with app.app_context():
        yield _db