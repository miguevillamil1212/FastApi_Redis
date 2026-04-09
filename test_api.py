from fastapi import FastAPI, HTTPException
import redis

app = FastAPI()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.post("/crear_cita")
def crear_cita():
    lock = r.set("cita_10am", "ocupado", nx=True, ex=10)
    if not lock:
        raise HTTPException(status_code=400, detail="Cita ya ocupada")
    return {"mensaje": "Cita reservada correctamente"}

@app.get("/ver_cita")
def ver_cita():
    cita = r.get("cita_10am")
    ttl = r.ttl("cita_10am")
    if not cita:
        return {"estado": "disponible"}
    return {"estado": cita, "ttl_segundos": ttl}

@app.delete("/cancelar_cita")
def cancelar_cita():
    cita = r.get("cita_10am")
    if not cita:
        raise HTTPException(status_code=404, detail="No hay cita activa")
    r.delete("cita_10am")
    return {"mensaje": "Cita cancelada correctamente"}