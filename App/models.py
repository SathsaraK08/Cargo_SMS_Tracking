from extensions import db
from datetime import datetime

# This model represents a cargo package in the system
class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.String(50), unique=True, nullable=False)
    sender_name = db.Column(db.String(100), nullable=False)
    receiver_name = db.Column(db.String(100), nullable=False)
    phone_sender = db.Column(db.String(15), nullable=False)
    phone_receiver = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(50), default="Registered")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Package {self.tracking_id}>"