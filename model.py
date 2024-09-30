from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FlightBooking(db.Model):
    __tablename__ = 'flight_booking'
    
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.Integer, nullable=False)
    seat = db.Column(db.String(10), nullable=False, unique=True)
    seat_type = db.Column(db.String(30), nullable=False)
    is_free = db.Column(db.Boolean, default=True)
    booking_date = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'flight_number': self.flight_number,
            'seat': self.seat,
            'seat_type': self.seat_type,
            'is_free': self.is_free,
            'booking_date': self.booking_date
        }
