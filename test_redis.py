import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r.set("lock_cita", "ocupado", nx=True)

print(r.get("mensaje"))