"""Configuración central del backend."""

from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
NOMBRE_APLICACION = os.getenv("APP_NAME", "FastAPI Agro")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
URL_BASE_DATOS = os.getenv(
    "DB_URL",
    f"sqlite:///{(BASE_DIR / 'agro.db').as_posix()}",
)
