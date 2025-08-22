import stripe
from flask import current_app
from models.payment import Payment
from models.booking import Booking
from main import db
from datetime import datetime

def process_payment(booking_id, payment_method_id, amount):
    """
    Process a payment for a booking using Stripe
    """
    try:
        # Get the booking
        booking = Booking.query.get(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        
        # Set up Stripe
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency='usd',
            payment_method=payment_method_id,
            confirm=True,
            return_url=current_app.config.get('STRIPE_RETURN_URL', 'http://localhost:3000/payment-success')
        )
        
        # Create payment record
        payment = Payment(
            booking_id=booking_id,
            amount=amount,
            currency='usd',
            payment_method='stripe',
            stripe_payment_intent_id=intent.id,
            status='completed' if intent.status == 'succeeded' else 'pending'
        )
        
        db.session.add(payment)
        
        # Update booking status
        if intent.status == 'succeeded':
            booking.status = 'paid'
            booking.payment_status = 'completed'
        
        db.session.commit()
        
        return {
            'success': True,
            'payment_id': payment.id,
            'stripe_intent_id': intent.id,
            'status': intent.status
        }
        
    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def refund_payment(payment_id, amount=None):
    """
    Process a refund for a payment
    """
    try:
        payment = Payment.query.get(payment_id)
        if not payment:
            raise ValueError("Payment not found")
        
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        
        # Create refund
        refund_amount = int((amount or payment.amount) * 100)
        refund = stripe.Refund.create(
            payment_intent=payment.stripe_payment_intent_id,
            amount=refund_amount
        )
        
        # Update payment status
        payment.status = 'refunded'
        payment.refunded_at = datetime.utcnow()
        
        db.session.commit()
        
        return {
            'success': True,
            'refund_id': refund.id,
            'amount': refund_amount / 100
        }
        
    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_payment_status(payment_id):
    """
    Get the current status of a payment
    """
    payment = Payment.query.get(payment_id)
    if not payment:
        return None
    
    return {
        'id': payment.id,
        'amount': payment.amount,
        'currency': payment.currency,
        'status': payment.status,
        'created_at': payment.created_at.isoformat() if payment.created_at else None,
        'stripe_payment_intent_id': payment.stripe_payment_intent_id
    } 