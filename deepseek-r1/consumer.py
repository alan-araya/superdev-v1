import requests
import threading
import random
import time

# Configurações
BASE_URL = "http://127.0.0.1:5000/flight"
CONCURRENT_CONSUMERS = 10
SEAT_TYPES = ["Premium", "Economy"]
stop_event = threading.Event()

class Consumer(threading.Thread):
    def __init__(self, consumer_id):
        super().__init__()
        self.consumer_id = consumer_id
        
    def get_available_seats(self):
        try:
            response = requests.get(f"{BASE_URL}/availability", timeout=5)
            return response.json() if response.status_code == 200 else []
        except:
            return []

    def reserve_seat(self, seat_number):
        try:
            response = requests.post(
                f"{BASE_URL}/reserve",
                json={"seat": seat_number},
                timeout=5
            )
            return response.status_code
        except:
            return 500

    def run(self):
        while not stop_event.is_set():
            # Obter assentos disponíveis
            available_seats = self.get_available_seats()
            if not available_seats:
                stop_event.set()
                break

            # Aguarda um curto intervalo antes de iniciar um novo batch
            time.sleep(0.3)
            
            # Priorizar Economy Premium
            economy_premium = [s for s in available_seats if s["seat_type"] == "Economy Premium"]
            if economy_premium:
                seat = random.choice(economy_premium)
            else:
                # Escolher aleatoriamente entre Premium/Economy
                chosen_type = random.choice(SEAT_TYPES)
                filtered_seats = [s for s in available_seats if s["seat_type"] == chosen_type]
                if not filtered_seats: continue
                seat = random.choice(filtered_seats)

            # Tentar reservar
            status = self.reserve_seat(seat["seat"])
            if status == 200:
                print(f"✅ [Consumidor {self.consumer_id}] Reservou {seat['seat']} ({seat['seat_type']})")
            elif status == 400:
                time.sleep(0.1)  # Backoff para conflitos
            else:
                time.sleep(1)

def check_completion():
    while not stop_event.is_set():
        response = requests.get(f"{BASE_URL}/seats")
        if all(not seat["is_free"] for seat in response.json()):
            stop_event.set()
            print("\n🎉 Todos os assentos foram reservados!")
            break
        time.sleep(1)

if __name__ == "__main__":
    # Resetar assentos (opcional)
    # requests.delete(f"{BASE_URL}")

    # Iniciar monitor de conclusão
    threading.Thread(target=check_completion, daemon=True).start()

    # Iniciar consumidores
    print(f"🚀 Iniciando {CONCURRENT_CONSUMERS} consumidores...")
    consumers = [Consumer(i+1) for i in range(CONCURRENT_CONSUMERS)]
    
    for c in consumers:
        c.start()
    
    for c in consumers:
        c.join()