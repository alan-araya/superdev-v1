import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
from model import db, FlightBooking  # Importa o modelo e o objeto db
from flask_cors import CORS

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar a aplicação com o banco de dados
db.init_app(app)

# Permitir CORS para todos os domínios e rotas
CORS(app)

# Método para reservar um assento
@app.route('/flight/reserve', methods=['POST'])
def reserve_seat():
    data = request.get_json()
    seat = data.get('seat')

    if not seat:
        return jsonify({'error': 'Assento não especificado'}), 400

    try:
        booking = db.session.query(FlightBooking).filter_by(seat=seat).with_for_update().first()

        if not booking:
            return jsonify({'error': 'Assento não encontrado'}), 404

        if not booking.is_free:
            return jsonify({'error': 'Assento já reservado'}), 400

        booking.is_free = False
        booking.booking_date = datetime.now()
        db.session.commit()

        return jsonify({'message': 'Assento reservado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao reservar assento: {}'.format(str(e))}), 500

# Método para obter disponibilidade de assentos
@app.route('/flight/availability', methods=['GET'])
def get_available_seats():
    seats = FlightBooking.query.filter_by(is_free=True).all()
    available_seats = [seat.to_dict() for seat in seats]
    return jsonify(available_seats), 200

# Método para obter todos os assentos
@app.route('/flight/seats', methods=['GET'])
def get_all_seats():
    seats = FlightBooking.query.all()
    all_seats = [seat.to_dict() for seat in seats]
    return jsonify(all_seats), 200

# Método para limpar todas as reservas
@app.route('/flight', methods=['DELETE'])
def clear_reservations():
    try:
        db.session.query(FlightBooking).update({'is_free': True, 'booking_date': None})
        db.session.commit()
        return jsonify({'message': 'Todas as reservas foram removidas'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao limpar reservas: {}'.format(str(e))}), 500

# Método de health check
@app.route('/flight/hc', methods=['GET'])
def health_check():
    return "Hello-World", 200

if __name__ == '__main__':
    app.run(debug=True)
