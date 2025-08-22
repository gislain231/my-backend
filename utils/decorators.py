from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from datetime import datetime
import re

def role_required(*roles):
    """Decorator to require specific user roles"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('roles') and any(role in claims['roles'] for role in roles):
                return fn(*args, **kwargs)
            return jsonify({'message': 'Insufficient permissions'}), 403
        return decorator
    return wrapper

def validate_input(schema):
    """Decorator to validate request input against a schema"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            data = request.get_json()
            errors = {}
            
            for field, rules in schema.items():
                value = data.get(field)
                
                # Check required fields
                if rules.get('required') and not value:
                    errors[field] = 'This field is required'
                    continue
                    
                # Type checking
                if 'type' in rules:
                    if rules['type'] == 'email' and not re.match(r"[^@]+@[^@]+\.[^@]+", str(value)):
                        errors[field] = 'Invalid email format'
                    elif rules['type'] == 'phone' and not re.match(r"^\+?[0-9]{10,15}$", str(value)):
                        errors[field] = 'Invalid phone number'
                    elif rules['type'] == 'datetime':
                        try:
                            datetime.fromisoformat(value)
                        except ValueError:
                            errors[field] = 'Invalid datetime format'
            
            if errors:
                return jsonify({'errors': errors}), 400
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper