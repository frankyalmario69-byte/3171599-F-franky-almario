"""
Simulación de Base de Datos en memoria para Reservas Hoteleras
"""

# "Base de datos" en memoria
reservations_db: dict[int, dict] = {}

# Contador para IDs
_id_counter = 0


def get_next_id() -> int:
    """Obtener siguiente ID disponible."""
    global _id_counter
    _id_counter += 1
    return _id_counter


def find_by_reservation_code(reservation_code: str) -> dict | None:
    """Buscar reserva por código de reserva."""
    code_upper = reservation_code.upper()
    for reservation in reservations_db.values():
        if reservation["reservation_code"].upper() == code_upper:
            return reservation
    return None


def reset_db() -> None:
    """Resetear base de datos (útil para tests)."""
    global _id_counter
    reservations_db.clear()
    _id_counter = 0
