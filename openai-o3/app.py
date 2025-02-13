import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # Suporte para CORS

# Configurar conexão com o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Importar o modelo e inicializar o SQLAlchemy com a aplicação
from model import db, FlightBooking
db.init_app(app)

# -------------------------------
# Endpoint de Health Check
# -------------------------------
@app.route("/flight/hc", methods=["GET"])
def health_check():
    return "Hello-World", 200

# -------------------------------
# Endpoint para reservar um assento
# -------------------------------
@app.route("/flight/reserve", methods=["POST"])
def reserve_seat():
    data = request.get_json()
    if not data or "seat" not in data:
        return jsonify({"erro": "Parâmetro 'seat' é obrigatório."}), 400

    seat_param = data["seat"]

    try:
        # Inicia uma transação e bloqueia a linha para tratar a concorrência
        seat_obj = db.session.query(FlightBooking).filter_by(seat=seat_param).with_for_update().first()
        if not seat_obj:
            return jsonify({"erro": f"Assento '{seat_param}' não encontrado."}), 400

        if not seat_obj.is_free:
            return jsonify({"erro": f"Assento '{seat_param}' já está reservado."}), 400

        # Realiza a reserva
        seat_obj.is_free = False
        seat_obj.booking_date = datetime.utcnow()
        db.session.commit()
        return jsonify({"mensagem": f"Assento '{seat_param}' reservado com sucesso."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao processar a reserva."}), 500

# -------------------------------
# Endpoint para retornar todos os assentos livres
# -------------------------------
@app.route("/flight/availability", methods=["GET"])
def available_seats():
    try:
        assentos = FlightBooking.query.filter_by(is_free=True).order_by(
            db.cast(db.func.regexp_replace(FlightBooking.seat, '[^0-9]', ''), db.Integer),
            FlightBooking.seat
        ).all()
        return jsonify([assento.to_dict() for assento in assentos]), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao recuperar os assentos disponíveis."}), 500

# -------------------------------
# Endpoint para retornar todos os assentos do voo
# -------------------------------
@app.route("/flight/seats", methods=["GET"])
def all_seats():
    try:
        assentos = FlightBooking.query.order_by(
            db.cast(db.func.regexp_replace(FlightBooking.seat, '[^0-9]', ''), db.Integer),
            FlightBooking.seat
        ).all()
        return jsonify([assento.to_dict() for assento in assentos]), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao recuperar os assentos."}), 500

# -------------------------------
# Endpoint para resetar as reservas do voo
# -------------------------------
@app.route("/flight", methods=["DELETE"])
def reset_flight():
    try:
        seats = FlightBooking.query.all()
        for seat in seats:
            seat.is_free = True
            seat.booking_date = None
        db.session.commit()
        return jsonify({"mensagem": "Todas as reservas foram removidas e os assentos resetados para livres."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao resetar as reservas."}), 500

if __name__ == "__main__":
    app.run(debug=True)
