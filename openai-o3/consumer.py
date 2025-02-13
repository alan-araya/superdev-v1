import threading
import requests
import random
import time

# URL base da API
API_BASE = "http://127.0.0.1:5000"

def consumer(thread_id):
    """
    Função que simula um consumidor virtual.
    Cada consumidor:
      1. Busca os assentos disponíveis.
      2. Tenta reservar primeiro um assento Economy Premium.
      3. Se não houver, randomiza entre Premium e Economy.
      4. Realiza a reserva e finaliza.
    """
    try:
        # Consulta os assentos disponíveis
        response = requests.get(f"{API_BASE}/flight/availability")
        if response.status_code != 200:
            print(f"[Thread {thread_id}] Erro ao buscar assentos disponíveis.")
            return

        available_seats = response.json()
        if not available_seats:
            print(f"[Thread {thread_id}] Nenhum assento disponível.")
            return

        # Filtra os assentos por tipo (convertendo o tipo para minúsculo para comparação)
        economy_premium = [seat for seat in available_seats
                           if seat["seat_type"].lower() in ["economy premium", "economy-premium"]]
        if economy_premium:
            # Se existir algum Economy Premium, seleciona um aleatório
            seat_to_reserve = random.choice(economy_premium)
        else:
            # Se não houver Economy Premium, randomiza entre Premium e Economy
            premium_economy = [seat for seat in available_seats
                               if seat["seat_type"].lower() in ["premium", "economy"]]
            if premium_economy:
                seat_to_reserve = random.choice(premium_economy)
            else:
                print(f"[Thread {thread_id}] Não encontrou assento do tipo Premium ou Economy.")
                return

        # Para a reserva, extrai o valor numérico da propriedade "seat" (ex.: "23A" -> "23")
        # Conforme solicitado, a variável "seat.seat" deve considerar apenas números.
        # Mas, como a API espera a string completa (número e letra) para identificar o assento,
        # utilizamos o valor original para o POST.
        seat_label = seat_to_reserve["seat"]

        # Realiza a chamada POST para reservar o assento
        reserve_response = requests.post(f"{API_BASE}/flight/reserve", json={"seat": seat_label})
        if reserve_response.status_code == 200:
            print(f"[Thread {thread_id}] Reserva bem-sucedida para o assento {seat_label} ({seat_to_reserve['seat_type']}).")
        else:
            print(f"[Thread {thread_id}] Falha ao reservar o assento {seat_label}. Resposta: {reserve_response.text}")
    except Exception as e:
        print(f"[Thread {thread_id}] Exceção: {e}")

def main():
    """
    Função principal que:
      - Verifica se há assentos disponíveis.
      - Cria 10 threads simultâneas (consumidores) para tentar reservas.
      - Repete o processo enquanto existirem assentos livres.
    """
    batch = 1
    while True:
        # Consulta os assentos livres
        try:
            response = requests.get(f"{API_BASE}/flight/availability")
            if response.status_code != 200:
                print("Erro ao consultar assentos disponíveis na API.")
                break
            available_seats = response.json()
        except Exception as e:
            print(f"Erro ao conectar na API: {e}")
            break

        if not available_seats:
            print("Todos os assentos estão reservados. Fim da simulação.")
            break

        print(f"\n--- Iniciando batch {batch} com {min(10, len(available_seats))} consumidores ---")
        threads = []
        # Cria 10 threads (ou menos, se o número de assentos disponíveis for menor)
        num_consumers = min(10, len(available_seats))
        for i in range(num_consumers):
            t = threading.Thread(target=consumer, args=(f"{batch}-{i+1}",))
            t.start()
            threads.append(t)

        # Aguarda todas as threads do batch terminarem
        for t in threads:
            t.join()

        # Aguarda um curto intervalo antes de iniciar um novo batch
        time.sleep(0.5)
        batch += 1

if __name__ == "__main__":
    main()
