"""Endpoints de pedidos."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.pedido import PedidoCrear, PedidoLeer
from backend.services.pedido_service import (
    confirmar_pedido,
    crear_pedido,
    listar_pedidos,
)

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.get("", response_model=list[PedidoLeer])
def obtener_pedidos(db: Session = Depends(get_db)):
    return listar_pedidos(db)


@router.post(
    "",
    response_model=PedidoLeer,
    status_code=status.HTTP_201_CREATED,
)
def registrar_pedido(datos: PedidoCrear, db: Session = Depends(get_db)):
    try:
        return crear_pedido(db, datos)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/{pedido_id}/confirmar", response_model=PedidoLeer)
def confirmar_un_pedido(pedido_id: int, db: Session = Depends(get_db)):
    try:
        return confirmar_pedido(db, pedido_id)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
