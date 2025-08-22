#!/usr/bin/env python3
"""
Debug script to test Flask application
"""
from main import create_app, db
from config import Config

# Override config to use SQLite for testing
Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///debug_database.db'

def test_app_creation():
    """Test if the app can be created and basic routes work"""
    try:
        app = create_app()
        print("✅ App created successfully")
        
        with app.app_context():
            # Test database connection
            db.create_all()
            print("✅ Database tables created")
            
            # Test a simple route
            with app.test_client() as client:
                response = client.get('/')
                print(f"✅ Root route status: {response.status_code}")
                print(f"✅ Root route response: {response.get_data(as_text=True)}")
                
                # Test vehicles route
                response = client.get('/vehicles')
                print(f"✅ Vehicles route status: {response.status_code}")
                
                # Test auth route
                response = client.get('/register')
                print(f"✅ Register route status: {response.status_code}")
                
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🔍 Debugging Flask Application")
    print("=" * 40)
    
    if test_app_creation():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Tests failed!") 