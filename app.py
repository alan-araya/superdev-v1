from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importa a extensão CORS
from dotenv import load_dotenv
import os
from datetime import datetime
from model import db, FlightBooking  # Importa o modelo e o objeto db

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o objeto db com as configurações do app
db.init_app(app)

# Configura o CORS para permitir todas as origens
CORS(app)

@app.route('/flight/reserve', methods=['POST'])
def reserve_seat():
    data = request.get_json()
    seat = data.get('seat')

    if not seat:
        return jsonify({'error': 'Parâmetro "seat" é obrigatório'}), 400

    try:
        # Verificar se o assento está disponível
        booking = FlightBooking.query.filter_by(seat=seat).with_for_update().first()

        if not booking:
            return jsonify({'error': 'Assento não encontrado'}), 404
        
        if not booking.is_free:
            return jsonify({'error': 'Assento já reservado'}), 400

        # Atualizar o assento como reservado
        booking.is_free = False
        booking.booking_date = datetime.now()
        db.session.commit()

        return jsonify({'message': 'Assento reservado com sucesso'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/flight/availability', methods=['GET'])
def get_available_seats():
    try:
        available_seats = FlightBooking.query.filter_by(is_free=True).all()
        return jsonify([seat.to_dict() for seat in available_seats]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/flight/seats', methods=['GET'])
def get_all_seats():
    try:
        all_seats = FlightBooking.query.all()
        return jsonify([seat.to_dict() for seat in all_seats]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/flight', methods=['DELETE'])
def clear_reservations():
    try:
        FlightBooking.query.update({FlightBooking.is_free: True, FlightBooking.booking_date: None})
        db.session.commit()
        return jsonify({'message': 'Todas as reservas foram limpas'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/flight/hc', methods=['GET'])
def health_check():
    return jsonify({'message': 'Hello-World'}), 200


if __name__ == '__main__':
    app.run(debug=True)
