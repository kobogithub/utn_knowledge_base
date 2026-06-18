"""Servicios de semillas."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.semilla import Lote, Semilla
from backend.schemas.semilla import LoteCrear, SemillaCrear


def listar_semillas(db: Session) -> list[Semilla]:
    """Obtiene todas las semillas."""

    return list(db.scalars(select(Semilla).order_by(Semilla.id)).all())


def crear_semilla(db: Session, datos: SemillaCrear) -> Semilla:
    """Crea una semilla nueva."""

    semilla = Semilla(nombre=datos.nombre, descripcion=datos.descripcion)
    db.add(semilla)
    db.commit()
    db.refresh(semilla)
    return semilla


def crear_lote(db: Session, datos: LoteCrear) -> Lote:
    """Crea un lote y su inventario asociado."""

    from backend.models.inventario import Inventario

    lote = Lote(
        codigo=datos.codigo,
        semilla_id=datos.semilla_id,
        kilos_disponibles=datos.kilos_disponibles,
    )
    db.add(lote)
    db.flush()
    inventario = Inventario(
        lote_id=lote.id,
        stock_total=datos.kilos_disponibles,
        stock_reservado=0,
    )
    db.add(inventario)
    db.commit()
    db.refresh(lote)
    return lote


def listar_lotes(db: Session) -> list[Lote]:
    """Obtiene todos los lotes."""

    return list(db.scalars(select(Lote).order_by(Lote.id)).all())
