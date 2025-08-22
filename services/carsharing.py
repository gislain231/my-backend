from datetime import datetime, timedelta
from models.vehicle import Vehicle
from models.booking import CarsharingBooking
from utils.geoutils import calculate_distance
from main import db

def find_available_vehicles(start_time, end_time, location, radius_km=10):
    """
    Find available vehicles within a radius that don't have conflicting bookings
    Args:
        start_time: Booking start datetime
        end_time: Booking end datetime
        location: Tuple of (latitude, longitude)
        radius_km: Search radius in kilometers
    Returns:
        List of available Vehicle objects
    """
    # Get all approved and available vehicles
    vehicles = Vehicle.query.filter(
        Vehicle.is_approved == True,
        Vehicle.is_available == True
    ).all()

    available_vehicles = []
    
    for vehicle in vehicles:
        # Skip vehicles without location data
        if not vehicle.latitude or not vehicle.longitude:
            continue
            
        # Check if vehicle is within search radius
        vehicle_location = (vehicle.latitude, vehicle.longitude)
        distance = calculate_distance(location, vehicle_location)
        if distance > radius_km:
            continue
            
        # Check for booking conflicts
        has_conflict = CarsharingBooking.query.filter(
            CarsharingBooking.vehicle_id == vehicle.id,
            CarsharingBooking.status.in_(['confirmed', 'pending']),
            CarsharingBooking.start_time < end_time,
            CarsharingBooking.end_time > start_time
        ).first()
        
        if not has_conflict:
            available_vehicles.append(vehicle)
    
    return available_vehicles

def calculate_booking_price(vehicle, start_time, end_time):
    """
    Calculate booking price based on vehicle rates and duration
    Args:
        vehicle: Vehicle object
        start_time: Booking start datetime
        end_time: Booking end datetime
    Returns:
        Calculated price as float
    """
    duration_hours = (end_time - start_time).total_seconds() / 3600
    
    # Use hourly rate if duration < 24 hours and hourly rate exists
    if duration_hours < 24 and vehicle.hourly_rate:
        return float(vehicle.hourly_rate * duration_hours)
    else:
        # Use daily rate (round up to full days)
        days = (end_time - start_time).days + 1
        return float(vehicle.daily_rate * days)

def create_carsharing_booking(user_id, vehicle_id, start_time, end_time, pickup_location, dropoff_location=None):
    """
    Create a new carsharing booking
    Args:
        user_id: ID of user making the booking
        vehicle_id: ID of vehicle being booked
        start_time: Booking start datetime
        end_time: Booking end datetime
        pickup_location: Dict with address, lat, lng
        dropoff_location: Optional dict with address, lat, lng
    Returns:
        Created CarsharingBooking object
    """
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle or not vehicle.is_available:
        raise ValueError("Vehicle not available")
    
    price = calculate_booking_price(vehicle, start_time, end_time)
    
    booking = CarsharingBooking(
        user_id=user_id,
        vehicle_id=vehicle_id,
        driver_id=vehicle.owner_id,
        start_time=start_time,
        end_time=end_time,
        pickup_address=pickup_location['address'],
        pickup_latitude=pickup_location['lat'],
        pickup_longitude=pickup_location['lng'],
        dropoff_address=dropoff_location['address'] if dropoff_location else None,
        dropoff_latitude=dropoff_location['lat'] if dropoff_location else None,
        dropoff_longitude=dropoff_location['lng'] if dropoff_location else None,
        total_price=price,
        status='pending'
    )
    
    vehicle.is_available = False
    db.session.add(booking)
    db.session.commit()
    
    return booking