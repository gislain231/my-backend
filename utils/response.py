from flask import jsonify
from typing import Any, Dict, List, Optional

def success_response(data: Any = None, 
                    message: str = 'Success', 
                    status_code: int = 200) -> Dict:
    """Standard success response format"""
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def error_response(message: str = 'Error', 
                  errors: Optional[Dict] = None, 
                  status_code: int = 400) -> Dict:
    """Standard error response format"""
    response = {
        'success': False,
        'message': message,
        'errors': errors or {}
    }
    return jsonify(response), status_code

def paginated_response(items: List, 
                      page: int, 
                      per_page: int, 
                      total: int) -> Dict:
    """Standard paginated response format"""
    return success_response({
        'items': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    })