#!/usr/bin/env python3
"""
Simple test to isolate JWT issue
"""
from main import create_app, db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///simple_test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def simple_test():
    """Simple test to check JWT token creation"""
    print("🔍 Simple JWT Test")
    print("=" * 30)
    
    app = create_app(TestConfig)
    
    with app.app_context():
        # Create database tables
        db.create_all()
        print("✅ Database tables created")
        
        # Create test user
        from models.user import User
        user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone='+1234567890'
        )
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        
        print(f"✅ User created with ID: {user.id}")
        
        # Test JWT token creation
        from flask_jwt_extended import create_access_token
        try:
            token = create_access_token(identity=user.id)
            print(f"✅ JWT token created: {token[:20]}...")
        except Exception as e:
            print(f"❌ JWT token creation failed: {e}")
        
        # Test login endpoint
        client = app.test_client()
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpass'
        })
        
        print(f"Login response status: {response.status_code}")
        print(f"Login response: {response.get_data(as_text=True)}")

if __name__ == '__main__':
    simple_test() 