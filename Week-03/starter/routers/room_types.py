"""
Router de Tipos de Habitación
==============================

CRUD completo para tipos de habitación (categorías del dominio hotelero).
"""

from fastapi import APIRouter, Path, HTTPException, status
from datetime import datetime

from database import room_types_db, get_next_room_type_id
from schemas import RoomTypeCreate, RoomTypeUpdate, RoomTypeResponse

router = APIRouter(
    prefix="/room-types",
    tags=["Tipos de Habitación"],
    responses={404: {"description": "Tipo de habitación no encontrado"}}
)


# ============================================
# GET /room-types - Listar todos los tipos
# ============================================

@router.get("/", response_model=list[RoomTypeResponse])
async def list_room_types():
    """
    Listar todos los tipos de habitación disponibles.
    """
    return list(room_types_db.values())


# ============================================
# GET /room-types/{id} - Obtener un tipo
# ============================================

@router.get("/{room_type_id}", response_model=RoomTypeResponse)
async def get_room_type(
    room_type_id: int = Path(..., gt=0, description="ID del tipo de habitación")
):
    """
    Obtener un tipo de habitación por su ID.
    """
    if room_type_id not in room_types_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {room_type_id} no encontrado"
        )
    return room_types_db[room_type_id]


# ============================================
# POST /room-types - Crear tipo de habitación
# ============================================

@router.post("/", response_model=RoomTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_room_type(room_type: RoomTypeCreate):
    """
    Crear un nuevo tipo de habitación.
    """
    new_id = get_next_room_type_id()
    new_room_type = {
        "id": new_id,
        **room_type.model_dump(),
        "created_at": datetime.now()
    }
    room_types_db[new_id] = new_room_type
    return new_room_type


# ============================================
# PUT /room-types/{id} - Reemplazar tipo completo
# ============================================

@router.put("/{room_type_id}", response_model=RoomTypeResponse)
async def update_room_type(
    room_type_id: int = Path(..., gt=0),
    room_type: RoomTypeCreate = ...
):
    """
    Actualizar completamente un tipo de habitación.
    """
    if room_type_id not in room_types_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {room_type_id} no encontrado"
        )
    updated_room_type = {
        "id": room_type_id,
        **room_type.model_dump(),
        "created_at": room_types_db[room_type_id]["created_at"]
    }
    room_types_db[room_type_id] = updated_room_type
    return updated_room_type


# ============================================
# DELETE /room-types/{id} - Eliminar tipo
# ============================================

@router.delete("/{room_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_type(
    room_type_id: int = Path(..., gt=0)
):
    """
    Eliminar un tipo de habitación.
    """
    if room_type_id not in room_types_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitación con ID {room_type_id} no encontrado"
        )
    del room_types_db[room_type_id]
    return None
