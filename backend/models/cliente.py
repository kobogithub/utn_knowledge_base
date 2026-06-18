"""Modelo de clientes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

if TYPE_CHECKING:
    from backend.models.pedido import Pedido


class Cliente(Base):
    """Cliente que realiza pedidos."""

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    documento: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False, index=True
    )
    email: Mapped[str | None] = mapped_column(String(120), unique=True)

    pedidos: Mapped[list[Pedido]] = relationship(
        back_populates="cliente", cascade="all, delete-orphan"
    )
