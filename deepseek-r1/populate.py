import os
from dotenv import load_dotenv
from flask import Flask
from model import FlightBooking
from extensions import db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def generate_seats():
    seats = []
    
    # Premium: Fileiras 1-10 (6 assentos cada)
    for row in range(1, 11):
        for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
            seats.append({
                'flight_number': 1,
                'seat': f"{row}{letter}",
                'seat_type': 'Premium'
            })
    
    # Economy Premium: Fileira 11 (4 assentos)
    row = 11
    for letter in ['A', 'B', 'C', 'D']:
        seats.append({
            'flight_number': 1,
            'seat': f"{row}{letter}",
            'seat_type': 'Economy Premium'
        })
    
    # Economy: Fileiras 12-22 (6 assentos cada)
    for row in range(12, 23):
        for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
            seats.append({
                'flight_number': 1,
                'seat': f"{row}{letter}",
                'seat_type': 'Economy'
            })
    
    # Economy Premium: Fileira 23 (4 assentos)
    row = 23
    for letter in ['A', 'B', 'C', 'D']:
        seats.append({
            'flight_number': 1,
            'seat': f"{row}{letter}",
            'seat_type': 'Economy Premium'
        })
    
    # Economy: Fileiras 24-34 (6 assentos cada)
    for row in range(24, 35):
        for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
            seats.append({
                'flight_number': 1,
                'seat': f"{row}{letter}",
                'seat_type': 'Economy'
            })
    
    return seats

def populate_database():
    with app.app_context():
        try:
            # Limpar tabela
            db.session.query(FlightBooking).delete()
            
            # Gerar novos assentos
            seats_data = generate_seats()
            db.session.bulk_insert_mappings(FlightBooking, seats_data)
            
            db.session.commit()
            print(f"✅ Banco populado com {len(seats_data)} assentos!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao popular banco: {str(e)}")

if __name__ == '__main__':
    populate_database()