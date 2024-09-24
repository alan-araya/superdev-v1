# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa a extensão Flask-CORS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import datetime

from models import db, FlightBooking  # Importa o modelo e o objeto db

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Configura a extensão Flask-CORS para permitir CORS em todas as rotas

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

def seat_sort_key(seat):
    """
    Função para gerar a chave de ordenação para os assentos.
    """
    return (int(seat.seat[:-1]), seat.seat[-1])

@app.route('/flight/availability', methods=['GET'])
def get_available_seats():
    available_seats = FlightBooking.query.filter_by(is_free=True).all()
    sorted_seats = sorted(available_seats, key=seat_sort_key)
    return jsonify([seat.seat for seat in sorted_seats])

@app.route('/flight/seats', methods=['GET'])
def get_all_seats():
    all_seats = FlightBooking.query.all()
    sorted_seats = sorted(all_seats, key=seat_sort_key)
    return jsonify([{'seat': seat.seat, 'is_free': seat.is_free, 'seat_type': seat.seat_type} for seat in sorted_seats])

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
