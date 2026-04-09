"""
Schemas Pydantic
================

Modelos de datos para el sistema de reservas hoteleras.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# ============================================
# ENUMS
# ============================================

class SortOrder(str, Enum):
    """Orden de clasificación"""
    asc = "asc"
    desc = "desc"


class ReservationSortField(str, Enum):
    """Campos para ordenar reservas"""
    reservation_code = "reservation_code"
    num_nights = "num_nights"
    created_at = "created_at"
    status = "status"
    check_out_date = "check_out_date"


class ReservationStatus(str, Enum):
    """Estados posibles de una reserva"""
    pending = "pending"         # Registrada, pendiente de confirmación
    confirmed = "confirmed"     # Confirmada
    checked_in = "checked_in"   # Huésped en el hotel
    cancelled = "cancelled"     # Cancelada


# ============================================
# ROOM TYPE SCHEMAS (Categorías = Tipos de habitación)
# ============================================

class RoomTypeBase(BaseModel):
    """Schema base para tipos de habitación"""
    code: str = Field(..., min_length=2, max_length=20, description="Código único del tipo (ej: DBL-STD)")
    name: str = Field(..., min_length=2, max_length=100, description="Nombre descriptivo del tipo de habitación")
    description: str | None = Field(default=None, max_length=300)
    price_per_night: float = Field(..., gt=0, description="Precio por noche en USD")
    is_available: bool = Field(default=True, description="¿Está disponible para reservas?")


class RoomTypeCreate(RoomTypeBase):
    """Schema para crear un tipo de habitación"""
    pass


class RoomTypeUpdate(BaseModel):
    """Schema para actualizar un tipo de habitación (todos los campos opcionales)"""
    code: str | None = Field(default=None, min_length=2, max_length=20)
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    price_per_night: float | None = Field(default=None, gt=0)
    is_available: bool | None = None


class RoomTypeResponse(RoomTypeBase):
    """Schema de respuesta para un tipo de habitación"""
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ============================================
# RESERVATION SCHEMAS (Entidad principal = Reservas)
# ============================================

class ReservationBase(BaseModel):
    """Schema base para reservas"""
    reservation_code: str = Field(..., min_length=3, max_length=50, description="Código de reserva único (ej: RES-2024-001)")
    guest_name: str = Field(..., min_length=2, max_length=150, description="Nombre del huésped")
    hotel_name: str = Field(..., min_length=2, max_length=150, description="Nombre del hotel")
    check_in_date: str = Field(..., min_length=8, max_length=20, description="Fecha de entrada (ej: 2024-06-15)")
    check_out_date: str = Field(..., min_length=8, max_length=20, description="Fecha de salida (ej: 2024-06-20)")
    num_nights: int = Field(..., gt=0, description="Número de noches")
    special_requests: str | None = Field(default=None, max_length=500, description="Solicitudes especiales del huésped")
    is_vip: bool = Field(default=False, description="¿Es huésped VIP?")


class ReservationCreate(ReservationBase):
    """Schema para crear una reserva"""
    room_type_id: int = Field(..., gt=0, description="ID del tipo de habitación")
    status: ReservationStatus = Field(default=ReservationStatus.pending, description="Estado inicial de la reserva")


class ReservationUpdate(BaseModel):
    """Schema para actualización parcial de una reserva"""
    reservation_code: str | None = Field(default=None, min_length=3, max_length=50)
    guest_name: str | None = Field(default=None, min_length=2, max_length=150)
    hotel_name: str | None = Field(default=None, min_length=2, max_length=150)
    room_type_id: int | None = Field(default=None, gt=0)
    status: ReservationStatus | None = None
    check_in_date: str | None = Field(default=None, min_length=8, max_length=20)
    check_out_date: str | None = Field(default=None, min_length=8, max_length=20)
    num_nights: int | None = Field(default=None, gt=0)
    special_requests: str | None = Field(default=None, max_length=500)
    is_vip: bool | None = None


class ReservationResponse(ReservationBase):
    """Schema de respuesta para una reserva"""
    id: int
    room_type_id: int
    status: ReservationStatus
    created_at: datetime
    room_type: RoomTypeResponse | None = None

    model_config = {"from_attributes": True}


# ============================================
# PAGINATION SCHEMAS
# ============================================

class PaginatedResponse(BaseModel):
    """Schema para respuestas paginadas"""
    items: list
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool
