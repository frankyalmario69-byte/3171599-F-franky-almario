"""
Dependencias Reutilizables
==========================

Define dependencias para paginación, filtros y ordenamiento
adaptadas al dominio de reservas hoteleras.
"""

from fastapi import Query, Depends
from typing import Annotated
from schemas import SortOrder, ReservationSortField, ReservationStatus


# ============================================
# PAGINACIÓN
# ============================================

class PaginationParams:
    """
    Dependencia para parámetros de paginación.
    - page: número de página (default 1)
    - per_page: ítems por página (default 10, máx 50)
    - offset: calculado automáticamente
    """

    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Número de página"),
        per_page: int = Query(default=10, ge=1, le=50, description="Reservas por página")
    ):
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page


PaginationDep = Annotated[PaginationParams, Depends()]


# ============================================
# FILTROS DE RESERVAS
# ============================================

class ReservationFilters:
    """
    Dependencia para filtros de búsqueda de reservas.

    Filtros disponibles:
    - search         → busca en reservation_code, guest_name y special_requests
    - room_type_id   → filtra por tipo de habitación
    - status         → filtra por estado (pending, confirmed, checked_in, cancelled)
    - hotel_name     → filtra por nombre del hotel
    - is_vip         → solo reservas de huéspedes VIP o no VIP
    - min_nights     → número mínimo de noches
    - max_nights     → número máximo de noches
    - check_in_date  → filtra por fecha de entrada (búsqueda parcial, ej: "2024-06")
    - check_out_date → filtra por fecha de salida (búsqueda parcial, ej: "2024-07")
    """

    def __init__(
        self,
        search: str | None = Query(
            default=None,
            min_length=2,
            description="Busca en código de reserva, nombre del huésped o solicitudes especiales"
        ),
        room_type_id: int | None = Query(
            default=None,
            gt=0,
            description="Filtrar por ID de tipo de habitación"
        ),
        status: ReservationStatus | None = Query(
            default=None,
            description="Filtrar por estado: pending, confirmed, checked_in, cancelled"
        ),
        hotel_name: str | None = Query(
            default=None,
            min_length=2,
            description="Filtrar por nombre del hotel (ej: Grand Plaza)"
        ),
        is_vip: bool | None = Query(
            default=None,
            description="Filtrar reservas VIP (true) o no VIP (false)"
        ),
        min_nights: int | None = Query(
            default=None,
            ge=1,
            description="Número mínimo de noches"
        ),
        max_nights: int | None = Query(
            default=None,
            ge=1,
            description="Número máximo de noches"
        ),
        check_in_date: str | None = Query(
            default=None,
            min_length=4,
            description="Filtrar por fecha de entrada (búsqueda parcial, ej: 2024-06)"
        ),
        check_out_date: str | None = Query(
            default=None,
            min_length=4,
            description="Filtrar por fecha de salida (búsqueda parcial, ej: 2024-07)"
        ),
    ):
        self.search = search
        self.room_type_id = room_type_id
        self.status = status
        self.hotel_name = hotel_name
        self.is_vip = is_vip
        self.min_nights = min_nights
        self.max_nights = max_nights
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date


ReservationFiltersDep = Annotated[ReservationFilters, Depends()]


# ============================================
# ORDENAMIENTO
# ============================================

class SortingParams:
    """
    Dependencia para ordenamiento de reservas.
    - sort_by: campo por el que ordenar (default: created_at)
    - order: asc o desc (default: desc)
    """

    def __init__(
        self,
        sort_by: ReservationSortField = Query(
            default=ReservationSortField.created_at,
            description="Campo por el que ordenar"
        ),
        order: SortOrder = Query(
            default=SortOrder.desc,
            description="Orden: asc (ascendente) o desc (descendente)"
        )
    ):
        self.sort_by = sort_by
        self.order = order


SortingDep = Annotated[SortingParams, Depends()]
