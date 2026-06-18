"""Conexión sincrónica a SQLite y sesión de SQLAlchemy."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.config import URL_BASE_DATOS


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos ORM."""


es_sqlite = URL_BASE_DATOS.startswith("sqlite")
argumentos_motor = {"check_same_thread": False} if es_sqlite else {}

motor = create_engine(URL_BASE_DATOS, connect_args=argumentos_motor)
SessionLocal = sessionmaker(bind=motor, autoflush=False, autocommit=False)


def get_db() -> Generator:
    """Devuelve una sesión de base de datos por request."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
