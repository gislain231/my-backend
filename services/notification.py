from flask import current_app
from models.notification import Notification
from main import db
from threading import Thread
import requests

def send_notification(user_id, title, message, notification_type=None, related_id=None):
    """
    Send in-app notification and trigger other notification methods
    Args:
        user_id: Recipient user ID
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        related_id: ID of related entity
    """
    # Create in-app notification
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        related_id=related_id
    )
    
    db.session.add(notification)
    db.session.commit()
    
    # Trigger push and email notifications in background
    Thread(target=send_push_notification, args=(user_id, title, message)).start()
    Thread(target=send_email_notification, args=(user_id, title, message)).start()

def send_push_notification(user_id, title, message):
    """
    Send push notification to user's device
    Args:
        user_id: Recipient user ID
        title: Notification title
        message: Notification message
    """
    # In a real implementation, this would use FCM/APNs
    # This is a mock implementation
    try:
        user = User.query.get(user_id)
        if not user or not user.push_token:
            return
            
        # Example Firebase Cloud Messaging request
        if current_app.config.get('FCM_API_KEY'):
            headers = {
                'Authorization': f'key={current_app.config["FCM_API_KEY"]}',
                'Content-Type': 'application/json'
            }
            payload = {
                'to': user.push_token,
                'notification': {
                    'title': title,
                    'body': message
                }
            }
            requests.post(
                'https://fcm.googleapis.com/fcm/send',
                headers=headers,
                json=payload
            )
    except Exception as e:
        current_app.logger.error(f"Push notification failed: {str(e)}")

def send_email_notification(user_id, title, message):
    """
    Send email notification to user
    Args:
        user_id: Recipient user ID
        title: Email subject
        message: Email body
    """
    # In a real implementation, this would use Flask-Mail or similar
    # This is a mock implementation
    try:
        user = User.query.get(user_id)
        if not user or not user.email:
            return
            
        if current_app.config.get('MAIL_SERVER'):
            # Example using Flask-Mail (would need proper setup)
            from flask_mail import Message
            mail = current_app.extensions.get('mail')
            if mail:
                msg = Message(
                    subject=title,
                    recipients=[user.email],
                    body=message
                )
                mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Email notification failed: {str(e)}")