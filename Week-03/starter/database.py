"""
Base de Datos Simulada
======================

Datos en memoria para el sistema de reservas hoteleras.
"""

from datetime import datetime

# ============================================
# TIPOS DE HABITACIÓN (Categories)
# ============================================

room_types_db: dict[int, dict] = {
    1: {
        "id": 1,
        "code": "SGL-STD",
        "name": "Individual Estándar",
        "description": "Habitación individual con cama sencilla, ideal para viajeros de negocios",
        "price_per_night": 80.0,
        "is_available": True,
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    2: {
        "id": 2,
        "code": "DBL-STD",
        "name": "Doble Estándar",
        "description": "Habitación doble con cama matrimonial o dos camas individuales",
        "price_per_night": 120.0,
        "is_available": True,
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    3: {
        "id": 3,
        "code": "STE-STD",
        "name": "Suite Estándar",
        "description": "Suite con sala de estar separada, perfecta para estadías prolongadas",
        "price_per_night": 200.0,
        "is_available": True,
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    4: {
        "id": 4,
        "code": "STE-PRE",
        "name": "Suite Presidencial",
        "description": "Suite presidencial con vista panorámica, mayordomía y amenidades premium",
        "price_per_night": 500.0,
        "is_available": True,
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
}

next_room_type_id = 5

# ============================================
# RESERVAS (Main Entity)
# ============================================

reservations_db: dict[int, dict] = {
    1: {
        "id": 1,
        "reservation_code": "RES-2024-001",
        "guest_name": "Carlos Pérez",
        "hotel_name": "Hotel Grand Plaza",
        "room_type_id": 2,
        "status": "confirmed",
        "check_in_date": "2024-06-15",
        "check_out_date": "2024-06-18",
        "num_nights": 3,
        "special_requests": "Habitación en piso alto con vista al mar",
        "is_vip": False,
        "created_at": datetime(2024, 5, 10, 9, 0, 0)
    },
    2: {
        "id": 2,
        "reservation_code": "RES-2024-002",
        "guest_name": "Ana Gómez",
        "hotel_name": "Hotel Boutique Central",
        "room_type_id": 1,
        "status": "checked_in",
        "check_in_date": "2024-07-01",
        "check_out_date": "2024-07-03",
        "num_nights": 2,
        "special_requests": None,
        "is_vip": False,
        "created_at": datetime(2024, 6, 15, 10, 0, 0)
    },
    3: {
        "id": 3,
        "reservation_code": "RES-2024-003",
        "guest_name": "Luis Martínez",
        "hotel_name": "Grand Hotel Internacional",
        "room_type_id": 4,
        "status": "confirmed",
        "check_in_date": "2024-08-20",
        "check_out_date": "2024-08-25",
        "num_nights": 5,
        "special_requests": "Decoración especial por aniversario, champán de bienvenida",
        "is_vip": True,
        "created_at": datetime(2024, 7, 1, 14, 0, 0)
    },
    4: {
        "id": 4,
        "reservation_code": "RES-2024-004",
        "guest_name": "Empresa MexTech",
        "hotel_name": "Hotel Ejecutivo Norte",
        "room_type_id": 3,
        "status": "pending",
        "check_in_date": "2024-09-10",
        "check_out_date": "2024-09-14",
        "num_nights": 4,
        "special_requests": "Sala de reuniones disponible, desayuno incluido",
        "is_vip": False,
        "created_at": datetime(2024, 8, 1, 8, 0, 0)
    },
    5: {
        "id": 5,
        "reservation_code": "RES-2024-005",
        "guest_name": "María Torres",
        "hotel_name": "Hotel Grand Plaza",
        "room_type_id": 2,
        "status": "pending",
        "check_in_date": "2024-10-05",
        "check_out_date": "2024-10-07",
        "num_nights": 2,
        "special_requests": "Cuna para bebé",
        "is_vip": False,
        "created_at": datetime(2024, 9, 1, 11, 0, 0)
    },
    6: {
        "id": 6,
        "reservation_code": "RES-2024-006",
        "guest_name": "Juan Rodríguez",
        "hotel_name": "Hotel Boutique Central",
        "room_type_id": 1,
        "status": "confirmed",
        "check_in_date": "2024-11-12",
        "check_out_date": "2024-11-14",
        "num_nights": 2,
        "special_requests": None,
        "is_vip": False,
        "created_at": datetime(2024, 10, 5, 16, 0, 0)
    },
    7: {
        "id": 7,
        "reservation_code": "RES-2024-007",
        "guest_name": "Studio ARG",
        "hotel_name": "Grand Hotel Internacional",
        "room_type_id": 3,
        "status": "cancelled",
        "check_in_date": "2024-12-01",
        "check_out_date": "2024-12-05",
        "num_nights": 4,
        "special_requests": "Estudio fotográfico disponible",
        "is_vip": True,
        "created_at": datetime(2024, 11, 1, 9, 0, 0)
    },
    8: {
        "id": 8,
        "reservation_code": "RES-2024-008",
        "guest_name": "Café Europa SL",
        "hotel_name": "Hotel Ejecutivo Norte",
        "room_type_id": 2,
        "status": "confirmed",
        "check_in_date": "2024-12-10",
        "check_out_date": "2024-12-17",
        "num_nights": 7,
        "special_requests": "Frigobar sin alcohol, menú especial vegano",
        "is_vip": False,
        "created_at": datetime(2024, 11, 15, 10, 0, 0)
    },
}

next_reservation_id = 9


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_next_room_type_id() -> int:
    """Obtener y incrementar ID de tipo de habitación"""
    global next_room_type_id
    current = next_room_type_id
    next_room_type_id += 1
    return current


def get_next_reservation_id() -> int:
    """Obtener y incrementar ID de reserva"""
    global next_reservation_id
    current = next_reservation_id
    next_reservation_id += 1
    return current
