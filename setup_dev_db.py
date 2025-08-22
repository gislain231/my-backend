#!/usr/bin/env python3
"""
Development Database Setup Script
Uses SQLite for easy development and testing
"""
import os
import sys
from main import create_app, db
from config import Config

def setup_dev_database():
    """Setup development database with SQLite"""
    try:
        app = create_app()
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ All tables created successfully")
            
            # Create sample data
            create_sample_data()
            
            return True
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def create_sample_data():
    """Create sample data for development"""
    try:
        from models.user import User
        from models.vehicle import Vehicle
        from models.service import DetailingService
        
        # Check if sample data already exists
        if User.query.filter_by(email='admin@carsharing.com').first():
            print("✅ Sample data already exists")
            return True
        
        # Create admin user
        admin = User(
            email='admin@carsharing.com',
            first_name='Admin',
            last_name='User',
            phone='+1234567890',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample driver
        driver = User(
            email='driver@carsharing.com',
            first_name='John',
            last_name='Driver',
            phone='+1987654321',
            is_driver=True
        )
        driver.set_password('driver123')
        db.session.add(driver)
        
        # Create sample detailing provider
        provider = User(
            email='provider@carsharing.com',
            first_name='Jane',
            last_name='Provider',
            phone='+1555555555',
            is_detailing_provider=True,
            service_radius_km=20
        )
        provider.set_password('provider123')
        db.session.add(provider)
        
        db.session.commit()
        
        # Create sample vehicle
        vehicle = Vehicle(
            owner_id=driver.id,
            make='Toyota',
            model='Camry',
            year=2020,
            license_plate='ABC123',
            vehicle_type='sedan',
            seating_capacity=5,
            daily_rate=50.00,
            hourly_rate=10.00,
            is_available=True,
            is_approved=True,
            latitude=34.0522,
            longitude=-118.2437
        )
        db.session.add(vehicle)
        
        # Create sample detailing service
        service = DetailingService(
            name='Basic Wash',
            description='Exterior wash and interior vacuum',
            base_price=25.00,
            duration=30,
            is_active=True
        )
        db.session.add(service)
        
        db.session.commit()
        print("✅ Sample data created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Development Database")
    print("=" * 40)
    
    # Update config to use SQLite for development
    Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_database.db'
    
    if setup_dev_database():
        print("\n" + "=" * 40)
        print("✅ Development database setup completed!")
        print("\n📋 Sample Accounts:")
        print("   Admin: admin@carsharing.com / admin123")
        print("   Driver: driver@carsharing.com / driver123")
        print("   Provider: provider@carsharing.com / provider123")
        print("\n🌐 Start the application with: python main.py")
        print("🧪 Run tests with: python -m pytest")
        print("🔧 Run API tests with: python api_tests.py")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1)

if __name__ == '__main__':
    main() 