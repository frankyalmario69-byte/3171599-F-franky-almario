"""
Router de Reservas
==================

CRUD con filtrado avanzado, paginación y ordenamiento
para el sistema de reservas hoteleras.
"""

from fastapi import APIRouter, Path, HTTPException, status
from datetime import datetime
from math import ceil

from database import reservations_db, room_types_db, get_next_reservation_id
from schemas import ReservationCreate, ReservationUpdate, ReservationResponse, SortOrder
from dependencies import PaginationDep, ReservationFiltersDep, SortingDep

router = APIRouter(
    prefix="/reservations",
    tags=["Reservas"],
    responses={404: {"description": "Reserva no encontrada"}}
)


# ============================================
# HELPER: Enriquecer reserva con datos del tipo de habitación
# ============================================

def enrich_reservation(res: dict) -> dict:
    """Añade el objeto room_type al dict de la reserva."""
    result = dict(res)
    result["room_type"] = room_types_db.get(res["room_type_id"])
    return result


# ============================================
# GET /reservations - Listar con filtros avanzados
# ============================================

@router.get("/")
async def list_reservations(
    pagination: PaginationDep,
    filters: ReservationFiltersDep,
    sorting: SortingDep
):
    """
    Listar reservas con filtrado avanzado, paginación y ordenamiento.

    **Filtros disponibles:**
    - `search` → busca en reservation_code, guest_name y special_requests
    - `room_type_id` → filtra por tipo de habitación
    - `status` → estado (pending, confirmed, checked_in, cancelled)
    - `hotel_name` → nombre del hotel (búsqueda parcial)
    - `is_vip` → reservas VIP o no VIP
    - `min_nights` / `max_nights` → rango de noches
    - `check_in_date` → fecha de entrada (búsqueda parcial, ej: 2024-06)
    - `check_out_date` → fecha de salida (búsqueda parcial, ej: 2024-07)
    """
    items = list(reservations_db.values())

    # --- Filtro: búsqueda en texto ---
    if filters.search:
        term = filters.search.lower()
        items = [
            r for r in items
            if term in r["reservation_code"].lower()
            or term in r["guest_name"].lower()
            or term in (r.get("special_requests") or "").lower()
        ]

    # --- Filtro: tipo de habitación ---
    if filters.room_type_id is not None:
        items = [r for r in items if r["room_type_id"] == filters.room_type_id]

    # --- Filtro: estado ---
    if filters.status is not None:
        items = [r for r in items if r["status"] == filters.status.value]

    # --- Filtro: hotel ---
    if filters.hotel_name:
        term = filters.hotel_name.lower()
        items = [r for r in items if term in r["hotel_name"].lower()]

    # --- Filtro: VIP ---
    if filters.is_vip is not None:
        items = [r for r in items if r["is_vip"] == filters.is_vip]

    # --- Filtro: noches mínimas ---
    if filters.min_nights is not None:
        items = [r for r in items if r["num_nights"] >= filters.min_nights]

    # --- Filtro: noches máximas ---
    if filters.max_nights is not None:
        items = [r for r in items if r["num_nights"] <= filters.max_nights]

    # --- Filtro: fecha de entrada ---
    if filters.check_in_date:
        term = filters.check_in_date.lower()
        items = [r for r in items if term in r["check_in_date"].lower()]

    # --- Filtro: fecha de salida ---
    if filters.check_out_date:
        term = filters.check_out_date.lower()
        items = [r for r in items if term in r["check_out_date"].lower()]

    # --- Ordenamiento ---
    reverse = sorting.order == SortOrder.desc
    items = sorted(items, key=lambda r: r.get(sorting.sort_by.value, ""), reverse=reverse)

    # --- Paginación ---
    total = len(items)
    pages = ceil(total / pagination.per_page) if total > 0 else 1
    paginated = items[pagination.offset: pagination.offset + pagination.per_page]

    return {
        "items": [enrich_reservation(r) for r in paginated],
        "total": total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pages,
        "has_next": pagination.page < pages,
        "has_prev": pagination.page > 1
    }


# ============================================
# GET /reservations/search - Búsqueda full-text
# ============================================

@router.get("/search")
async def search_reservations(q: str):
    """
    Búsqueda full-text en todos los campos de texto de la reserva.
    """
    if len(q) < 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El término de búsqueda debe tener al menos 2 caracteres"
        )
    term = q.lower()
    results = [
        enrich_reservation(r) for r in reservations_db.values()
        if term in r["reservation_code"].lower()
        or term in r["guest_name"].lower()
        or term in r["hotel_name"].lower()
        or term in (r.get("special_requests") or "").lower()
        or term in r["check_in_date"].lower()
        or term in r["check_out_date"].lower()
    ]
    return {"query": q, "total": len(results), "items": results}


# ============================================
# GET /reservations/stats - Estadísticas por tipo de habitación
# ============================================

@router.get("/stats")
async def reservation_stats():
    """
    Estadísticas de reservas agrupadas por tipo de habitación.
    Incluye conteo por estado, promedio de noches y noches totales.
    """
    stats = {}

    for res in reservations_db.values():
        room_type_id = res["room_type_id"]
        room_type = room_types_db.get(room_type_id)
        room_type_name = room_type["name"] if room_type else f"Tipo {room_type_id}"

        if room_type_id not in stats:
            stats[room_type_id] = {
                "room_type_id": room_type_id,
                "room_type_name": room_type_name,
                "total_reservations": 0,
                "total_nights": 0,
                "by_status": {
                    "pending": 0,
                    "confirmed": 0,
                    "checked_in": 0,
                    "cancelled": 0
                }
            }

        stats[room_type_id]["total_reservations"] += 1
        stats[room_type_id]["total_nights"] += res["num_nights"]
        stats[room_type_id]["by_status"][res["status"]] += 1

    # Calcular promedio de noches
    for s in stats.values():
        if s["total_reservations"] > 0:
            s["avg_nights"] = round(s["total_nights"] / s["total_reservations"], 1)
        else:
            s["avg_nights"] = 0.0

    return {
        "total_reservations": len(reservations_db),
        "room_types_summary": list(stats.values())
    }


# ============================================
# GET /reservations/{id} - Obtener una reserva
# ============================================

@router.get("/{reservation_id}")
async def get_reservation(
    reservation_id: int = Path(..., gt=0, description="ID de la reserva")
):
    """
    Obtener una reserva por su ID, incluyendo datos del tipo de habitación.
    """
    if reservation_id not in reservations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reservation_id} no encontrada"
        )
    return enrich_reservation(reservations_db[reservation_id])


# ============================================
# POST /reservations - Crear reserva
# ============================================

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation: ReservationCreate):
    """
    Registrar una nueva reserva hotelera.
    """
    if reservation.room_type_id not in room_types_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El tipo de habitación con ID {reservation.room_type_id} no existe"
        )

    room_type = room_types_db[reservation.room_type_id]
    if not room_type["is_available"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El tipo de habitación '{room_type['name']}' no está disponible para reservas"
        )

    new_id = get_next_reservation_id()
    new_reservation = {
        "id": new_id,
        **reservation.model_dump(),
        "status": reservation.status.value,
        "created_at": datetime.now()
    }
    reservations_db[new_id] = new_reservation
    return enrich_reservation(new_reservation)


# ============================================
# PUT /reservations/{id} - Reemplazar reserva
# ============================================

@router.put("/{reservation_id}")
async def replace_reservation(
    reservation_id: int = Path(..., gt=0),
    reservation: ReservationCreate = ...
):
    """
    Reemplazar completamente los datos de una reserva.
    """
    if reservation_id not in reservations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reservation_id} no encontrada"
        )
    if reservation.room_type_id not in room_types_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El tipo de habitación con ID {reservation.room_type_id} no existe"
        )

    updated = {
        "id": reservation_id,
        **reservation.model_dump(),
        "status": reservation.status.value,
        "created_at": reservations_db[reservation_id]["created_at"]
    }
    reservations_db[reservation_id] = updated
    return enrich_reservation(updated)


# ============================================
# PATCH /reservations/{id} - Actualizar parcialmente
# ============================================

@router.patch("/{reservation_id}")
async def update_reservation(
    reservation_id: int = Path(..., gt=0),
    reservation: ReservationUpdate = ...
):
    """
    Actualizar parcialmente una reserva (ej: cambiar estado o solicitudes especiales).
    """
    if reservation_id not in reservations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reservation_id} no encontrada"
        )

    update_data = reservation.model_dump(exclude_unset=True)

    if "room_type_id" in update_data and update_data["room_type_id"] not in room_types_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El tipo de habitación con ID {update_data['room_type_id']} no existe"
        )

    # Convertir enum a string si viene status
    if "status" in update_data and hasattr(update_data["status"], "value"):
        update_data["status"] = update_data["status"].value

    reservations_db[reservation_id].update(update_data)
    return enrich_reservation(reservations_db[reservation_id])


# ============================================
# DELETE /reservations/{id} - Eliminar reserva
# ============================================

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: int = Path(..., gt=0)
):
    """
    Eliminar una reserva del sistema.
    """
    if reservation_id not in reservations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {reservation_id} no encontrada"
        )
    del reservations_db[reservation_id]
    return None


# ============================================
# GET /reservations/by-room-type/{id} - Reservas por tipo de habitación
# ============================================

@router.get("/by-room-type/{room_type_id}")
async def reservations_by_room_type(
    room_type_id: int = Path(..., gt=0, description="ID del tipo de habitación")
):
    """
    Listar todas las reservas de un tipo de habitación específico.
    """
    if room_type_id not in room_types_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {room_type_id} no encontrado"
        )
    res_list = [enrich_reservation(r) for r in reservations_db.values() if r["room_type_id"] == room_type_id]
    return {
        "room_type": room_types_db[room_type_id],
        "total": len(res_list),
        "reservations": res_list
    }
