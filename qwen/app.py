import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from model import db, FlightBooking

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o aplicativo Flask
app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db.init_app(app)

# Health Check
@app.route('/flight/hc', methods=['GET'])
def health_check():
    return jsonify({"message": "Hello-World"}), 200

# Reservar Assento
@app.route('/flight/reserve', methods=['POST'])
def reserve_seat():
    data = request.get_json()
    seat = data.get('seat')

    if not seat:
        return jsonify({"error": "O campo 'seat' é obrigatório."}), 400

    # Busca o assento no banco de dados
    seat_record = FlightBooking.query.filter_by(seat=seat).with_for_update().first()

    if not seat_record:
        return jsonify({"error": f"Assento '{seat}' não encontrado."}), 404

    if not seat_record.is_free:
        return jsonify({"error": f"Assento '{seat}' já está reservado."}), 400

    # Reserva o assento
    seat_record.is_free = False
    seat_record.booking_date = db.func.now()
    db.session.commit()

    return jsonify({"message": f"Assento '{seat}' reservado com sucesso."}), 200

# Verificar Disponibilidade de Assentos
@app.route('/flight/availability', methods=['GET'])
def get_availability():
    available_seats = FlightBooking.query.filter_by(is_free=True).all()
    return jsonify([seat.to_dict() for seat in available_seats]), 200

# Listar Todos os Assentos
@app.route('/flight/seats', methods=['GET'])
def get_all_seats():
    all_seats = FlightBooking.query.all()
    return jsonify([seat.to_dict() for seat in all_seats]), 200

# Limpar Todas as Reservas
@app.route('/flight', methods=['DELETE'])
def reset_reservations():
    FlightBooking.query.update({"is_free": True, "booking_date": None})
    db.session.commit()
    return jsonify({"message": "Todas as reservas foram limpas."}), 200

# Executa o aplicativo
if __name__ == '__main__':
    app.run(debug=True)