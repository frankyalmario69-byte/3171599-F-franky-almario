"""
Schemas Pydantic para la API de Reservas Hoteleras
====================================================

Schemas requeridos:
- ReservationBase: Campos comunes
- ReservationCreate: Para POST (con validadores)
- ReservationUpdate: Para PATCH (todos opcionales)
- ReservationResponse: Para respuestas
- ReservationList: Lista paginada
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from decimal import Decimal
import re
from enum import Enum


# ============================================
# Enum de estados
# ============================================

class StatusEnum(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    checked_in = "checked_in"
    cancelled = "cancelled"


# ============================================
# ReservationBase
# ============================================

class ReservationBase(BaseModel):
    reservation_code: str = Field(..., min_length=10, max_length=10)
    guest_name: str = Field(..., min_length=2, max_length=100)
    hotel_name: str = Field(..., min_length=2, max_length=100)
    room_type: str = Field(..., min_length=2, max_length=100)
    city: str = Field(..., min_length=2, max_length=100)
    num_nights: Decimal = Field(..., gt=0)
    status: StatusEnum = StatusEnum.pending
    is_vip: bool = False


# ============================================
# ReservationCreate
# ============================================

class ReservationCreate(ReservationBase):
    """Schema para crear una reserva."""

    @field_validator("reservation_code")
    def validate_reservation_code(cls, v: str) -> str:
        # Formato: 2 letras + 8 números (ej: HR12345678)
        if not re.match(r"^[A-Z]{2}\d{8}$", v):
            raise ValueError("Reservation code must be format: XX12345678 (e.g. HR12345678)")
        return v.upper()

    @field_validator("num_nights")
    def validate_num_nights(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Number of nights must be greater than 0")
        return round(v, 0)

    @field_validator("guest_name", "hotel_name", "room_type", "city")
    def normalize_strings(cls, v: str) -> str:
        return v.strip().title()


# ============================================
# ReservationUpdate
# ============================================

class ReservationUpdate(BaseModel):
    reservation_code: str | None = None
    guest_name: str | None = None
    hotel_name: str | None = None
    room_type: str | None = None
    city: str | None = None
    num_nights: Decimal | None = None
    status: StatusEnum | None = None
    is_vip: bool | None = None

    @field_validator("reservation_code")
    def validate_reservation_code(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not re.match(r"^[A-Z]{2}\d{8}$", v):
            raise ValueError("Reservation code must be format: XX12345678 (e.g. HR12345678)")
        return v.upper()

    @field_validator("num_nights")
    def validate_num_nights(cls, v: Decimal | None) -> Decimal | None:
        if v is None:
            return v
        if v <= 0:
            raise ValueError("Number of nights must be greater than 0")
        return round(v, 0)

    @field_validator("guest_name", "hotel_name", "room_type", "city")
    def normalize_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip().title()


# ============================================
# ReservationResponse
# ============================================

class ReservationResponse(ReservationBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


# ============================================
# ReservationList
# ============================================

class ReservationList(BaseModel):
    items: list[ReservationResponse]
    total: int
    page: int
    per_page: int
