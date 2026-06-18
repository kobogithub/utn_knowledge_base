"""Endpoints de clientes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.cliente import ClienteCrear, ClienteLeer
from backend.services.cliente_service import crear_cliente, listar_clientes

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("", response_model=list[ClienteLeer])
def obtener_clientes(db: Session = Depends(get_db)):
    return listar_clientes(db)


@router.post(
    "",
    response_model=ClienteLeer,
    status_code=status.HTTP_201_CREATED,
)
def registrar_cliente(datos: ClienteCrear, db: Session = Depends(get_db)):
    try:
        return crear_cliente(db, datos)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
