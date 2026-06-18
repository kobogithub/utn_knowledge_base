"""Endpoints de semillas."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.semilla import (
    LoteCrear,
    LoteLeer,
    SemillaCrear,
    SemillaLeer,
)
from backend.services.semilla_service import (
    crear_lote,
    crear_semilla,
    listar_lotes,
    listar_semillas,
)

router = APIRouter(prefix="/semillas", tags=["semillas"])
router_lotes = APIRouter(prefix="/lotes", tags=["lotes"])


@router.get("", response_model=list[SemillaLeer])
def obtener_semillas(db: Session = Depends(get_db)):
    return listar_semillas(db)


@router.post(
    "",
    response_model=SemillaLeer,
    status_code=status.HTTP_201_CREATED,
)
def registrar_semilla(datos: SemillaCrear, db: Session = Depends(get_db)):
    try:
        return crear_semilla(db, datos)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router_lotes.get("", response_model=list[LoteLeer])
def obtener_lotes(db: Session = Depends(get_db)):
    return listar_lotes(db)


@router_lotes.post(
    "",
    response_model=LoteLeer,
    status_code=status.HTTP_201_CREATED,
)
def registrar_lote(datos: LoteCrear, db: Session = Depends(get_db)):
    try:
        return crear_lote(db, datos)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
