# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa a função CORS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import datetime
import re

from models import db, FlightBooking  # Importa o modelo e o objeto db

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Configura o suporte a CORS

# Configuração do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializa o objeto db com o aplicativo Flask

# Endpoint de Health Check
@app.route('/flight/hc', methods=['GET'])
def health_check():
    return "Hello-World", 200

# Endpoint para reservar um assento
@app.route('/flight/reserve', methods=['POST'])
def book_seat():
    seat = request.json.get('seat')
    if not seat:
        return jsonify({'message': 'Número do assento é obrigatório.'}), 400
    try:
        seat = FlightBooking.query.filter_by(seat=seat).first()
        if not seat:
            return jsonify({'message': 'Assento não encontrado.'}), 404
        if not seat.is_free:
            return jsonify({'message': 'Assento já está reservado.'}), 400
        seat.is_free = False
        seat.booking_date = datetime.datetime.now()
        db.session.commit()
        return jsonify({'message': 'Assento reservado com sucesso.'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Erro ao reservar o assento.'}), 500

def sort_seats(seat):
    match = re.match(r"(\d+)([A-Z])", seat.seat)
    if match:
        return int(match.group(1)), match.group(2)
    return 0, ""

# Endpoint para obter todos os assentos
@app.route('/flight/seats', methods=['GET'])
def get_all_seats():
    seats = FlightBooking.query.all()
    seats_sorted = sorted(seats, key=sort_seats)
    seats_list = [seat.to_dict() for seat in seats_sorted]
    return jsonify(seats_list), 200

@app.route('/flight/availability', methods=['GET'])
def get_available_seats():
    seats = FlightBooking.query.filter_by(is_free=True).all()
    seats_sorted = sorted(seats, key=sort_seats)
    seats_list = [seat.to_dict() for seat in seats_sorted]
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
