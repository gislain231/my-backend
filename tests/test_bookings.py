import pytest
from datetime import datetime, timedelta
from models.vehicle import Vehicle


def test_create_carsharing_booking(client, app, test_user, test_vehicle):
    """Test creating a carsharing booking"""
    # Login first
    login_res = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    token = login_res.json['access_token']

    # Re-query vehicle in current app context
    with app.app_context():
        vehicle = Vehicle.query.get(test_vehicle)

    # Create booking
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)

    response = client.post('/bookings/carsharing/book', 
        headers={'Authorization': f'Bearer {token}'},
        json={
            'vehicle_id': vehicle.id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'pickup': {
                'address': '123 Main St',
                'lat': 34.0522,
                'lng': -118.2437
            }
        }
    )
    print('Booking creation response:', response.status_code, response.json)
    assert response.status_code == 201
    assert response.json['status'] == 'pending'


def test_cancel_booking(client, app, test_user, test_vehicle):
    """Test canceling a booking"""
    # Login and create booking first
    login_res = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    token = login_res.json['access_token']

    # Re-query vehicle in current app context
    with app.app_context():
        vehicle = Vehicle.query.get(test_vehicle)

    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    booking_res = client.post('/bookings/carsharing/book', 
        headers={'Authorization': f'Bearer {token}'},
        json={
            'vehicle_id': vehicle.id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'pickup': {
                'address': '123 Main St',
                'lat': 34.0522,
                'lng': -118.2437
            }
        }
    )
    print('Booking creation response:', booking_res.status_code, booking_res.json)
    booking_id = booking_res.json['id']

    # Cancel booking
    cancel_res = client.post(f'/bookings/{booking_id}/cancel',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert cancel_res.status_code == 200
    assert cancel_res.json['message'] == 'Booking canceled successfully'