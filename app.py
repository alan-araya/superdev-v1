from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
from model import db, FlightBooking
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o CORS
CORS(app)

db.init_app(app)

@app.route('/flight/reserve', methods=['POST'])
def reserve_seat():
    seat = request.json.get('seat')

    if not seat:
        return jsonify({"error": "Assento não informado"}), 400

    try:
        booking = FlightBooking.query.filter_by(seat=seat).first()

        if not booking.is_free:
            return jsonify({"error": "Assento já reservado"}), 400

        booking.is_free = False
        booking.booking_date = datetime.utcnow()

        db.session.commit()

        return jsonify({"message": "Assento reservado com sucesso"}), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Erro ao processar a reserva"}), 500

@app.route('/flight/availability', methods=['GET'])
def get_available_seats():
    seats = FlightBooking.query.filter_by(is_free=True).all()
    return jsonify([seat.to_dict() for seat in seats]), 200

@app.route('/flight/seats', methods=['GET'])
def get_all_seats():
    seats = FlightBooking.query.all()
    return jsonify([seat.to_dict() for seat in seats]), 200

@app.route('/flight', methods=['DELETE'])
def clear_reservations():
    try:
        FlightBooking.query.update({FlightBooking.is_free: True, FlightBooking.booking_date: None})
        db.session.commit()
        return jsonify({"message": "Todas as reservas foram canceladas"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/flight/hc', methods=['GET'])
def health_check():
    return "Hello-World", 200

if __name__ == '__main__':
    app.run(debug=True)
