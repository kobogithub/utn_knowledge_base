"""Esquemas de clientes."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClienteBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    documento: str = Field(min_length=5, max_length=20)
    email: EmailStr | None = None


class ClienteCrear(ClienteBase):
    """Datos para crear un cliente."""


class ClienteLeer(ClienteBase):
    """Datos expuestos de un cliente."""

    model_config = ConfigDict(from_attributes=True)

    id: int
