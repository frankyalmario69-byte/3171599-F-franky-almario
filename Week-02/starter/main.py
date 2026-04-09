"""
Proyecto Semana 02: API de Gestión de Reservas Hoteleras
=========================================================

Aplicación FastAPI principal.
Los endpoints ya están definidos, debes completar schemas.py

Ejecutar:
    docker compose up --build

Documentación: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, status, Query
from datetime import datetime

# Importar los schemas que crearás
from schemas import (
    ReservationCreate,
    ReservationUpdate,
    ReservationResponse,
    ReservationList,
)
from database import reservations_db, get_next_id, find_by_reservation_code

app = FastAPI(
    title="API de Gestión de Reservas Hoteleras",
    description="Proyecto Semana 02 - Pydantic v2",
    version="1.0.0",
)


# ============================================
# ENDPOINTS
# ============================================

@app.post(
    "/reservations",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Reservations"],
)
async def create_reservation(reservation: ReservationCreate) -> ReservationResponse:
    """
    Crear una nueva reserva hotelera.

    - Valida que el reservation_code no exista
    """
    if find_by_reservation_code(reservation.reservation_code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Reservation with code {reservation.reservation_code} already exists"
        )

    reservation_id = get_next_id()
    new_reservation = {
        "id": reservation_id,
        **reservation.model_dump(),
        "created_at": datetime.now(),
        "updated_at": None,
    }
    reservations_db[reservation_id] = new_reservation

    return new_reservation


@app.get(
    "/reservations",
    response_model=ReservationList,
    tags=["Reservations"],
)
async def list_reservations(
    page: int = Query(ge=1, default=1),
    per_page: int = Query(ge=1, le=100, default=10),
    status: str | None = None,
) -> ReservationList:
    """
    Listar reservas con paginación.

    - Soporta filtro por estado
    """
    reservations = list(reservations_db.values())
    if status:
        reservations = [r for r in reservations if r["status"] == status]

    total = len(reservations)
    start = (page - 1) * per_page
    end = start + per_page
    items = reservations[start:end]

    return ReservationList(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
    )


@app.get(
    "/reservations/{reservation_id}",
    response_model=ReservationResponse,
    tags=["Reservations"],
)
async def get_reservation(reservation_id: int) -> ReservationResponse:
    """Obtener reserva por ID."""
    if reservation_id not in reservations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    return reservations_db[reservation_id]


@app.get(
    "/reservations/code/{reservation_code}",
    response_model=ReservationResponse,
    tags=["Reservations"],
)
async def get_reservation_by_code(reservation_code: str) -> ReservationResponse:
    """Buscar reserva por código de reserva."""
    reservation = find_by_reservation_code(reservation_code)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    return reservation


@app.patch(
    "/reservations/{reservation_id}",
    response_model=ReservationResponse,
    tags=["Reservations"],
)
async def update_reservation(
    reservation_id: int,
    reservation: ReservationUpdate,
) -> ReservationResponse:
    """Actualizar reserva parcialmente."""
    if reservation_id not in reservations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )

    update_data = reservation.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    if "reservation_code" in update_data:
        existing = find_by_reservation_code(update_data["reservation_code"])
        if existing and existing["id"] != reservation_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Reservation code {update_data['reservation_code']} already in use"
            )

    stored = reservations_db[reservation_id]
    for key, value in update_data.items():
        stored[key] = value
    stored["updated_at"] = datetime.now()

    return stored


@app.delete(
    "/reservations/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Reservations"],
)
async def delete_reservation(reservation_id: int) -> None:
    """Eliminar reserva."""
    if reservation_id not in reservations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    del reservations_db[reservation_id]


# ============================================
# HEALTH CHECK
# ============================================

@app.get("/", tags=["Health"])
async def root():
    """Health check."""
    return {
        "status": "ok",
        "message": "Hotel Reservations API running",
        "total_reservations": len(reservations_db),
    }
