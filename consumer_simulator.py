import requests
import threading
import random
import time

# URL da API para buscar e reservar assentos
GET_SEATS_URL = 'http://127.0.0.1:5000/flight/seats'
RESERVE_SEAT_URL = 'http://127.0.0.1:5000/flight/reserve'

# Número de consumidores configurável
NUM_CONSUMERS = 3
THREAD_DELAY = 0.5  # Pequeno atraso entre o início de cada thread para simular concorrência

# Função para buscar assentos livres
def get_free_seats():
    try:
        response = requests.get(GET_SEATS_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao buscar assentos: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return []

# Função para reservar um assento
def reserve_seat(seat_id):
    try:
        response = requests.post(RESERVE_SEAT_URL, json={'seat': seat_id})
        if response.status_code == 200:
            print(f"Assento {seat_id} reservado com sucesso!")
            return True
        else:
            print(f"Erro ao reservar assento {seat_id}: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao reservar assento {seat_id}: {e}")
        return False

# Função que simula o comportamento de um consumidor
def consumer_behavior():
    while True:
        free_seats = get_free_seats()

        if not free_seats:
            print("Todos os assentos estão reservados ou não há assentos disponíveis.")
            break

        # Priorizar assentos do tipo "Economy Premium"
        economy_premium_seats = [seat for seat in free_seats if seat['seat_type'] == "Economy Premium" and seat['is_free']]
        if economy_premium_seats:
            seat_to_reserve = economy_premium_seats[0]
            reserve_seat(seat_to_reserve['seat'])

        # Se não houver "Economy Premium", randomizar entre "Premium" e "Economy"
        other_seats = [seat for seat in free_seats if seat['seat_type'] in ["Premium", "Economy"] and seat['is_free']]
        if other_seats:
            seat_to_reserve = random.choice(other_seats)
            reserve_seat(seat_to_reserve['seat'])
        
        time.sleep(0.3) 
            


# Função para iniciar consumidores simulados
def start_consumers(num_consumers):
    threads = []
    for i in range(num_consumers):
        t = threading.Thread(target=consumer_behavior)
        threads.append(t)
        t.start()
        time.sleep(THREAD_DELAY)  # Pequeno atraso entre o início de cada consumidor

    # Aguardar que todas as threads sejam concluídas
    for t in threads:
        t.join()


start_consumers(NUM_CONSUMERS)