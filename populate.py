from model import db, FlightBooking
from flask import Flask
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def populate_database():
    # Deleta todos os registros antes de popular
    with app.app_context():
        db.session.query(FlightBooking).delete()
        db.session.commit()

        # Função para gerar assentos
        def generate_seats(start_row, end_row, seat_letters, seat_type):
            for row in range(start_row, end_row + 1):
                for letter in seat_letters:
                    seat = f"{row}{letter}"
                    new_seat = FlightBooking(
                        flight_number=123,  # Altere conforme necessário
                        seat=seat,
                        seat_type=seat_type,
                        is_free=True
                    )
                    db.session.add(new_seat)

        # 10 Assentos Premium (Fileiras 1 a 10, 6 assentos por fileira)
        generate_seats(1, 10, ['A', 'B', 'C', 'D', 'E', 'F'], 'Premium')

        # 4 Assentos Economy Premium (Fileira 11, 4 assentos)
        generate_seats(11, 11, ['A', 'B', 'C', 'D'], 'Economy Premium')

        # 10 Assentos Economy (Fileiras 12 a 22, 6 assentos por fileira)
        generate_seats(12, 22, ['A', 'B', 'C', 'D', 'E', 'F'], 'Economy')

        # 4 Assentos Economy Premium (Fileira 23, 4 assentos)
        generate_seats(23, 23, ['A', 'B', 'C', 'D'], 'Economy Premium')

        # 10 Assentos Economy (Fileiras 24 a 34, 6 assentos por fileira)
        generate_seats(24, 34, ['A', 'B', 'C', 'D', 'E', 'F'], 'Economy')

        # Commit para salvar os dados
        db.session.commit()

        print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    populate_database()
