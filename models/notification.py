from datetime import datetime
from main import db
from utils.translation import translate_field, get_current_lang

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # booking/payment/alert
    related_id = db.Column(db.Integer)  # ID of related entity
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self, lang=None):
        if not lang:
            lang = get_current_lang()

        return {
            'id': self.id,
            'title': translate_field(self.title, lang),
            'message': translate_field(self.message, lang),
            'type': self.notification_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }