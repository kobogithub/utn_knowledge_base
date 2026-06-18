# CLAUDE.md — UTN Knowledge Base

## Contexto

Este repositorio contiene material de laboratorio para la materia **Procesamiento Digital de Imágenes** de la Tecnicatura Superior en Ciencias de Datos e IA (IFTS24). Conviven notebooks de visión artificial, interfaces web con Gradio y modelos preentrenados de Hugging Face.

## Prioridad actual

La prioridad principal de esta iteración es implementar el backend **FastAPI Agro** definido en `PLAN.md`, dentro de la carpeta `backend/`.

Orden de prioridad:

1. FastAPI + SQLite + SQLAlchemy sincrónico.
2. Dominio de negocio: clientes, semillas, lotes, pedidos e inventario.
3. Reglas críticas: validación de stock y reserva al confirmar pedidos.
4. Datos de ejemplo idempotentes y tests básicos de API/negocio.

Si hay conflicto entre tareas, priorizar avances del backend antes que nuevas extensiones en notebooks o demos.

## Stack principal

- MediaPipe para detección de landmarks de manos, cara y pose.
- OpenCV headless para procesamiento de imágenes y video.
- Gradio para interfaces web interactivas.
- Hugging Face Transformers para clasificación, zero-shot y detección.
- PyTorch CPU como backend de inferencia.
- JupyterLab como entorno de ejecución de notebooks.

## Convenciones de código

### Idioma

- Comentarios, docstrings y nombres de variables en español.
- Nombres de funciones y variables en `snake_case` descriptivo en español.
- Mensajes de consola con prefijo `✓` para éxito y `✗` para error.

### Apps Gradio

Seguir siempre el patrón de 3 capas:

1. Capa de datos: carga única del modelo al iniciar.
2. Capa de lógica: función pura, sin referencias a Gradio.
3. Capa de presentación: interfaz declarativa con `gr.Blocks`.

### MediaPipe

- Instanciar el detector una sola vez fuera del loop o función de procesamiento.
- Usar `static_image_mode=True` para imágenes sueltas y `False` para video.
- Trabajar siempre sobre una copia de la imagen original antes de dibujar landmarks.
- Convertir coordenadas normalizadas a píxeles multiplicando por ancho y alto.

### Loops de webcam

- Envolver siempre el loop en `try / finally` para liberar `captura.release()`.
- Aplicar cambios al sistema operativo cada N frames, no en cada frame.
- Usar suavizado exponencial para valores continuos como volumen o posición.

## Qué generar y qué evitar

- Generar código autocontenido que corra en una celda de Jupyter sin dependencias externas no declaradas.
- Generar funciones con docstring en español explicando parámetros y retorno.
- Evitar importar dentro de funciones salvo que sea necesario por conflictos de estado.
- Evitar cargar modelos dentro de funciones que se llaman en cada request.
- Evitar comentarios que repiten lo que el nombre ya dice.

## Instrucciones operativas para Claude

- Antes de editar, identificar el archivo, símbolo o comportamiento más cercano al problema.
- Mantener cambios pequeños, locales y verificables.
- Si se crea o modifica código, validar el resultado con la comprobación más barata y específica disponible.
- No revertir cambios del usuario ni tocar archivos no relacionados.
- No asumir arquitecturas nuevas si el plan ya define el alcance.

## Referencias útiles

- `PLAN.md` como fuente principal del alcance del backend.
- `.github/copilot-instructions.md` como referencia de convenciones del repositorio.
- `README.md` para la documentación de uso local.