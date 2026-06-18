"""Router agregador de la API v1."""

from __future__ import annotations

from fastapi import APIRouter

from backend.api.v1.clientes import router as clientes_router
from backend.api.v1.inventario import router as inventario_router
from backend.api.v1.pedidos import router as pedidos_router
from backend.api.v1.semillas import router as semillas_router, router_lotes

api_router = APIRouter()

api_router.include_router(clientes_router)
api_router.include_router(semillas_router)
api_router.include_router(router_lotes)
api_router.include_router(pedidos_router)
api_router.include_router(inventario_router)


@api_router.get("/ping", tags=["salud"])
def ping() -> dict[str, str]:
    """Confirma que la API responde."""

    return {"mensaje": "pong"}
