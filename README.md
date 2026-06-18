# UTN Knowledge Base

Repositorio de materiales prácticos para la materia **Procesamiento Digital de Imágenes** (Tecnicatura Superior en Ciencias de Datos e IA, IFTS24).

El objetivo del proyecto es centralizar laboratorios y ejemplos de visión artificial con ejecución local y opciones de despliegue.

## Backend FastAPI Agro

Este repositorio incluye un backend funcional para gestión de pedidos de semillas en `backend/`.

Estado actual del backend:

- API FastAPI con SQLite + SQLAlchemy sincrónico.
- Dominio implementado: clientes, semillas, lotes, pedidos e inventario.
- Regla crítica implementada: validación de stock y reserva al confirmar pedidos.
- Tests automatizados disponibles y en estado verde.

## Ejecución rápida (desde raíz del repo)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
python -m backend.db.init_db
uvicorn backend.app:app --reload
```

Documentación interactiva: `http://127.0.0.1:8000/docs`

## Verificación manual mínima

```bash
# Salud
curl -s http://127.0.0.1:8000/health

# Ping API v1
curl -s http://127.0.0.1:8000/api/v1/ping
```

## Flujo sugerido de prueba de negocio

1. Crear un cliente (`POST /api/v1/clientes`).
2. Crear una semilla (`POST /api/v1/semillas`).
3. Crear un lote (`POST /api/v1/lotes`).
4. Crear un pedido borrador (`POST /api/v1/pedidos`).
5. Confirmar el pedido (`POST /api/v1/pedidos/{pedido_id}/confirmar`).
6. Verificar inventario reservado (`GET /api/v1/inventario`).

### Instalación local

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Inicializar la base

```bash
cd ..
python -m backend.db.init_db
```

### Ejecutar el servidor

```bash
cd ..
uvicorn backend.app:app --reload
```

La documentación automática queda disponible en `/docs`.

### Ejecutar tests

```bash
pytest backend/tests
```

Resultado esperado actual: `4 passed`.

## Contenido

- Notebooks de aprendizaje progresivo
- Ejercicios con MediaPipe y OpenCV
- Interfaces web con Gradio
- Uso de modelos preentrenados de Hugging Face
- Guías de despliegue y buenas prácticas

## Stack principal

- Python 3.10+
- JupyterLab
- MediaPipe
- OpenCV (headless)
- Gradio
- Transformers (Hugging Face)
- PyTorch (CPU)

## Enfoque de arquitectura (Gradio)

Las apps se organizan en 3 capas:

1. **Data Layer**: carga única del modelo al iniciar.
2. **Business Logic**: funciones puras sin acoplarse a la UI.
3. **Presentation Layer**: interfaz declarativa con Gradio (`Interface` o `Blocks`).

## Estructura sugerida

```text
.
├── notebooks/
│   ├── 01_Entornos_de_Desarrollo.ipynb
│   ├── 02_Control_Volumen_con_Manos.ipynb
│   ├── 03_Integracion_Gradio_y_MediaPipe.ipynb
│   ├── 04_Proyecto_Pose_y_Despliegue.ipynb
│   ├── 05_Modelos_Preentrenados_HuggingFace.ipynb
│   └── 06_Cheatsheet_Desarrollo_Space.ipynb
├── .github/
└── README.md
```

## Cómo empezar

1. Clonar el repositorio.
2. Crear entorno virtual.
3. Instalar dependencias del proyecto.
4. Levantar JupyterLab y ejecutar notebooks.

Ejemplo rápido:

```bash
git clone https://github.com/kobogithub/utn_knowledge_base.git
cd utn_knowledge_base
python -m venv .venv
source .venv/bin/activate
pip install -U pip
# Si existe requirements.txt:
# pip install -r requirements.txt
jupyter lab
```

## Convenciones

- Código, comentarios y docstrings en español.
- Variables y funciones en `snake_case` descriptivo.
- Evitar cargar modelos dentro de funciones que se ejecutan por request.
- En webcam loops con OpenCV: usar `try/finally` para liberar recursos.

## Estado

Repositorio en evolución. Se recomienda revisar periódicamente nuevas prácticas, notebooks y material de apoyo.

## Licencia

Definir licencia del proyecto (por ejemplo, MIT) según política institucional.
