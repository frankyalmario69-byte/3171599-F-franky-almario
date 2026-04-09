# API de Gestión de Reservas Hoteleras

Proyecto Semana 02 - Bootcamp

## Descripción
Este proyecto es una API REST para gestionar reservas hoteleras.  
Se construyó con **FastAPI** y **Pydantic v2**, y se ejecuta en **Docker**.

## Tecnologías
- Python 3.14
- FastAPI
- Pydantic
- Docker / Docker Compose
- Uvicorn

## Cómo ejecutar
1. Clonar el repositorio.
2. Construir y levantar el contenedor:
   ```bash
   docker compose up --build
   ```
3. Abrir la documentación en el navegador:
   http://localhost:8000/docs

---

## Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/reservations` | Crear reserva |
| GET | `/reservations` | Listar reservas (con filtro por estado) |
| GET | `/reservations/{id}` | Obtener reserva por ID |
| GET | `/reservations/code/{reservation_code}` | Buscar por código de reserva |
| PATCH | `/reservations/{id}` | Actualizar reserva parcialmente |
| DELETE | `/reservations/{id}` | Eliminar reserva |

---

## Ejemplo de reserva

```json
{
  "reservation_code": "HR12345678",
  "guest_name": "Carlos Pérez",
  "hotel_name": "Hotel Grand Plaza",
  "room_type": "Doble Estándar",
  "city": "Cartagena",
  "num_nights": 3,
  "status": "pending",
  "is_vip": false
}
```

## Estados de una reserva

| Estado | Descripción |
|--------|-------------|
| `pending` | Registrada, pendiente de confirmación |
| `confirmed` | Confirmada |
| `checked_in` | Huésped en el hotel |
| `cancelled` | Cancelada |

## Formato del código de reserva

El `reservation_code` debe seguir el formato: **2 letras mayúsculas + 8 dígitos**  
Ejemplo: `HR12345678`, `RV20240915`
