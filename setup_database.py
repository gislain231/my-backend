#!/usr/bin/env python3
"""
Database setup script for Car Sharing & Detailing App
"""
import os
import sys
from sqlalchemy import create_engine, text
from main import create_app, db
from config import Config

def create_database():
    """Create the database if it doesn't exist"""
    # Connect to PostgreSQL server (not specific database)
    engine = create_engine('postgresql://user:password@localhost/postgres')
    
    try:
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='carsharing'"))
            if not result.fetchone():
                # Create database
                conn.execute(text("CREATE DATABASE carsharing"))
                print("✅ Database 'carsharing' created successfully")
            else:
                print("✅ Database 'carsharing' already exists")
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        print("Please make sure PostgreSQL is running and credentials are correct")
        return False
    
    return True

def setup_tables():
    """Create all tables in the database"""
    try:
        app = create_app()
        with app.app_context():
            db.create_all()
            print("✅ All tables created successfully")
            return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    try:
        app = create_app()
        with app.app_context():
            from models.user import User
            from models.vehicle import Vehicle
            from models.service import DetailingService
            
            # Create sample users
            if not User.query.filter_by(email='admin@carsharing.com').first():
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
    print("🚀 Setting up Car Sharing & Detailing App Database")
    print("=" * 50)
    
    # Step 1: Create database
    print("\n1. Creating database...")
    if not create_database():
        sys.exit(1)
    
    # Step 2: Create tables
    print("\n2. Creating tables...")
    if not setup_tables():
        sys.exit(1)
    
    # Step 3: Create sample data
    print("\n3. Creating sample data...")
    if not create_sample_data():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Database setup completed successfully!")
    print("\n📋 Sample Accounts:")
    print("   Admin: admin@carsharing.com / admin123")
    print("   Driver: driver@carsharing.com / driver123")
    print("   Provider: provider@carsharing.com / provider123")
    print("\n🌐 Start the application with: python main.py")

if __name__ == '__main__':
    main() 