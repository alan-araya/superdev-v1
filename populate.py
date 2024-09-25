import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Criar a instância do Flask
app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar a instância do SQLAlchemy
db = SQLAlchemy(app)

# Importar o modelo
from model import FlightBooking

# Função para popular o banco de dados
def populate_database():
    with app.app_context():
        # Deletar todos os registros existentes
        db.session.query(FlightBooking).delete()

        # Listas de assentos
        premium_seats = generate_seat_numbers(range(1, 11), 6)  # Fileiras 1 a 10 com 6 assentos (A-F)
        economy_premium_seats = generate_seat_numbers([11, 23], 4)  # Fileiras 11 e 23 com 4 assentos (A-D)
        economy_seats = generate_seat_numbers(range(12, 23), 6) + generate_seat_numbers(range(24, 35), 6)  # Fileiras 12-22 e 24-34 com 6 assentos (A-F)

        # Inserir assentos Premium
        for seat in premium_seats:
            booking = FlightBooking(flight_number=1, seat=seat, seat_type="Premium", is_free=True)
            db.session.add(booking)

        # Inserir assentos Economy Premium
        for seat in economy_premium_seats:
            booking = FlightBooking(flight_number=1, seat=seat, seat_type="Economy Premium", is_free=True)
            db.session.add(booking)

        # Inserir assentos Economy
        for seat in economy_seats:
            booking = FlightBooking(flight_number=1, seat=seat, seat_type="Economy", is_free=True)
            db.session.add(booking)

        # Commit das inserções
        db.session.commit()
        print("Banco de dados populado com sucesso.")

# Função para gerar números de assento
def generate_seat_numbers(rows, seats_per_row):
    seat_letters = ['A', 'B', 'C', 'D', 'E', 'F']
    seat_list = []
    for row in rows:
        for i in range(seats_per_row):
            seat_list.append(f"{row}{seat_letters[i]}")
    return seat_list

# Executar a função de popular o banco de dados
if __name__ == "__main__":
    populate_database()
