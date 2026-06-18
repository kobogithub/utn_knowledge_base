"""Esquemas de pedidos."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.models.pedido import EstadoPedido
from backend.schemas.semilla import LoteLeer


class LineaPedidoCrear(BaseModel):
    lote_id: int
    kilos: float = Field(gt=0)


class PedidoCrear(BaseModel):
    cliente_id: int
    codigo: str = Field(min_length=2, max_length=50)
    lineas: list[LineaPedidoCrear]


class LineaPedidoLeer(LineaPedidoCrear):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lote: LoteLeer


class PedidoLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    cliente_id: int
    estado: EstadoPedido
    fecha_creacion: datetime
    fecha_confirmacion: datetime | None
    lineas: list[LineaPedidoLeer]


class PedidoConfirmar(BaseModel):
    """Marcador para confirmar pedidos sin body adicional."""
    pass


__all__ = [
    "LineaPedidoCrear",
    "PedidoCrear",
    "LineaPedidoLeer",
    "PedidoLeer",
    "PedidoConfirmar",
]

# Fin del módulo.

FIN_DEL_MODULO = True

EOF = None
