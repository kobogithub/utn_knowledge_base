"""
Encuentro 4 — API de Monitoreo de Cultivos
Python, Datos e Ingeniería de IA Aplicada · UTN Rosario

Correr:
    uvicorn app_cultivos:app --reload
Documentación:
    http://localhost:8000/docs
"""
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
from datetime import datetime

# ── Logging ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("api.cultivos")

# ── Modelos Pydantic ──────────────────────────────────────

class ParcelaIn(BaseModel):
    nombre: str = Field(..., min_length=2, example="El Ombú")
    cultivo: str = Field(..., example="soja")
    superficie_ha: float = Field(..., gt=0, description="Hectáreas")
    zona: Literal["norte", "sur", "este", "oeste"]

class LecturaSensorIn(BaseModel):
    parcela_id: int
    tipo: Literal["temperatura", "humedad_suelo", "ph", "lluvia"]
    valor: float
    unidad: str

    @validator("valor")
    def rango_valido(cls, v, values):
        rangos = {
            "temperatura":   (-20, 60),
            "humedad_suelo": (0, 100),
            "ph":            (0, 14),
            "lluvia":        (0, 500),
        }
        tipo = values.get("tipo")
        if tipo in rangos:
            lo, hi = rangos[tipo]
            if not lo <= v <= hi:
                raise ValueError(f"{tipo} debe estar en [{lo}, {hi}], recibido {v}")
        return v

class PrediccionIn(BaseModel):
    parcela_id: int
    modelo: Literal["stress_hidrico", "riesgo_helada", "rendimiento"]

# ── Estado en memoria (en producción: reemplazar con DB) ──
parcelas: dict = {}
lecturas: list = []
alertas: list = []
_ids = {"parcela": 1, "alerta": 1}

UMBRALES = {
    "temperatura":   {"warning": 38.0, "crítico": 45.0},
    "humedad_suelo": {"warning": 20.0, "crítico": 10.0},  # bajos son críticos
    "ph":            {"warning": 5.0,  "crítico": 4.0},   # bajos son críticos
}

# ── Aplicación ────────────────────────────────────────────
app = FastAPI(
    title="API de Monitoreo de Cultivos",
    description="""
## Sistema Inteligente de Monitoreo Agropecuario

Permite:
- Gestionar **parcelas** y sus cultivos
- Registrar **lecturas de sensores** (temperatura, humedad, pH, lluvia)
- Generar **alertas automáticas** cuando los valores superan umbrales
- Obtener **predicciones de IA** sobre estado de los cultivos
    """,
    version="1.0.0",
    contact={"name": "UTN Rosario — Ingeniería de IA Aplicada"},
)


@app.exception_handler(Exception)
async def handler_global(request: Request, exc: Exception):
    logger.error("Error no manejado en %s: %s", request.url, exc)
    return JSONResponse(
        status_code=500,
        content={"error": "error_interno", "detalle": str(exc)},
    )


# ── Endpoints: Parcelas ───────────────────────────────────

@app.post("/parcelas", status_code=201, tags=["Parcelas"],
          summary="Registrar nueva parcela")
def crear_parcela(p: ParcelaIn):
    id_p = _ids["parcela"]
    parcelas[id_p] = {"id": id_p, **p.model_dump()}
    _ids["parcela"] += 1
    logger.info("Parcela creada | id=%d nombre=%s cultivo=%s", id_p, p.nombre, p.cultivo)
    return parcelas[id_p]


@app.get("/parcelas", tags=["Parcelas"], summary="Listar parcelas")
def listar_parcelas(zona: Optional[str] = None, cultivo: Optional[str] = None):
    result = list(parcelas.values())
    if zona:
        result = [p for p in result if p["zona"] == zona]
    if cultivo:
        result = [p for p in result if p["cultivo"] == cultivo]
    return {"total": len(result), "parcelas": result}


@app.get("/parcelas/{parcela_id}", tags=["Parcelas"], summary="Obtener parcela por ID")
def obtener_parcela(parcela_id: int):
    if parcela_id not in parcelas:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "parcela_no_encontrada",
                "id": parcela_id,
                "sugerencia": "Consultá GET /parcelas para ver las disponibles",
            },
        )
    return parcelas[parcela_id]


# ── Endpoints: Sensores ───────────────────────────────────

@app.post("/sensores", status_code=201, tags=["Sensores"],
          summary="Registrar lectura de sensor")
def registrar_lectura(lectura: LecturaSensorIn):
    if lectura.parcela_id not in parcelas:
        raise HTTPException(404, detail=f"Parcela {lectura.parcela_id} no encontrada")

    registro = {**lectura.model_dump(), "timestamp": datetime.now().isoformat()}
    lecturas.append(registro)
    logger.info(
        "Lectura | parcela=%d tipo=%-15s valor=%.2f %s",
        lectura.parcela_id, lectura.tipo, lectura.valor, lectura.unidad
    )

    _evaluar_umbrales(lectura)
    return registro


@app.get("/sensores", tags=["Sensores"], summary="Listar lecturas de sensores")
def listar_lecturas(
    parcela_id: Optional[int] = None,
    tipo: Optional[str] = None,
):
    result = lecturas
    if parcela_id:
        result = [l for l in result if l["parcela_id"] == parcela_id]
    if tipo:
        result = [l for l in result if l["tipo"] == tipo]
    return {"total": len(result), "lecturas": result}


def _evaluar_umbrales(lectura: LecturaSensorIn):
    if lectura.tipo not in UMBRALES:
        return

    sensores_inversos = {"humedad_suelo", "ph"}  # valores bajos son problemáticos

    for nivel, umbral in UMBRALES[lectura.tipo].items():
        supera = (
            lectura.valor <= umbral
            if lectura.tipo in sensores_inversos
            else lectura.valor >= umbral
        )
        if supera:
            id_a = _ids["alerta"]
            alerta = {
                "id": id_a,
                "parcela_id": lectura.parcela_id,
                "tipo": f"{lectura.tipo}_fuera_de_rango",
                "nivel": nivel,
                "mensaje": (
                    f"{lectura.tipo} = {lectura.valor} {lectura.unidad} "
                    f"(umbral {nivel}: {umbral})"
                ),
                "timestamp": datetime.now().isoformat(),
                "resuelta": False,
            }
            alertas.append(alerta)
            _ids["alerta"] += 1
            logger.warning("ALERTA %s | parcela=%d | %s",
                           nivel.upper(), lectura.parcela_id, alerta["mensaje"])
            break  # registrar solo el nivel más severo


# ── Endpoints: Alertas ────────────────────────────────────

@app.get("/alertas", tags=["Alertas"], summary="Listar alertas")
def listar_alertas(
    nivel: Optional[str] = None,
    resuelta: Optional[bool] = None,
    parcela_id: Optional[int] = None,
):
    result = alertas
    if nivel:
        result = [a for a in result if a["nivel"] == nivel]
    if resuelta is not None:
        result = [a for a in result if a["resuelta"] == resuelta]
    if parcela_id:
        result = [a for a in result if a["parcela_id"] == parcela_id]
    return {"total": len(result), "alertas": result}


@app.patch("/alertas/{alerta_id}/resolver", tags=["Alertas"],
           summary="Marcar alerta como resuelta")
def resolver_alerta(alerta_id: int):
    for a in alertas:
        if a["id"] == alerta_id:
            a["resuelta"] = True
            logger.info("Alerta resuelta | id=%d", alerta_id)
            return a
    raise HTTPException(404, detail=f"Alerta {alerta_id} no encontrada")


# ── Endpoints: Predicciones IA ────────────────────────────

@app.post("/prediccion", tags=["IA"],
          summary="Predicción de estado del cultivo")
def predecir(req: PrediccionIn):
    if req.parcela_id not in parcelas:
        raise HTTPException(404, detail=f"Parcela {req.parcela_id} no encontrada")

    ultimas = [l for l in lecturas if l["parcela_id"] == req.parcela_id]
    if not ultimas:
        raise HTTPException(
            400,
            detail="No hay lecturas de sensores para esta parcela. "
                   "Registrá al menos una lectura antes de pedir predicciones.",
        )

    # Simulación del modelo de IA
    # En producción: llamada a modelo real, embeddings, ML, etc.
    resultados = {
        "stress_hidrico": {
            "riesgo": "bajo",
            "confianza": 0.85,
            "recomendacion": "Sin acción requerida. Monitorear cada 48 hs.",
        },
        "riesgo_helada": {
            "riesgo": "medio",
            "confianza": 0.72,
            "recomendacion": "Monitorear temperatura nocturna. Activar sistema anti-helada si baja de 3°C.",
        },
        "rendimiento": {
            "estimado_tn_ha": 3.8,
            "confianza": 0.68,
            "recomendacion": "Condiciones favorables. Rendimiento esperado dentro del promedio zonal.",
        },
    }

    logger.info("Predicción | parcela=%d modelo=%s lecturas_analizadas=%d",
                req.parcela_id, req.modelo, len(ultimas))

    return {
        "parcela_id": req.parcela_id,
        "parcela_nombre": parcelas[req.parcela_id]["nombre"],
        "modelo": req.modelo,
        "resultado": resultados[req.modelo],
        "lecturas_analizadas": len(ultimas),
        "timestamp": datetime.now().isoformat(),
    }
