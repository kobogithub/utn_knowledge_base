"""Pruebas de negocio para pedidos y stock."""

from __future__ import annotations


def crear_datos_base(cliente):
    respuesta_cliente = cliente.post(
        "/api/v1/clientes",
        json={
            "nombre": "Cliente Prueba",
            "documento": "30111222333",
        },
    )
    assert respuesta_cliente.status_code == 201
    cliente_id = respuesta_cliente.json()["id"]

    respuesta_semilla = cliente.post(
        "/api/v1/semillas",
        json={"nombre": "Soja Test", "descripcion": "Semilla de prueba"},
    )
    assert respuesta_semilla.status_code == 201
    semilla_id = respuesta_semilla.json()["id"]

    respuesta_lote = cliente.post(
        "/api/v1/lotes",
        json={
            "codigo": "LOT-TEST-001",
            "semilla_id": semilla_id,
            "kilos_disponibles": 100.0,
        },
    )
    assert respuesta_lote.status_code == 201
    lote_id = respuesta_lote.json()["id"]

    return cliente_id, lote_id


def test_crear_y_confirmar_pedido(client):
    cliente_id, lote_id = crear_datos_base(client)

    respuesta_pedido = client.post(
        "/api/v1/pedidos",
        json={
            "cliente_id": cliente_id,
            "codigo": "PED-TEST-001",
            "lineas": [{"lote_id": lote_id, "kilos": 25.0}],
        },
    )
    assert respuesta_pedido.status_code == 201
    assert respuesta_pedido.json()["estado"] == "borrador"

    pedido_id = respuesta_pedido.json()["id"]
    respuesta_confirmar = client.post(f"/api/v1/pedidos/{pedido_id}/confirmar")
    assert respuesta_confirmar.status_code == 200
    assert respuesta_confirmar.json()["estado"] == "confirmado"

    respuesta_inventario = client.get("/api/v1/inventario")
    assert respuesta_inventario.status_code == 200
    inventario = respuesta_inventario.json()[0]
    assert inventario["stock_reservado"] == 25.0
    assert inventario["stock_disponible"] == 75.0


def test_rechaza_stock_insuficiente(client):
    cliente_id, lote_id = crear_datos_base(client)

    respuesta_pedido = client.post(
        "/api/v1/pedidos",
        json={
            "cliente_id": cliente_id,
            "codigo": "PED-TEST-002",
            "lineas": [{"lote_id": lote_id, "kilos": 250.0}],
        },
    )
    assert respuesta_pedido.status_code == 400
    assert "Stock insuficiente" in respuesta_pedido.json()["detail"]
