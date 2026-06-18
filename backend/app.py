"""Punto de entrada de la API FastAPI Agro."""

from __future__ import annotations

from fastapi import FastAPI

from backend.api.v1.router import api_router
from backend.config import DEBUG, NOMBRE_APLICACION

app = FastAPI(title=NOMBRE_APLICACION, debug=DEBUG, version="0.1.0")


@app.get("/health", tags=["salud"])
def health() -> dict[str, str]:
    """Estado básico de salud de la aplicación."""

    return {"estado": "ok"}


app.include_router(api_router, prefix="/api/v1")
