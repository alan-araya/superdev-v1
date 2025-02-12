import os
from dotenv import load_dotenv
from model import db, FlightBooking
from app import app

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def populate_database():
    with app.app_context():
        # Deleta todos os registros existentes na tabela
        db.session.query(FlightBooking).delete()
        db.session.commit()

        # Função auxiliar para gerar assentos
        def generate_seats(start_row, end_row, seat_letters, seat_type):
            seats = []
            for row in range(start_row, end_row + 1):
                for letter in seat_letters:
                    seat = f"{row}{letter}"
                    seats.append(
                        FlightBooking(
                            flight_number=100,
                            seat=seat,
                            seat_type=seat_type,
                            is_free=True
                        )
                    )
            return seats

        # Gera assentos Premium (fileiras 1 a 10)
        premium_seats = generate_seats(1, 10, ['A', 'B', 'C', 'D', 'E', 'F'], 'Premium')

        # Gera assentos Economy Premium (fileira 11)
        economy_premium_1 = generate_seats(11, 11, ['A', 'B', 'C', 'D'], 'Economy Premium')

        # Gera assentos Economy (fileiras 12 a 22)
        economy_seats_1 = generate_seats(12, 22, ['A', 'B', 'C', 'D', 'E', 'F'], 'Economy')

        # Gera assentos Economy Premium (fileira 23)
        economy_premium_2 = generate_seats(23, 23, ['A', 'B', 'C', 'D'], 'Economy Premium')

        # Gera assentos Economy (fileiras 24 a 34)
        economy_seats_2 = generate_seats(24, 34, ['A', 'B', 'C', 'D', 'E', 'F'], 'Economy')

        # Combina todos os assentos
        all_seats = (
            premium_seats +
            economy_premium_1 +
            economy_seats_1 +
            economy_premium_2 +
            economy_seats_2
        )

        # Insere todos os assentos no banco de dados
        db.session.add_all(all_seats)
        db.session.commit()

        print(f"Total de assentos inseridos: {len(all_seats)}")

if __name__ == '__main__':
    populate_database()