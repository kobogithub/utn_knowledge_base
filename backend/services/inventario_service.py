"""Servicios de inventario."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.inventario import Inventario
from backend.models.pedido import Pedido


def listar_inventario(db: Session) -> list[Inventario]:
    """Obtiene todo el inventario por lote."""

    return list(db.scalars(select(Inventario).order_by(Inventario.id)).all())


def obtener_inventario_por_lote(
    db: Session, lote_id: int
) -> Inventario | None:
    """Busca el inventario asociado a un lote."""

    consulta = select(Inventario).where(Inventario.lote_id == lote_id)
    return db.scalar(consulta)


def validar_stock_lineas(db: Session, lineas: list[tuple[int, float]]) -> None:
    """Valida que exista stock disponible suficiente para cada lote."""

    for lote_id, kilos in lineas:
        inventario = obtener_inventario_por_lote(db, lote_id)
        if inventario is None:
            raise ValueError(f"No existe inventario para el lote {lote_id}")
        if kilos > inventario.stock_disponible:
            raise ValueError(f"Stock insuficiente para el lote {lote_id}")


def reservar_stock_pedido(db: Session, pedido: Pedido) -> None:
    """Reserva stock para todas las líneas de un pedido confirmado."""

    for linea in pedido.lineas:
        inventario = obtener_inventario_por_lote(db, linea.lote_id)
        if inventario is None:
            raise ValueError(
                f"No existe inventario para el lote {linea.lote_id}"
            )
        if linea.kilos > inventario.stock_disponible:
            raise ValueError(
                f"Stock insuficiente para el lote {linea.lote_id}"
            )
        inventario.stock_reservado += linea.kilos

    db.commit()
