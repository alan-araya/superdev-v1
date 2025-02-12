from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
from extensions import db
import os
from model import FlightBooking

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

@app.route('/flight/hc', methods=['GET'])
def health_check():
    return 'Hello-World', 200

@app.route('/flight/reserve', methods=['POST'])
def reserve_seat():
    data = request.get_json()
    if not data or 'seat' not in data:
        return jsonify({'message': 'Parâmetro "seat" não fornecido'}), 400
    
    seat_number = data['seat']
    
    try:
        with db.session.begin():
            seat = FlightBooking.query.filter_by(seat=seat_number).with_for_update().first()
            if not seat:
                return jsonify({'message': f'Assento {seat_number} não encontrado'}), 400
            if not seat.is_free:
                return jsonify({'message': f'Assento {seat_number} já reservado'}), 400
            
            seat.is_free = False
            seat.booking_date = datetime.utcnow()
            db.session.add(seat)
        
        return jsonify(seat.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao reservar assento'}), 500

@app.route('/flight/availability', methods=['GET'])
def get_availability():
    seats = FlightBooking.query.filter_by(is_free=True).all()
    return jsonify([seat.to_dict() for seat in seats]), 200

@app.route('/flight/seats', methods=['GET'])
def get_all_seats():
    seats = FlightBooking.query.all()
    return jsonify([seat.to_dict() for seat in seats]), 200

@app.route('/flight', methods=['DELETE'])
def reset_seats():
    try:
        FlightBooking.query.update({'is_free': True, 'booking_date': None})
        db.session.commit()
        return jsonify({'message': 'Todas as reservas foram resetadas'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao resetar reservas'}), 500

if __name__ == '__main__':
    app.run(debug=True)