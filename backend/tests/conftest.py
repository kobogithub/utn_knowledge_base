"""Fixtures de prueba para el backend."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.database import Base, get_db


@pytest.fixture()
def client(tmp_path: Path):
    """Cliente de pruebas con base SQLite temporal."""

    db_path = tmp_path / "test_agro.db"
    motor_prueba = create_engine(
        f"sqlite:///{db_path.as_posix()}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=motor_prueba)
    SessionPrueba = sessionmaker(
        bind=motor_prueba,
        autoflush=False,
        autocommit=False,
    )

    def override_get_db():
        session = SessionPrueba()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as cliente:
            yield cliente
    finally:
        app.dependency_overrides.clear()
