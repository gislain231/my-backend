from flask_mail import Message, Mail
from flask import current_app
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail = Mail()
        mail.init_app(app)
        mail.send(msg)

def send_password_reset_email(email, reset_link):
    msg = Message(
        subject='Password Reset Request',
        recipients=[email],
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    msg.body = f'''To reset your password, visit the following link:
{reset_link}

This link will expire in 1 hour.

If you did not make this request, please ignore this email.
'''
    # Send email in background
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()