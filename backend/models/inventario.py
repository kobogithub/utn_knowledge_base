"""Modelo de inventario por lote."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

if TYPE_CHECKING:
    from backend.models.semilla import Lote


class Inventario(Base):
    """Stock total y reservado de un lote."""

    __tablename__ = "inventarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lote_id: Mapped[int] = mapped_column(
        ForeignKey("lotes.id"), unique=True, nullable=False, index=True
    )
    stock_total: Mapped[float] = mapped_column(Float, nullable=False)
    stock_reservado: Mapped[float] = mapped_column(
        Float, nullable=False, default=0
    )

    lote: Mapped["Lote"] = relationship(back_populates="inventario")

    @property
    def stock_disponible(self) -> float:
        """Cantidad disponible para reservar."""

        return self.stock_total - self.stock_reservado
