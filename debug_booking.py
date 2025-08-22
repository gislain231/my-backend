#!/usr/bin/env python3
"""
Debug script to test booking endpoints
"""
from main import create_app, db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///debug_booking.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def debug_bookings():
    """Debug booking endpoints"""
    print("🔍 Debugging Booking Endpoints")
    print("=" * 40)
    
    app = create_app(TestConfig)
    
    with app.app_context():
        # Create database tables
        db.create_all()
        print("✅ Database tables created")
        
        # Create test data
        from models.user import User
        from models.vehicle import Vehicle
        from models.service import DetailingService
        
        # Create test user
        user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone='+1234567890'
        )
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()  # Commit user first to get ID
        
        # Create test vehicle
        vehicle = Vehicle(
            owner_id=user.id,
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
        
        # Create test service
        service = DetailingService(
            name='Basic Wash',
            description='Exterior wash and interior vacuum',
            base_price=25.00,
            duration=30,
            is_active=True
        )
        db.session.add(service)
        
        db.session.commit()
        print("✅ Test data created")
        
        # Create test client
        client = app.test_client()
        
        # Test 1: Login
        print("\n🔍 Testing Login")
        login_response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpass'
        })
        print(f"Login status: {login_response.status_code}")
        if login_response.status_code == 200:
            token = login_response.get_json()['access_token']
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {login_response.get_data(as_text=True)}")
            return
        
        # Test 2: Create carsharing booking
        print("\n🔍 Testing Carsharing Booking")
        booking_data = {
            'vehicle_id': vehicle.id,
            'start_time': '2024-01-15T10:00:00',
            'end_time': '2024-01-15T12:00:00',
            'pickup': {
                'address': '123 Main St',
                'lat': 34.0522,
                'lng': -118.2437
            }
        }
        
        headers = {'Authorization': f'Bearer {token}'}
        response = client.post('/bookings/carsharing/book',
                             json=booking_data,
                             headers=headers)
        
        print(f"Carsharing booking status: {response.status_code}")
        print(f"Response: {response.get_data(as_text=True)}")
        
        # Test 3: Create detailing booking
        print("\n🔍 Testing Detailing Booking")
        detailing_data = {
            'service_id': service.id,
            'provider_id': user.id,
            'vehicle_id': vehicle.id,
            'start_time': '2024-01-15T14:00:00',
            'location': {
                'address': '123 Main St',
                'lat': 34.0522,
                'lng': -118.2437
            }
        }
        
        response = client.post('/detailing/book',
                             json=detailing_data,
                             headers=headers)
        
        print(f"Detailing booking status: {response.status_code}")
        print(f"Response: {response.get_data(as_text=True)}")

if __name__ == '__main__':
    debug_bookings() 