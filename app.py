from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
import datetime

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Base = declarative_base()

# Modelo da entidade FlightBooking
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

# Endpoint de Health Check
@app.route('/flight/hc', methods=['GET'])
def health_check():
    return "Hello-World", 200

# Endpoint para reservar um assento
@app.route('/flight/booking', methods=['POST'])
def book_seat():
    seat_number = request.json.get('seat')
    if not seat_number:
        return jsonify({'message': 'Parâmetro "seat" é obrigatório.'}), 400

    try:
        # Inicia uma transação
        with db.session.begin_nested():
            # Bloqueia o registro para evitar condições de corrida
            seat = db.session.query(FlightBooking).with_for_update().filter_by(seat=seat_number).first()
            if not seat:
                return jsonify({'message': 'Assento não encontrado.'}), 404
            if not seat.is_free:
                return jsonify({'message': 'Assento já está reservado.'}), 400
            seat.is_free = False
            seat.booking_date = datetime.datetime.now()
            db.session.commit()
        return jsonify({'message': 'Assento reservado com sucesso.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao reservar o assento.', 'error': str(e)}), 500

# Endpoint para obter todos os assentos livres
@app.route('/flight/availability', methods=['GET'])
def get_available_seats():
    seats = FlightBooking.query.filter_by(is_free=True).all()
    seats_list = [seat.to_dict() for seat in seats]
    return jsonify(seats_list), 200

# Endpoint para obter todos os assentos e seus status
@app.route('/flight/seats', methods=['GET'])
def get_all_seats():
    seats = FlightBooking.query.all()
    seats_list = [seat.to_dict() for seat in seats]
    return jsonify(seats_list), 200

# Endpoint para limpar todas as reservas
@app.route('/flight', methods=['DELETE'])
def reset_seats():
    try:
        FlightBooking.query.update({FlightBooking.is_free: True, FlightBooking.booking_date: None})
        db.session.commit()
        return jsonify({'message': 'Todas as reservas foram resetadas.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao resetar as reservas.', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
