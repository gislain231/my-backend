from datetime import datetime, timedelta
from models.user import User
from models.booking import DetailingBooking
from models.service import DetailingService
from utils.geoutils import calculate_distance
from main import db

def find_available_providers(service_id, start_time, location, radius_km=15):
    """
    Find available detailing providers for a specific service
    Args:
        service_id: ID of detailing service
        start_time: Booking start datetime
        location: Tuple of (latitude, longitude)
        radius_km: Search radius in kilometers
    Returns:
        List of dicts with provider, service, and price info
    """
    service = DetailingService.query.get(service_id)
    if not service or not service.is_active:
        return []
    
    end_time = start_time + timedelta(minutes=service.duration)
    
    providers = User.query.filter(
        User.is_detailing_provider == True
    ).all()
    
    available_providers = []
    
    for provider in providers:
        # Skip providers without location data
        if not provider.latitude or not provider.longitude:
            continue
            
        # Check if provider is within service radius
        provider_location = (provider.latitude, provider.longitude)
        distance = calculate_distance(location, provider_location)
        if distance > provider.service_radius_km:
            continue
            
        # Check for booking conflicts
        has_conflict = DetailingBooking.query.filter(
            DetailingBooking.provider_id == provider.id,
            DetailingBooking.status.in_(['confirmed', 'in_progress']),
            DetailingBooking.start_time < end_time,
            DetailingBooking.end_time > start_time
        ).first()
        
        if not has_conflict:
            available_providers.append({
                'provider': provider,
                'service': service,
                'estimated_price': service.base_price
            })
    
    return available_providers

def create_detailing_booking(user_id, service_id, provider_id, vehicle_id, start_time, location):
    """
    Create a new detailing booking
    Args:
        user_id: ID of user making the booking
        service_id: ID of detailing service
        provider_id: ID of detailing provider
        vehicle_id: ID of vehicle being serviced
        start_time: Booking start datetime
        location: Dict with address, lat, lng
    Returns:
        Created DetailingBooking object
    """
    service = DetailingService.query.get(service_id)
    if not service or not service.is_active:
        raise ValueError("Service not available")
    
    end_time = start_time + timedelta(minutes=service.duration)
    
    booking = DetailingBooking(
        user_id=user_id,
        service_id=service_id,
        provider_id=provider_id,
        vehicle_id=vehicle_id,
        start_time=start_time,
        end_time=end_time,
        address=location['address'],
        latitude=location['lat'],
        longitude=location['lng'],
        total_price=service.base_price,
        status='confirmed'
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return booking