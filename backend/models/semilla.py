"""Modelos de semillas y lotes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

if TYPE_CHECKING:
    from backend.models.inventario import Inventario
    from backend.models.pedido import LineaPedido


class Semilla(Base):
    """Variedad de semilla comercializada."""

    __tablename__ = "semillas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False, index=True
    )
    descripcion: Mapped[str | None] = mapped_column(String(255))

    lotes: Mapped[list[Lote]] = relationship(
        back_populates="semilla", cascade="all, delete-orphan"
    )


class Lote(Base):
    """Lote físico de una semilla."""

    __tablename__ = "lotes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    semilla_id: Mapped[int] = mapped_column(
        ForeignKey("semillas.id"), nullable=False
    )
    kilos_disponibles: Mapped[float] = mapped_column(Float, nullable=False)

    semilla: Mapped[Semilla] = relationship(back_populates="lotes")
    inventario: Mapped[Inventario | None] = relationship(
        back_populates="lote", cascade="all, delete-orphan", uselist=False
    )
    lineas_pedido: Mapped[list[LineaPedido]] = relationship(
        back_populates="lote"
    )
