"""Esquemas de semillas y lotes."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SemillaBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: str | None = Field(default=None, max_length=255)


class SemillaCrear(SemillaBase):
    """Datos para crear una semilla."""


class SemillaLeer(SemillaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class LoteBase(BaseModel):
    codigo: str = Field(min_length=2, max_length=50)
    semilla_id: int
    kilos_disponibles: float = Field(gt=0)


class LoteCrear(LoteBase):
    """Datos para crear un lote."""


class LoteLeer(LoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
