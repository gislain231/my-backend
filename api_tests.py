#!/usr/bin/env python3
"""
API Testing Suite for Car Sharing & Detailing App
"""
import requests
import json
import time
from datetime import datetime, timedelta

class APITester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None
        
    def print_test(self, test_name, status, response=None):
        """Print test result with formatting"""
        if status:
            print(f"✅ {test_name}")
        else:
            print(f"❌ {test_name}")
            if response:
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
        print()

    def test_health_check(self):
        """Test if the server is running"""
        try:
            response = self.session.get(f"{self.base_url}/")
            self.print_test("Health Check", response.status_code in [200, 404])
            return response.status_code in [200, 404]
        except requests.exceptions.ConnectionError:
            self.print_test("Health Check", False)
            return False

    def test_user_registration(self):
        """Test user registration"""
        data = {
            'email': f'test{int(time.time())}@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '+1234567890'
        }
        
        response = self.session.post(f"{self.base_url}/register", json=data)
        success = response.status_code == 201
        self.print_test("User Registration", success, response if not success else None)
        
        if success:
            result = response.json()
            self.access_token = result.get('access_token')
            self.refresh_token = result.get('refresh_token')
        
        return success

    def test_user_login(self):
        """Test user login"""
        data = {
            'email': 'admin@carsharing.com',
            'password': 'admin123'
        }
        
        response = self.session.post(f"{self.base_url}/login", json=data)
        success = response.status_code == 200
        self.print_test("User Login", success, response if not success else None)
        
        if success:
            result = response.json()
            self.access_token = result.get('access_token')
            self.refresh_token = result.get('refresh_token')
        
        return success

    def test_get_profile(self):
        """Test getting user profile"""
        if not self.access_token:
            self.print_test("Get Profile", False)
            return False
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.session.get(f"{self.base_url}/profile", headers=headers)
        success = response.status_code == 200
        self.print_test("Get Profile", success, response if not success else None)
        return success

    def test_get_vehicles(self):
        """Test getting vehicles"""
        response = self.session.get(f"{self.base_url}/vehicles")
        success = response.status_code == 200
        self.print_test("Get Vehicles", success, response if not success else None)
        return success

    def test_get_detailing_services(self):
        """Test getting detailing services"""
        response = self.session.get(f"{self.base_url}/detailing/services")
        success = response.status_code == 200
        self.print_test("Get Detailing Services", success, response if not success else None)
        return success

    def test_create_booking(self):
        """Test creating a car sharing booking"""
        if not self.access_token:
            self.print_test("Create Booking", False)
            return False
        
        # First get available vehicles
        vehicles_response = self.session.get(f"{self.base_url}/vehicles")
        if vehicles_response.status_code != 200:
            self.print_test("Create Booking", False)
            return False
        
        vehicles = vehicles_response.json()
        if not vehicles:
            self.print_test("Create Booking - No vehicles available", False)
            return False
        
        vehicle_id = vehicles[0]['id']
        
        # Create booking
        start_time = datetime.utcnow() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        booking_data = {
            'vehicle_id': vehicle_id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'pickup': {
                'address': '123 Main St',
                'lat': 34.0522,
                'lng': -118.2437
            }
        }
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.session.post(f"{self.base_url}/carsharing/book", 
                                   json=booking_data, headers=headers)
        success = response.status_code == 201
        self.print_test("Create Car Sharing Booking", success, response if not success else None)
        return success

    def test_get_notifications(self):
        """Test getting notifications"""
        if not self.access_token:
            self.print_test("Get Notifications", False)
            return False
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.session.get(f"{self.base_url}/notifications", headers=headers)
        success = response.status_code == 200
        self.print_test("Get Notifications", success, response if not success else None)
        return success

    def test_admin_dashboard(self):
        """Test admin dashboard access"""
        if not self.access_token:
            self.print_test("Admin Dashboard", False)
            return False
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.session.get(f"{self.base_url}/admin/dashboard", headers=headers)
        success = response.status_code == 200
        self.print_test("Admin Dashboard", success, response if not success else None)
        return success

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting API Tests for Car Sharing & Detailing App")
        print("=" * 60)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Get Profile", self.test_get_profile),
            ("Get Vehicles", self.test_get_vehicles),
            ("Get Detailing Services", self.test_get_detailing_services),
            ("Create Booking", self.test_create_booking),
            ("Get Notifications", self.test_get_notifications),
            ("Admin Dashboard", self.test_admin_dashboard),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing: {test_name}")
            print("-" * 40)
            if test_func():
                passed += 1
        
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! API is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the application logs.")
        
        return passed == total

def main():
    """Main function to run API tests"""
    tester = APITester()
    tester.run_all_tests()

if __name__ == '__main__':
    main() 