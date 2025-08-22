import pytest
from utils.auth import generate_password_reset_token, verify_password_reset_token
from models.user import User


def test_register(client):
    """Test user registration"""
    response = client.post('/auth/register', json={
        'email': 'new@example.com',
        'password': 'newpass123',
        'first_name': 'New',
        'last_name': 'User',
        'phone': '+1234567890'
    })
    assert response.status_code == 201
    assert 'access_token' in response.json


def test_login(client, test_user):
    """Test user login"""
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_password_reset(client, app, test_user):
    """Test password reset flow"""
    with app.app_context():
        user = User.query.get(test_user)
        # Generate reset token
        token = generate_password_reset_token(user)
        # Verify token
        assert verify_password_reset_token(user, token) is True
    # Reset password
    response = client.post('/auth/reset-password', json={
        'email': 'test@example.com',
        'token': token,
        'new_password': 'newsecurepass'
    })
    assert response.status_code == 200
    # Verify new password works
    login_response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'newsecurepass'
    })
    assert login_response.status_code == 200