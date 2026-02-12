# QUÉ: Importo FastAPI
# PARA: Crear la aplicación web y definir endpoints
# IMPACTO: Sin esto no puedo levantar el servidor ni usar las rutas
from fastapi import FastAPI

# QUÉ: Diccionario con mensajes de confirmación en varios idiomas
# PARA: Personalizar la experiencia de reservas según el idioma del cliente
# IMPACTO: Hace que la plataforma sea más inclusiva y usable internacionalmente
CONFIRMATIONS: dict[str, str] = {
    "es": "Reserva confirmada para {name} en el hotel {hotel}.",
    "en": "Booking confirmed for {name} at hotel {hotel}.",
    "fr": "Réservation confirmée pour {name} à l'hôtel {hotel}.",
    "de": "Buchung bestätigt für {name} im Hotel {hotel}.",
    "it": "Prenotazione confermata per {name} presso l'hotel {hotel}.",
    "pt": "Reserva confirmada para {name} no hotel {hotel}.",
}

# QUÉ: Lista de idiomas soportados
# PARA: Mostrar en la documentación qué idiomas están disponibles
# IMPACTO: Ayuda a los usuarios a saber qué opciones tienen
SUPPORTED_LANGUAGES = list(CONFIRMATIONS.keys())

# QUÉ: Creo la instancia principal de FastAPI
# PARA: Configurar la API con título, descripción y versión
# IMPACTO: Esto aparece en la documentación automática y da contexto
app = FastAPI(
    title="Hotel Booking API",
    description="Plataforma de reservas hoteleras - Turismo y Hospitalidad",
    version="1.0.0"
)

# QUÉ: Endpoint raíz GET /
# PARA: Mostrar información básica de la API
# IMPACTO: Sirve como punto de entrada para saber qué hace la API
@app.get("/")
async def root() -> dict[str, str | list[str]]:
    return {
        "name": "Hotel Booking API",
        "version": "1.0.0",
        "docs": "/docs",
        "languages": SUPPORTED_LANGUAGES,
        "domain": "Turismo y Hospitalidad"
    }

# QUÉ: Endpoint GET /book/{hotel}/{name}
# PARA: Registrar una reserva en un hotel para un cliente
# IMPACTO: Ejemplo de cómo usar parámetros de ruta y query
@app.get("/book/{hotel}/{name}")
async def book(hotel: str, name: str, language: str = "es") -> dict[str, str]:
    template = CONFIRMATIONS.get(language, CONFIRMATIONS["es"])
    confirmation = template.format(name=name, hotel=hotel)
    return {"confirmation": confirmation, "hotel": hotel, "name": name, "language": language}

# QUÉ: Endpoint GET /health
# PARA: Verificar que la API está funcionando correctamente
# IMPACTO: Útil para monitoreo y despliegues en producción
@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "service": "hotel-booking-api", "version": "1.0.0"}
