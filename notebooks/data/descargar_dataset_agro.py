"""Descarga y prepara la capa cruda (Bronze) con datos REALES de cosechas.

Fuente oficial: **Estimaciones Agrícolas** del Ministerio de Agricultura,
Ganadería y Pesca de Argentina (MAGyP), publicadas como datos abiertos.

    https://datos.magyp.gob.ar/dataset/estimaciones-agricolas

Contiene superficie sembrada/cosechada, producción y rendimiento por cultivo,
campaña, provincia y departamento desde 1969. Es la misma serie que cruza la
Bolsa de Cereales (cuyo portal exige registro y no expone descarga abierta).

Este script baja el CSV completo (~15 MB, ~160.000 filas), lo **acota** a los
cultivos del caso y a las últimas campañas, y guarda el resultado crudo en la
capa `unprocessed/`. NO limpia los datos: el crudo se conserva tal cual (incluye
variantes de cultivo, rendimiento en kg/ha y filas con pérdida de cosecha). Toda
la limpieza ocurre en la capa `processed/` dentro del notebook.

Uso:
    python notebooks/data/descargar_dataset_agro.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# URL de descarga directa del dataset oficial (CSV).
URL_MAGYP = (
    "https://datos.magyp.gob.ar/dataset/9e1e77ba-267e-4eaa-a59f-3296e86b5f36/"
    "resource/95d066e6-8a0f-4a80-b59d-6f28f88eacd5/download/"
    "estimaciones-agricolas-2026-03.csv"
)

# Acotamos el alcance: cultivos del caso y campañas recientes.
CULTIVOS_PATRON = "soja|trigo|maíz|maiz|girasol"
ANIO_DESDE = 2015


def main() -> None:
    destino = Path(__file__).parent / "unprocessed" / "cosecha_agro.csv"
    destino.parent.mkdir(parents=True, exist_ok=True)

    print(f"Descargando dataset oficial del MAGyP...\n  {URL_MAGYP}")
    df = pd.read_csv(URL_MAGYP)
    print(f"✓ Descargado: {len(df):,} filas")

    # Acotar a los cultivos del caso y a las campañas recientes (se conserva crudo).
    mask = (df["cultivo"].str.contains(CULTIVOS_PATRON, case=False, na=False)
            & (df["anio"] >= ANIO_DESDE))
    crudo = df[mask].reset_index(drop=True)

    crudo.to_csv(destino, index=False, encoding="utf-8")
    print(f"✓ Capa cruda (unprocessed/Bronze): {destino}")
    print(f"  {len(crudo):,} filas, {crudo.shape[1]} columnas")
    print(f"  Cultivos crudos: {sorted(crudo['cultivo'].unique())}")


if __name__ == "__main__":
    main()
