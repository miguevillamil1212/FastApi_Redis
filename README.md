<div align="center">

#  Implementación de Sincronización Distribuida con Redis

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.x-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Repositorio-181717?style=for-the-badge&logo=github&logoColor=white)

**Actividad Integradora — Sistemas Distribuidos**  
Implementación de un lock distribuido funcional usando Redis como coordinador central.

</div>

---

##  Integrantes

| Nombre |
|--------|
|  Esteban Murillo Gomez |
|  Miguel Angel Villamil Echavarria |
|  Rooger Andres Gomez Clavijo |
|  Mauricio Lopez Campiño |

---

##  Descripción

Este proyecto implementa un sistema de **sincronización distribuida** usando **Redis** como mecanismo de lock y **FastAPI** como framework web. El objetivo es demostrar cómo múltiples clientes pueden intentar acceder a un recurso compartido (una cita médica) de forma simultánea, y cómo Redis garantiza que solo uno de ellos logre reservarla, evitando condiciones de carrera (*race conditions*).

---

##  Tecnologías Usadas

| Tecnología | Descripción |
|------------|-------------|
|  **Python 3.11** | Lenguaje principal del proyecto |
|  **FastAPI** | Framework web para construir la API REST |
|  **Redis** | Base de datos en memoria usada como coordinador de locks |
|  **Uvicorn** | Servidor ASGI para correr FastAPI |
|  **GitHub** | Control de versiones y repositorio del proyecto |

---

##  Estructura del Proyecto

```
FastApi_Redis/
├── venv/                    # Entorno virtual de Python
├── testapi.py               # API principal con FastAPI
├── test_concurrencia.py     # Script de prueba de concurrencia
└── test_redis.py            # Prueba básica de conexión con Redis
```

---

##  Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/miguevillamil1212/FastApi_Redis.git
cd FastApi_Redis
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Levantar Redis

```bash
redis-server
```

### 4. Ejecutar la API

```bash
uvicorn test_api:app --reload
```

---

##  Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/crear_cita` | Reserva la cita si está disponible (lock distribuido) |
| `GET` | `/ver_cita` | Consulta el estado actual de la cita y su TTL |
| `DELETE` | `/cancelar_cita` | Libera la cita manualmente |

### Ejemplo de uso con curl

```bash
# Crear cita
curl -X POST http://127.0.0.1:8000/crear_cita

# Ver estado
curl http://127.0.0.1:8000/ver_cita

# Cancelar cita
curl -X DELETE http://127.0.0.1:8000/cancelar_cita
```

---


##  Evidencias

### Explicación breve

El sistema implementa un **lock distribuido** usando el comando `SET nx=True` de Redis. Cuando 20 hilos intentan reservar la cita al mismo tiempo:

- El primero que llega escribe la clave `cita_10am` en Redis con `nx=True` (solo si no existe).
- Los demás encuentran la clave ya existente y reciben `None`, activando el error HTTP 400.
- El parámetro `ex=10` libera automáticamente el lock después de 10 segundos, evitando bloqueos permanentes si el sistema falla.

---

##  Conexión con Sistemas Distribuidos (SSDD)

### ¿Qué problema se resolvió?

Se resolvió el problema de **condición de carrera** (*race condition*) en un entorno distribuido. Sin coordinación, múltiples procesos pueden leer "disponible" al mismo tiempo y todos creerían haber reservado el recurso, generando inconsistencia en los datos. Este es uno de los problemas fundamentales de los Sistemas Distribuidos.

### ¿Cómo actúa Redis como coordinador?

Redis actúa como un **nodo coordinador centralizado** gracias a que sus operaciones son **atómicas**. El comando `SET nx=True` garantiza que aunque lleguen 20 peticiones simultáneamente, solo una puede escribir la clave primero. Esto es posible porque Redis procesa comandos en un **único hilo secuencial**, eliminando los conflictos de escritura simultánea.

| Mecanismo | Función |
|-----------|---------|
| `nx=True` | Solo escribe si la clave **no existe** → lock distribuido |
| `ex=10` | Expiración automática → evita locks eternos ante fallos |
| `r.ttl()` | Consulta el tiempo restante del lock |
| `/cancelar_cita` | Libera el lock manualmente antes de expirar |

> Redis no es solo una base de datos en memoria, es un **árbitro de concurrencia** que decide quién accede primero al recurso compartido, garantizando consistencia en sistemas distribuidos.

---

##  Repositorio

[![GitHub](https://img.shields.io/badge/Ver%20en%20GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/miguevillamil1212/FastApi_Redis.git)

---

<div align="center">
  <sub>Desarrollado con ❤️ — Cotecnova · Sistemas Distribuidos · 2025</sub>
</div>
