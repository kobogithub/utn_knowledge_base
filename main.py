"""Entry point de Firebase Functions para exponer la API FastAPI."""

from __future__ import annotations

from a2wsgi import ASGIMiddleware
from firebase_functions import https_fn
from werkzeug.wrappers import Response

from backend.app import app as api_fastapi

adaptador_wsgi = ASGIMiddleware(api_fastapi)


@https_fn.on_request()
def api(request: https_fn.Request) -> https_fn.Response:
    """Enruta las requests HTTP de Firebase hacia la app FastAPI."""

    return Response.from_app(adaptador_wsgi, request.environ)
