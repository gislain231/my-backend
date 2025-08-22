import pytest
from datetime import datetime, timedelta
from models.service import DetailingService
from models.user import User
from models.vehicle import Vehicle

def test_get_detailing_services(client, test_detailing_service):
    """Test getting detailing services"""
    response = client.get('/detailing/services')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'Basic Wash'

def test_create_detailing_booking(client, app, test_user, test_detailing_service, test_detailing_provider, test_vehicle):
    """Test creating a detailing booking"""
    # Login first
    login_res = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    token = login_res.json['access_token']
    
    # Re-query objects in current app context
    with app.app_context():
        service = DetailingService.query.get(test_detailing_service)
        provider = User.query.get(test_detailing_provider)
        vehicle = Vehicle.query.get(test_vehicle)
    
    # Create booking
    start_time = datetime.utcnow() + timedelta(hours=24)
    response = client.post('/detailing/book', 
        headers={'Authorization': f'Bearer {token}'},
        json={
            'service_id': service.id,
            'provider_id': provider.id,
            'vehicle_id': vehicle.id,
            'start_time': start_time.isoformat(),
            'location': {
                'address': '123 Main St',
                'lat': 34.0522,
                'lng': -118.2437
            }
        }
    )
    print('Detailing booking creation response:', response.status_code, response.json)
    assert response.status_code == 201
    assert response.json['status'] == 'confirmed'