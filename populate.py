# populate.py
from flask import Flask
from dotenv import load_dotenv
import os

from models import db, FlightBooking  # Importa o modelo e o objeto db

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializa o objeto db com o aplicativo Flask

def populate_seats():
    with app.app_context():
        db.create_all()  # Cria as tabelas se não existirem

        if FlightBooking.query.first():
            print("Os assentos já foram populados.")
            return

        # Assentos Premium (Fileiras 1 a 10)
        for row in range(1, 11):
            for seat_letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                seat = FlightBooking(
                    flight_number=1,
                    seat=f"{row}{seat_letter}",
                    is_free=True
                )
                db.session.add(seat)
        # Assentos Economy Premium (Fileiras 11 e 23)
        for row in [11, 23]:
            for seat_letter in ['A', 'B', 'C', 'D']:
                seat = FlightBooking(
                    flight_number=1,
                    seat=f"{row}{seat_letter}",
                    is_free=True
                )
                db.session.add(seat)
        # Assentos Economy (Fileiras 12 a 22 e 24 a 34)
        for row in list(range(12, 23)) + list(range(24, 35)):
            for seat_letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                seat = FlightBooking(
                    flight_number=1,
                    seat=f"{row}{seat_letter}",
                    is_free=True
                )
                db.session.add(seat)
        db.session.commit()
        print("Assentos iniciais populados com sucesso.")

if __name__ == '__main__':
    populate_seats()
