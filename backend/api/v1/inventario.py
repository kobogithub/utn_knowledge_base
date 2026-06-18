"""Endpoints de inventario."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.inventario import InventarioLeer
from backend.services.inventario_service import listar_inventario

router = APIRouter(prefix="/inventario", tags=["inventario"])


@router.get("", response_model=list[InventarioLeer])
def obtener_inventario(db: Session = Depends(get_db)):
    return listar_inventario(db)
