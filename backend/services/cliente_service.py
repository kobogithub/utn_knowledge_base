"""Servicios de clientes."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.cliente import Cliente
from backend.schemas.cliente import ClienteCrear


def listar_clientes(db: Session) -> list[Cliente]:
    """Obtiene todos los clientes."""

    return list(db.scalars(select(Cliente).order_by(Cliente.id)).all())


def crear_cliente(db: Session, datos: ClienteCrear) -> Cliente:
    """Crea un cliente nuevo."""

    cliente = Cliente(
        nombre=datos.nombre,
        documento=datos.documento,
        email=datos.email,
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente
