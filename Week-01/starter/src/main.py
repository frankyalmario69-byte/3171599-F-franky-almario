# ============================================
# PROYECTO: API DE RESERVAS HOTELERAS
# ============================================
# Semana 01 - Bootcamp FastAPI Zero to Hero
# ============================================

from fastapi import FastAPI

# ============================================
# DATOS DE CONFIGURACIÓN
# ============================================

# Diccionario de saludos por idioma
GREETINGS: dict[str, str] = {
    "es": "¡Bienvenido al Hotel, {name}! Esperamos que disfrute su estadía.",
    "en": "Welcome to the Hotel, {name}! We hope you enjoy your stay.",
    "fr": "Bienvenue à l'hôtel, {name}! Nous espérons que vous apprécierez votre séjour.",
    "de": "Willkommen im Hotel, {name}! Wir hoffen, dass Sie Ihren Aufenthalt genießen.",
    "it": "Benvenuto in Hotel, {name}! Speriamo che ti piaccia il soggiorno.",
    "pt": "Bem-vindo ao Hotel, {name}! Esperamos que aproveite a sua estadia.",
}

SUPPORTED_LANGUAGES = list(GREETINGS.keys())

# ============================================
# TODO 1: CREAR LA INSTANCIA DE FASTAPI
# ============================================

app = FastAPI(
    title="Hotel Reservations API",
    description="API para gestión de reservas hoteleras",
    version="1.0.0"
)

# ============================================
# TODO 2: ENDPOINT RAÍZ
# ============================================

@app.get("/")
async def root() -> dict[str, str | list[str]]:
    """Información general de la API de reservas hoteleras."""
    return {
        "name": "Hotel Reservations API",
        "version": "1.0.0",
        "domain": "hospitality",
        "docs": "/docs",
        "languages": SUPPORTED_LANGUAGES
    }

# ============================================
# TODO 3: BIENVENIDA PERSONALIZADA
# ============================================

@app.get("/welcome/{name}")
async def welcome(name: str, language: str = "es") -> dict[str, str]:
    """Mensaje de bienvenida personalizado al huésped en el idioma especificado."""
    template = GREETINGS.get(language, GREETINGS["es"])
    return {
        "message": template.format(name=name),
        "language": language,
        "guest": name
    }

# ============================================
# TODO 4: INFORMACIÓN DE ENTIDAD
# ============================================

@app.get("/entity/{name}/info")
async def entity_info(name: str, title: str = "Huésped") -> dict[str, str]:
    """Información formal del huésped o empresa registrada."""
    greeting = f"Estimado/a {title} {name}, su reserva ha sido registrada en nuestro sistema hotelero."
    return {
        "greeting": greeting,
        "title": title,
        "entity": name
    }

# ============================================
# TODO 5: SERVICIO SEGÚN HORARIO
# ============================================

def get_service_period(hour: int) -> tuple[str, str]:
    """Determina el servicio hotelero disponible según la hora."""
    if 5 <= hour < 12:
        return ("Recepción y desayuno disponibles", "morning")
    elif 12 <= hour < 18:
        return ("Servicio de habitaciones en operación", "afternoon")
    else:
        return ("Servicio nocturno y concierge disponible", "night")

@app.get("/service/{name}/time-based")
async def service_time_based(name: str, hour: int) -> dict[str, str | int]:
    """Servicio hotelero adaptado según el horario del día."""
    if hour < 0 or hour > 23:
        return {"error": "La hora debe estar entre 0 y 23"}
    mensaje, periodo = get_service_period(hour)
    return {
        "service_message": f"{mensaje}, {name}.",
        "hour": hour,
        "period": periodo
    }

# ============================================
# TODO 6: HEALTH CHECK
# ============================================

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Verifica el estado de la API."""
    return {
        "status": "healthy",
        "service": "hotel-reservations-api",
        "domain": "hospitality",
        "version": "1.0.0"
    }
