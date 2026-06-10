
# app.py — Detector de Pose con MediaPipe
# Estructura: 3 capas (Data Layer / Business Logic / Presentation Layer)

import mediapipe as mp
import gradio as gr
import numpy as np


# ─────────────────────────────────────────────────────────────────────────
# CAPA 1 — DATA LAYER
# El modelo se carga una sola vez cuando arranca la aplicación.
# Si lo cargáramos dentro de la función, cada request esperaría la carga.
# ─────────────────────────────────────────────────────────────────────────

modulo_pose    = mp.solutions.pose
modulo_dibujo  = mp.solutions.drawing_utils
estilos_dibujo = mp.solutions.drawing_styles

# TODO: completá los parámetros con los valores que encontraron en la exploración
detector_pose = modulo_pose.Pose(
    static_image_mode=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# ─────────────────────────────────────────────────────────────────────────
# CAPA 2 — BUSINESS LOGIC
# Toda la lógica de procesamiento vive acá, desacoplada de la interfaz.
# Si mañana cambian la UI de Gradio a otra tecnología, esta función no cambia.
# ─────────────────────────────────────────────────────────────────────────

def detectar_pose(imagen_entrada):
    # TODO: peguen aquí la función que terminaron en la Consigna 1
    # Asegúrense de que incluya los TODO que completaron (métricas propias, etc.)
    pass


# ─────────────────────────────────────────────────────────────────────────
# CAPA 3 — PRESENTATION LAYER
# La interfaz declara cómo se ve la app, sin lógica de negocio adentro.
# ─────────────────────────────────────────────────────────────────────────

with gr.Blocks(title="Detector de Pose") as aplicacion:

    gr.Markdown("## Detector de Pose corporal — MediaPipe")
    gr.Markdown(
        "Subí una imagen de una persona y el modelo va a detectar "
        "los 33 puntos clave del esqueleto corporal."
    )

    with gr.Row():
        # TODO: definí los componentes de entrada
        # Pista: gr.Image con type="numpy" y un label descriptivo
        entrada_imagen = None   # reemplazá None por el componente correcto

    with gr.Row():
        # TODO: definí los dos componentes de salida
        # Pista: imagen anotada + cuadro de texto con métricas
        salida_imagen = None    # reemplazá None por el componente correcto
        salida_texto  = None    # reemplazá None por el componente correcto

    boton_analizar = gr.Button("Analizar pose", variant="primary")

    boton_analizar.click(
        fn=detectar_pose,
        inputs=entrada_imagen,
        outputs=[salida_imagen, salida_texto]
    )


if __name__ == "__main__":
    aplicacion.launch()
