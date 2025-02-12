import os
from flask import Flask
from dotenv import load_dotenv
from model import db, FlightBooking

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar a aplicação Flask e o SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy com a aplicação
db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        try:
            # Remove todos os registros existentes na tabela flight_booking
            db.session.query(FlightBooking).delete()
            db.session.commit()
            print("Registros antigos removidos com sucesso.")

            flight_number = 1  # Definindo um número de voo padrão para todos os assentos
            novos_assentos = []

            # -----------------------------------------------------------
            # Bloco 1: Assentos Premium
            # Fileiras 1 a 10 (10 fileiras) com 6 assentos (3 de cada lado: A-F)
            # Exemplo: fileira 1 -> 1A, 1B, 1C, 1D, 1E, 1F
            # -----------------------------------------------------------
            for fileira in range(1, 11):
                for letra in ['A', 'B', 'C', 'D', 'E', 'F']:
                    assento = f"{fileira}{letra}"
                    novo = FlightBooking(
                        flight_number=flight_number,
                        seat=assento,
                        seat_type="Premium",
                        is_free=True
                    )
                    novos_assentos.append(novo)

            # -----------------------------------------------------------
            # Bloco 2: Assentos Economy Premium (primeiro)
            # Fileira 11, com apenas 4 assentos: 11A, 11B, 11C, 11D
            # -----------------------------------------------------------
            fileira = 11
            for letra in ['A', 'B', 'C', 'D']:
                assento = f"{fileira}{letra}"
                novo = FlightBooking(
                    flight_number=flight_number,
                    seat=assento,
                    seat_type="Economy Premium",
                    is_free=True
                )
                novos_assentos.append(novo)

            # -----------------------------------------------------------
            # Bloco 3: Assentos Economy (primeiro)
            # Fileiras 12 a 22 (conforme descrição, fileira 22 inclusa)
            # Cada fileira possui 6 assentos: A, B, C, D, E, F
            # -----------------------------------------------------------
            for fileira in range(12, 23):  # 23 não é incluído, logo 12 a 22
                for letra in ['A', 'B', 'C', 'D', 'E', 'F']:
                    assento = f"{fileira}{letra}"
                    novo = FlightBooking(
                        flight_number=flight_number,
                        seat=assento,
                        seat_type="Economy",
                        is_free=True
                    )
                    novos_assentos.append(novo)

            # -----------------------------------------------------------
            # Bloco 4: Assentos Economy Premium (segundo)
            # Fileira 23, com apenas 4 assentos: 23A, 23B, 23C, 23D
            # -----------------------------------------------------------
            fileira = 23
            for letra in ['A', 'B', 'C', 'D']:
                assento = f"{fileira}{letra}"
                novo = FlightBooking(
                    flight_number=flight_number,
                    seat=assento,
                    seat_type="Economy Premium",
                    is_free=True
                )
                novos_assentos.append(novo)

            # -----------------------------------------------------------
            # Bloco 5: Assentos Economy (segundo)
            # Fileiras 24 a 34 (fileira 34 inclusa)
            # Cada fileira possui 6 assentos: A, B, C, D, E, F
            # -----------------------------------------------------------
            for fileira in range(24, 35):  # 35 não é incluído, logo 24 a 34
                for letra in ['A', 'B', 'C', 'D', 'E', 'F']:
                    assento = f"{fileira}{letra}"
                    novo = FlightBooking(
                        flight_number=flight_number,
                        seat=assento,
                        seat_type="Economy",
                        is_free=True
                    )
                    novos_assentos.append(novo)

            # Insere todos os novos registros de uma vez
            db.session.bulk_save_objects(novos_assentos)
            db.session.commit()
            print("População do banco concluída com sucesso!")

        except Exception as e:
            db.session.rollback()
            print("Erro ao popular o banco de dados:", e)
