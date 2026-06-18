"""Pruebas básicas de la API."""

from __future__ import annotations


def test_health(client):
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}


def test_ping_api(client):
    respuesta = client.get("/api/v1/ping")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"mensaje": "pong"}
