"""
API de Reservas Hoteleras - Main
==================================

Punto de entrada de la aplicación.
Sistema de gestión de reservas hoteleras.
"""

from fastapi import FastAPI
from routers import room_types, reservations

app = FastAPI(
    title="API de Reservas Hoteleras",
    description=(
        "API para gestión de reservas hoteleras. "
        "Permite registrar tipos de habitación, crear reservas, filtrarlas por múltiples "
        "criterios y consultar estadísticas por tipo de habitación."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir routers
app.include_router(room_types.router)    # /room-types
app.include_router(reservations.router)  # /reservations


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "API de Reservas Hoteleras",
        "docs": "/docs",
        "version": "1.0.0",
        "endpoints": {
            "tipos_habitacion": "/room-types",
            "reservas": "/reservations",
            "busqueda": "/reservations/search?q=término",
            "estadísticas": "/reservations/stats"
        }
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """Health check"""
    return {"status": "healthy"}
