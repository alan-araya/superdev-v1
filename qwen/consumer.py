import threading
import requests
import random
import time

# Configurações
BASE_URL = "http://127.0.0.1:5000"
THREAD_COUNT = 10  # Número de threads simultâneas

# Função para verificar se ainda há assentos disponíveis
def are_seats_available():
    try:
        response = requests.get(f"{BASE_URL}/flight/availability")
        if response.status_code == 200:
            available_seats = response.json()
            return len(available_seats) > 0
        else:
            print("Erro ao verificar disponibilidade de assentos.")
            return False
    except Exception as e:
        print(f"Erro durante a verificação de disponibilidade: {e}")
        return False

# Função para reservar um assento
def reserve_seat():
    while True:
        try:
            # Obtém a lista de assentos livres
            response = requests.get(f"{BASE_URL}/flight/availability")
            if response.status_code != 200:
                print("Erro ao buscar assentos livres.")
                time.sleep(1)
                continue

            available_seats = response.json()

            # Filtra os assentos por tipo
            economy_premium_seats = [seat for seat in available_seats if seat['seat_type'] == 'Economy Premium']
            premium_seats = [seat for seat in available_seats if seat['seat_type'] == 'Premium']
            economy_seats = [seat for seat in available_seats if seat['seat_type'] == 'Economy']

            # Prioriza Economy Premium
            if economy_premium_seats:
                seat_to_reserve = random.choice(economy_premium_seats)
            else:
                # Randomiza entre Premium e Economy
                premium_or_economy = random.choice([premium_seats, economy_seats])
                if not premium_or_economy:
                    break  # Não há mais assentos disponíveis
                seat_to_reserve = random.choice(premium_or_economy)

            # Tenta reservar o assento
            response = requests.post(f"{BASE_URL}/flight/reserve", json={"seat": seat_to_reserve['seat']})
            if response.status_code == 200:
                print(f"Assento reservado: {seat_to_reserve['seat']} (Tipo: {seat_to_reserve['seat_type']})")
                break
            elif response.status_code == 400:
                print(f"Assento já reservado: {seat_to_reserve['seat']}")
            else:
                print(f"Erro ao reservar assento: {seat_to_reserve['seat']}")

        except Exception as e:
            print(f"Erro durante a reserva: {e}")
            time.sleep(1)

# Função principal para iniciar as threads
def main():
    while are_seats_available():
        threads = []
        for _ in range(THREAD_COUNT):
            thread = threading.Thread(target=reserve_seat)
            threads.append(thread)
            thread.start()

        # Aguarda todas as threads terminarem antes de iniciar o próximo ciclo
        for thread in threads:
            thread.join()

    print("Todos os assentos foram reservados.")

if __name__ == "__main__":
    main()