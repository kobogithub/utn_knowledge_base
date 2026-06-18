"""Inicializa la base de datos y carga datos de ejemplo."""

from __future__ import annotations

from sqlalchemy import select

from backend.database import Base, SessionLocal, motor
from backend.models.cliente import Cliente
from backend.models.inventario import Inventario
from backend.models.pedido import EstadoPedido, LineaPedido, Pedido
from backend.models.semilla import Lote, Semilla
from backend.services.inventario_service import reservar_stock_pedido


def obtener_o_crear(session, modelo, filtro, valores):
    instancia = session.scalar(select(modelo).where(filtro))
    if instancia is None:
        instancia = modelo(**valores)
        session.add(instancia)
        session.flush()
    return instancia


def inicializar_base() -> None:
    """Crea tablas y carga datos seed de forma idempotente."""

    Base.metadata.create_all(bind=motor)
    session = SessionLocal()
    try:
        cliente_1 = obtener_o_crear(
            session,
            Cliente,
            Cliente.documento == "20111222333",
            {
                "nombre": "Agro Sur SRL",
                "documento": "20111222333",
                "email": "contacto@agrosur.test",
            },
        )
        cliente_2 = obtener_o_crear(
            session,
            Cliente,
            Cliente.documento == "20999888777",
            {
                "nombre": "Campo Norte SA",
                "documento": "20999888777",
                "email": "compras@camponorte.test",
            },
        )

        semilla_1 = obtener_o_crear(
            session,
            Semilla,
            Semilla.nombre == "Soja DM 60R23",
            {
                "nombre": "Soja DM 60R23",
                "descripcion": "Variedad de soja de alto rendimiento",
            },
        )
        semilla_2 = obtener_o_crear(
            session,
            Semilla,
            Semilla.nombre == "Maíz AX 7784",
            {
                "nombre": "Maíz AX 7784",
                "descripcion": "Híbrido de maíz para siembra temprana",
            },
        )

        lote_1 = obtener_o_crear(
            session,
            Lote,
            Lote.codigo == "LOT-SOJA-001",
            {
                "codigo": "LOT-SOJA-001",
                "semilla_id": semilla_1.id,
                "kilos_disponibles": 1000.0,
            },
        )
        lote_2 = obtener_o_crear(
            session,
            Lote,
            Lote.codigo == "LOT-MAIZ-001",
            {
                "codigo": "LOT-MAIZ-001",
                "semilla_id": semilla_2.id,
                "kilos_disponibles": 750.0,
            },
        )
        lote_3 = obtener_o_crear(
            session,
            Lote,
            Lote.codigo == "LOT-SOJA-002",
            {
                "codigo": "LOT-SOJA-002",
                "semilla_id": semilla_1.id,
                "kilos_disponibles": 500.0,
            },
        )

        for lote in (lote_1, lote_2, lote_3):
            inventario = session.scalar(
                select(Inventario).where(Inventario.lote_id == lote.id)
            )
            if inventario is None:
                session.add(
                    Inventario(
                        lote_id=lote.id,
                        stock_total=lote.kilos_disponibles,
                        stock_reservado=0,
                    )
                )

        pedido_existente = session.scalar(
            select(Pedido).where(Pedido.codigo == "PED-0001")
        )
        if pedido_existente is None:
            pedido = Pedido(
                codigo="PED-0001",
                cliente_id=cliente_1.id,
                estado=EstadoPedido.BORRADOR,
            )
            session.add(pedido)
            session.flush()
            session.add_all(
                [
                    LineaPedido(
                        pedido_id=pedido.id,
                        lote_id=lote_1.id,
                        kilos=120.0,
                    ),
                    LineaPedido(
                        pedido_id=pedido.id,
                        lote_id=lote_2.id,
                        kilos=80.0,
                    ),
                ]
            )
            session.flush()
            session.refresh(pedido)
            reservar_stock_pedido(session, pedido)
            pedido.estado = EstadoPedido.CONFIRMADO
            session.commit()

        pedido_existente_2 = session.scalar(
            select(Pedido).where(Pedido.codigo == "PED-0002")
        )
        if pedido_existente_2 is None:
            pedido = Pedido(
                codigo="PED-0002",
                cliente_id=cliente_2.id,
                estado=EstadoPedido.BORRADOR,
            )
            session.add(pedido)
            session.flush()
            session.add(
                LineaPedido(
                    pedido_id=pedido.id,
                    lote_id=lote_3.id,
                    kilos=50.0,
                )
            )
            session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    inicializar_base()
    print("✓ Base de datos inicializada")
