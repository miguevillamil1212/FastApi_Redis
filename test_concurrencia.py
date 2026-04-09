import threading
import requests
import time

URL = "http://127.0.0.1:8000/crear_cita"
NUMERO_HILOS = 20

def intentar_reservar(id_hilo):
    time.sleep(1)
    response = requests.post(URL)
    print(f"[Hilo {id_hilo}] Status: {response.status_code} | {response.json()}")

hilos = []
for i in range(1, NUMERO_HILOS + 1):
    t = threading.Thread(target=intentar_reservar, args=(i,))
    hilos.append(t)

for t in hilos:
    t.start()

for t in hilos:
    t.join()