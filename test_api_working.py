#!/usr/bin/env python3
"""
Working API Test - Tests the Flask app directly without external server
"""
import json
import time
from main import create_app, db
from config import Config

# Override config for testing
Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///test_api.db'

def test_api_endpoints():
    """Test API endpoints directly using Flask test client"""
    print("🚀 Testing Car Sharing & Detailing API")
    print("=" * 50)
    
    # Create app
    app = create_app()
    
    with app.app_context():
        # Create database tables
        db.create_all()
        print("✅ Database tables created")
        
        # Create test client
        client = app.test_client()
        
        # Test 1: Health Check
        print("\n🔍 Testing: Health Check")
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Health Check - Server is running")
        else:
            print(f"❌ Health Check - Status: {response.status_code}")
        
        # Test 2: User Registration
        print("\n🔍 Testing: User Registration")
        registration_data = {
            'email': f'test{int(time.time())}@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '+1234567890'
        }
        response = client.post('/register', 
                             data=json.dumps(registration_data),
                             content_type='application/json')
        if response.status_code in [201, 200]:
            print("✅ User Registration - Success")
        else:
            print(f"❌ User Registration - Status: {response.status_code}")
        
        # Test 3: User Login
        print("\n🔍 Testing: User Login")
        login_data = {
            'email': 'admin@carsharing.com',
            'password': 'admin123'
        }
        response = client.post('/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        if response.status_code == 200:
            print("✅ User Login - Success")
            result = response.get_json()
            access_token = result.get('access_token')
        else:
            print(f"❌ User Login - Status: {response.status_code}")
            access_token = None
        
        # Test 4: Get Profile (if logged in)
        if access_token:
            print("\n🔍 Testing: Get Profile")
            headers = {'Authorization': f'Bearer {access_token}'}
            response = client.get('/profile', headers=headers)
            if response.status_code == 200:
                print("✅ Get Profile - Success")
            else:
                print(f"❌ Get Profile - Status: {response.status_code}")
        
        # Test 5: Get Vehicles
        print("\n🔍 Testing: Get Vehicles")
        response = client.get('/vehicles')
        if response.status_code == 200:
            print("✅ Get Vehicles - Success")
        else:
            print(f"❌ Get Vehicles - Status: {response.status_code}")
        
        # Test 6: Get Detailing Services
        print("\n🔍 Testing: Get Detailing Services")
        response = client.get('/detailing/services')
        if response.status_code == 200:
            print("✅ Get Detailing Services - Success")
        else:
            print(f"❌ Get Detailing Services - Status: {response.status_code}")
        
        # Test 7: Create Booking (if logged in)
        if access_token:
            print("\n🔍 Testing: Create Booking")
            booking_data = {
                'vehicle_id': 1,
                'start_time': '2024-01-15T10:00:00',
                'end_time': '2024-01-15T12:00:00',
                'pickup': {
                    'address': '123 Main St',
                    'lat': 34.0522,
                    'lng': -118.2437
                }
            }
            headers = {'Authorization': f'Bearer {access_token}'}
            response = client.post('/carsharing/book',
                                 data=json.dumps(booking_data),
                                 content_type='application/json',
                                 headers=headers)
            if response.status_code in [201, 200]:
                print("✅ Create Booking - Success")
            else:
                print(f"❌ Create Booking - Status: {response.status_code}")
        
        # Test 8: Get Notifications (if logged in)
        if access_token:
            print("\n🔍 Testing: Get Notifications")
            headers = {'Authorization': f'Bearer {access_token}'}
            response = client.get('/notifications', headers=headers)
            if response.status_code == 200:
                print("✅ Get Notifications - Success")
            else:
                print(f"❌ Get Notifications - Status: {response.status_code}")
        
        # Test 9: Admin Dashboard (if logged in)
        if access_token:
            print("\n🔍 Testing: Admin Dashboard")
            headers = {'Authorization': f'Bearer {access_token}'}
            response = client.get('/admin/dashboard', headers=headers)
            if response.status_code == 200:
                print("✅ Admin Dashboard - Success")
            else:
                print(f"❌ Admin Dashboard - Status: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("✅ API testing completed!")

if __name__ == '__main__':
    test_api_endpoints() 