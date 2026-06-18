"""Servicios de pedidos."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.models.cliente import Cliente
from backend.models.pedido import EstadoPedido, LineaPedido, Pedido
from backend.schemas.pedido import PedidoCrear
from backend.services.inventario_service import (
    reservar_stock_pedido,
    validar_stock_lineas,
)


def listar_pedidos(db: Session) -> list[Pedido]:
    """Obtiene pedidos con sus líneas y lotes."""

    consulta = select(Pedido).options(
        selectinload(Pedido.lineas).selectinload(LineaPedido.lote)
    ).order_by(Pedido.id)
    return list(db.scalars(consulta).all())


def crear_pedido(db: Session, datos: PedidoCrear) -> Pedido:
    """Crea un pedido en estado borrador validando stock disponible."""

    cliente = db.get(Cliente, datos.cliente_id)
    if cliente is None:
        raise ValueError("Cliente inexistente")

    lineas_validacion = [
        (linea.lote_id, linea.kilos) for linea in datos.lineas
    ]
    validar_stock_lineas(db, lineas_validacion)

    pedido = Pedido(
        codigo=datos.codigo,
        cliente_id=datos.cliente_id,
        estado=EstadoPedido.BORRADOR,
    )
    db.add(pedido)
    db.flush()

    for linea in datos.lineas:
        db.add(
            LineaPedido(
                pedido_id=pedido.id,
                lote_id=linea.lote_id,
                kilos=linea.kilos,
            )
        )

    db.commit()
    db.refresh(pedido)
    return obtener_pedido(db, pedido.id)


def obtener_pedido(db: Session, pedido_id: int) -> Pedido:
    """Obtiene un pedido con sus relaciones cargadas."""

    consulta = (
        select(Pedido)
        .where(Pedido.id == pedido_id)
        .options(selectinload(Pedido.lineas).selectinload(LineaPedido.lote))
    )
    pedido = db.scalar(consulta)
    if pedido is None:
        raise ValueError("Pedido inexistente")
    return pedido


def confirmar_pedido(db: Session, pedido_id: int) -> Pedido:
    """Confirma un pedido y reserva su stock."""

    pedido = obtener_pedido(db, pedido_id)
    if pedido.estado == EstadoPedido.CONFIRMADO:
        return pedido

    reservar_stock_pedido(db, pedido)
    pedido.estado = EstadoPedido.CONFIRMADO
    pedido.fecha_confirmacion = datetime.utcnow()
    db.commit()
    db.refresh(pedido)
    return obtener_pedido(db, pedido.id)
