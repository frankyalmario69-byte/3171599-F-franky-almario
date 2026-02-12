# Dominio: Plataforma de reservas hoteleras | Turismo y Hospitalidad

from fastapi import FastAPI

# TODO 1: Crear FastAPI app con nombre de tu dominio
app = FastAPI(
    title="Hotel Booking API",
    description="Plataforma de reservas hoteleras - Turismo y Hospitalidad",
    version="1.0.0"
)

# Diccionario de mensajes de bienvenida multiidioma
WELCOME_MESSAGES: dict[str, str] = {
    "es": "¡Bienvenido al hotel, {name}!",
    "en": "Welcome to the hotel, {name}!",
    "fr": "Bienvenue à l'hôtel, {name}!",
}
SUPPORTED_LANGUAGES = list(WELCOME_MESSAGES.keys())

# RF-01: API Information Endpoint
@app.get("/")
async def root() -> dict[str, str | list[str]]:
    return {
        "name": "Hotel Booking API",
        "version": "1.0.0",
        "domain": "turismo-hospitalidad",
        "languages": SUPPORTED_LANGUAGES,
    }

# RF-02: Personalized Welcome
@app.get("/guest/{name}")
async def welcome_guest(name: str, language: str = "es") -> dict[str, str]:
    template = WELCOME_MESSAGES.get(language, WELCOME_MESSAGES["es"])
    message = template.format(name=name)
    return {"message": message, "language": language, "guest": name}

# RF-03: Entity Information (Hotel Info)
@app.get("/hotel/{id}/info")
async def hotel_info(id: str, detail_level: str = "basic") -> dict[str, str | int | float]:
    basic_info = {"id": id, "name": "Hotel Bogotá", "rooms": 120}
    full_info = {**basic_info, "location": "Bogotá Centro", "rating": 4.5}
    return basic_info if detail_level == "basic" else full_info

# RF-04: Time-Based Service
def get_service_schedule(hour: int) -> tuple[str, list[str]]:
    if 6 <= hour <= 11:
        return ("Servicio de desayuno disponible", ["restaurant", "room-service"])
    elif 12 <= hour <= 17:
        return ("Check-in en curso", ["front-desk", "concierge"])
    else:
        return ("Servicio nocturno activo", ["room-service", "security"])

@app.get("/service/schedule")
async def service_schedule(hour: int) -> dict[str, str | list[str] | int]:
    if not (0 <= hour <= 23):
        return {"error": "La hora debe estar entre
