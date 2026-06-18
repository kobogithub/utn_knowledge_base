"""Esquemas de inventario."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from backend.schemas.semilla import LoteLeer


class InventarioLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lote_id: int
    stock_total: float
    stock_reservado: float
    stock_disponible: float
    lote: LoteLeer
