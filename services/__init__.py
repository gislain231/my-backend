
from .auth import AuthService
from .carsharing import (
    find_available_vehicles,
    calculate_booking_price,
    create_carsharing_booking
)
from .detailing import (
    find_available_providers,
    create_detailing_booking
)
from .payment import (
    process_payment,
    refund_payment,
    get_payment_status
)
from .notification import (
    send_notification,
    send_push_notification,
    send_email_notification
)

# Group related services for cleaner imports
class CarsharingService:
    find_available = find_available_vehicles
    calculate_price = calculate_booking_price
    create_booking = create_carsharing_booking

class DetailingService:
    find_providers = find_available_providers
    create_booking = create_detailing_booking

class PaymentService:
    process = process_payment
    refund = refund_payment
    get_status = get_payment_status

class NotificationService:
    send = send_notification
    send_push = send_push_notification
    send_email = send_email_notification

__all__ = [
    # Auth
    'AuthService',
    
    # Service Groups
    'CarsharingService',
    'DetailingService',
    'PaymentService',
    'NotificationService',
    
    # Individual functions
    'find_available_vehicles',
    'calculate_booking_price',
    'create_carsharing_booking',
    'find_available_providers',
    'create_detailing_booking',
    'process_payment',
    'refund_payment',
    'get_payment_status',
    'send_notification',
    'send_push_notification',
    'send_email_notification'
]