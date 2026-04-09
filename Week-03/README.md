# Proyecto Semana 03: API de Reservas Hoteleras con Búsqueda Avanzada

## Dominio: Reservas Hoteleras

**Categoría**: Tipos de Habitación (`RoomType`)  
**Entidad principal**: Reservas (`Reservation`)

---

## Objetivo

Construir una **API de catálogo** con búsqueda avanzada y filtros múltiples para el dominio de reservas hoteleras.

---

## Entidades

### RoomType (Tipo de Habitación)

```python
RoomType:
    id: int
    code: str           # "SGL-STD", "DBL-STD", "STE-PRE"...
    name: str           # "Individual Estándar", "Suite Presidencial"...
    description: str
    price_per_night: float
    is_available: bool
```

### Reservation (Reserva)

```python
Reservation:
    id: int
    reservation_code: str   # "RES-2024-001"
    guest_name: str
    hotel_name: str
    room_type_id: int       # FK a RoomType
    check_in_date: str      # "2024-06-15"
    check_out_date: str     # "2024-06-18"
    num_nights: int
    special_requests: str
    is_vip: bool
    status: str             # pending / confirmed / checked_in / cancelled
```

---

## Filtros de búsqueda (8 filtros)

| Filtro | Tipo | Descripción |
|--------|------|-------------|
| `search` | str | Busca en reservation_code, guest_name y special_requests |
| `room_type_id` | int | Filtrar por tipo de habitación |
| `status` | str | pending, confirmed, checked_in, cancelled |
| `hotel_name` | str | Filtrar por nombre del hotel |
| `is_vip` | bool | Solo reservas VIP o no VIP |
| `min_nights` | int | Número mínimo de noches |
| `max_nights` | int | Número máximo de noches |
| `check_in_date` | str | Filtrar por fecha de entrada (búsqueda parcial, ej: `2024-06`) |
| `check_out_date` | str | Filtrar por fecha de salida (búsqueda parcial) |

---

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/room-types/` | Listar tipos de habitación |
| POST | `/room-types/` | Crear tipo de habitación |
| GET | `/room-types/{id}` | Obtener tipo por ID |
| PUT | `/room-types/{id}` | Reemplazar tipo de habitación |
| DELETE | `/room-types/{id}` | Eliminar tipo de habitación |
| GET | `/reservations/` | Listar con filtros avanzados |
| GET | `/reservations/search` | Búsqueda full-text |
| GET | `/reservations/stats` | Estadísticas por tipo de habitación |
| GET | `/reservations/by-room-type/{id}` | Reservas de un tipo de habitación |
| GET | `/reservations/{id}` | Obtener reserva por ID |
| POST | `/reservations/` | Crear reserva |
| PUT | `/reservations/{id}` | Reemplazar reserva |
| PATCH | `/reservations/{id}` | Actualizar parcialmente |
| DELETE | `/reservations/{id}` | Eliminar reserva |

---

## Estructura del proyecto

```
starter/
├── main.py
├── schemas.py
├── database.py
├── dependencies.py
├── routers/
│   ├── room_types.py
│   └── reservations.py
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

---

## Cómo ejecutar

```bash
docker compose up --build
```

Documentación: http://localhost:8000/docs

---

## Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| **Funcionalidad** (40%) | |
| CRUD tipos de habitación + reservas | 15 |
| Filtros funcionan (6+) | 15 |
| Búsqueda y estadísticas | 10 |
| **Adaptación al Dominio** (35%) | |
| Filtros coherentes con el negocio hotelero | 12 |
| Tipos de habitación específicos | 13 |
| Originalidad | 10 |
| **Calidad del Código** (25%) | |
| Schemas de filtros limpios | 10 |
| Query parameters bien tipados | 10 |
| Código limpio | 5 |
| **Total** | **100** |
