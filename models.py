# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

db = SQLAlchemy()

class FlightBooking(db.Model):
    __tablename__ = 'flight_booking'
    id = db.Column(Integer, primary_key=True)
    flight_number = db.Column(Integer, nullable=False)
    seat = db.Column(String(10), nullable=False, unique=True)
    is_free = db.Column(Boolean, default=True)
    booking_date = db.Column(DateTime)

    def to_dict(self):
        return {
            'flight_number': self.flight_number,
            'seat': self.seat,
            'is_free': self.is_free,
            'booking_date': self.booking_date
        }
