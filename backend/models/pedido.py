"""Modelos de pedidos y líneas de pedido."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SqlEnum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

if TYPE_CHECKING:
    from backend.models.cliente import Cliente
    from backend.models.semilla import Lote


class EstadoPedido(str, Enum):
    """Estados posibles de un pedido."""

    BORRADOR = "borrador"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"


class Pedido(Base):
    """Pedido realizado por un cliente."""

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"), nullable=False
    )
    estado: Mapped[EstadoPedido] = mapped_column(
        SqlEnum(EstadoPedido), default=EstadoPedido.BORRADOR, nullable=False
    )
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    fecha_confirmacion: Mapped[datetime | None] = mapped_column(DateTime)

    cliente: Mapped[Cliente] = relationship(back_populates="pedidos")
    lineas: Mapped[list[LineaPedido]] = relationship(
        back_populates="pedido", cascade="all, delete-orphan"
    )


class LineaPedido(Base):
    """Detalle de un lote dentro de un pedido."""

    __tablename__ = "lineas_pedido"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"), nullable=False
    )
    lote_id: Mapped[int] = mapped_column(
        ForeignKey("lotes.id"), nullable=False
    )
    kilos: Mapped[float] = mapped_column(Float, nullable=False)

    pedido: Mapped[Pedido] = relationship(back_populates="lineas")
    lote: Mapped[Lote] = relationship(back_populates="lineas_pedido")
