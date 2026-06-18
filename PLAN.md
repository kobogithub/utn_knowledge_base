## Plan: Backend FastAPI Agro

Construir un backend nuevo dentro del repositorio usando FastAPI + SQLite + SQLAlchemy sincrónico, orientado al caso de uso de pedidos de lotes de semilla. El alcance incluye entidades de clientes, semillas, lotes, pedidos e inventario, más datos de ejemplo y tests básicos, evitando complejidad innecesaria como async, autenticación o migraciones completas en esta primera iteración.

**Steps**
1. Fase 1: base del proyecto. Crear la carpeta /home/kobo/github/personal/utn_knowledge_base/backend con una estructura consistente para FastAPI: app principal, configuración, conexión SQLite, modelos ORM, esquemas Pydantic, servicios, routers y tests. Esta fase desbloquea todo lo demás.
2. Definir el punto de entrada de la API en /home/kobo/github/personal/utn_knowledge_base/backend/app.py con metadata de FastAPI, ruta de salud y registro del router v1. Mantenerlo simple y listo para correr con uvicorn.
3. Centralizar configuración en /home/kobo/github/personal/utn_knowledge_base/backend/config.py y /home/kobo/github/personal/utn_knowledge_base/backend/.env.example. Incluir la URL SQLite, nombre de app y flags mínimos. Excluir de alcance settings avanzados, secrets y múltiples ambientes.
4. Implementar la capa de base de datos en /home/kobo/github/personal/utn_knowledge_base/backend/database.py con engine, SessionLocal y Base de SQLAlchemy 2 en modo sincrónico. Agregar dependencia get_db para inyección en endpoints. Esta decisión reduce fricción con SQLite y simplifica tests.
5. Fase 2: modelado del dominio. Crear modelos ORM para Cliente, Semilla, Lote, Pedido, LineaPedido e Inventario. Modelar relaciones mínimas: un cliente tiene muchos pedidos; un pedido tiene muchas líneas; una línea referencia un lote; un lote pertenece a una semilla; inventario referencia a un lote. Mantener MovimientoInventario fuera del primer corte salvo que aparezca como necesidad de negocio inmediata.
6. Definir los esquemas Pydantic en la carpeta schemas para create/read/update. Priorizar respuestas claras y validaciones básicas: cantidades mayores que cero, estados válidos, fechas opcionales y consistencia entre stock disponible y reservado.
7. Fase 3: servicios y reglas de negocio. Implementar servicios separados para semillas, lotes, pedidos e inventario. Las reglas críticas del primer corte son: no permitir crear líneas de pedido con más kilos que el stock disponible, reservar stock al confirmar pedido y exponer estado del pedido. Reutilizar funciones puras donde sea posible para facilitar testing.
8. Crear endpoints REST organizados en /home/kobo/github/personal/utn_knowledge_base/backend/api/v1 con un router agregador y recursos por dominio. Alcance recomendado: GET y POST para clientes, semillas, lotes y pedidos; GET para inventario; endpoint específico para confirmar pedido si se quiere separar la transición de estado del alta inicial.
9. Fase 4: datos de ejemplo. Crear un script de inicialización en /home/kobo/github/personal/utn_knowledge_base/backend/db/init_db.py que cree tablas y cargue datos semilla realistas del agro: clientes de ejemplo, variedades de semilla, lotes con kilos disponibles y pedidos de muestra en distintos estados. La semilla debe ser idempotente para poder correrse varias veces sin duplicar registros.
10. Preparar dependencias del proyecto con /home/kobo/github/personal/utn_knowledge_base/backend/requirements.txt o, si se prefiere, pyproject.toml como única fuente. Para este primer corte, requirements.txt es suficiente y más directo. Incluir FastAPI, uvicorn, SQLAlchemy, pydantic, python-dotenv, pytest y httpx o TestClient según la estrategia elegida.
11. Fase 5: testing. Crear tests básicos en /home/kobo/github/personal/utn_knowledge_base/backend/tests para validar arranque de la app, listado de recursos, creación de pedido y rechazo cuando el stock es insuficiente. Usar una base SQLite separada para tests o una variante temporal para no contaminar los datos de ejemplo.
12. Actualizar /home/kobo/github/personal/utn_knowledge_base/README.md para documentar cómo instalar dependencias, inicializar la base, cargar seeds, correr el servidor y consultar la documentación automática. Mantener la documentación enfocada en uso local.
13. Ajustar /home/kobo/github/personal/utn_knowledge_base/.gitignore para excluir archivos .db, .env, caches de pytest y artefactos Python. Esto depende de si el archivo ya existe; si no existe, crearlo como parte del backend.
14. Verificación final. Probar creación de tablas, seed, arranque del servidor, acceso a /docs y ejecución de tests. Si todo funciona, dejar el backend listo para iterar sobre autenticación, filtros o despliegue en una segunda etapa.

**Relevant files**
- /home/kobo/github/personal/utn_knowledge_base/README.md - documentar instalación, ejecución y seed del backend.
- /home/kobo/github/personal/utn_knowledge_base/.github/copilot-instructions.md - referencia de convenciones locales de idioma y estilo.
- /home/kobo/github/personal/utn_knowledge_base/backend/app.py - punto de entrada FastAPI a crear.
- /home/kobo/github/personal/utn_knowledge_base/backend/config.py - configuración central a crear.
- /home/kobo/github/personal/utn_knowledge_base/backend/database.py - engine, sesión y Base a crear.
- /home/kobo/github/personal/utn_knowledge_base/backend/models/cliente.py - modelo Cliente a crear.
- /home/kobo/github/personal/utn_knowledge_base/backend/models/semilla.py - modelos Semilla y Lote a crear.
- /home/kobo/github/personal/utn_knowledge_base/backend/models/pedido.py - modelos Pedido y LineaPedido a crear.
- /home/kobo/github/personal/utn_knowledge_base/backend/models/inventario.py - modelo Inventario a crear.
- /home/kobo/github/personal/utn_knowledge_base/backend/schemas/ - esquemas Pydantic a crear.
- /home/kobo/github/personal/utn_knowledge_base/backend/services/ - reglas de negocio a crear.
- /home/kobo/github/personal/utn_knowledge_base/backend/api/v1/ - routers REST a crear.
- /home/kobo/github/personal/utn_knowledge_base/backend/db/init_db.py - inicialización y carga de datos de ejemplo.
- /home/kobo/github/personal/utn_knowledge_base/backend/tests/ - tests de API y negocio a crear.
- /home/kobo/github/personal/utn_knowledge_base/.gitignore - excluir SQLite, entorno y caches.

**Verification**
1. Instalar dependencias del backend y verificar que la app importe sin errores.
2. Ejecutar el script de inicialización de base y confirmar que crea tablas y datos de ejemplo sin duplicarlos en una segunda corrida.
3. Levantar uvicorn apuntando a la app principal y validar la ruta de salud y la UI de Swagger en /docs.
4. Probar manualmente el flujo base: listar semillas y lotes, crear pedido, confirmar pedido, verificar reserva de stock en inventario.
5. Ejecutar pytest sobre /home/kobo/github/personal/utn_knowledge_base/backend/tests y validar al menos los casos felices y el rechazo por stock insuficiente.

**Decisions**
- Incluye: FastAPI, SQLite, SQLAlchemy sincrónico, seed de ejemplo, tests básicos, documentación local.
- Excluye de este primer corte: autenticación, usuarios, despliegue, Alembic, background jobs, cache, permisos y panel administrativo.
- Se recomienda modelar inventario por lote desde el inicio porque es la pieza que sostiene la validación de pedidos.
- Se recomienda separar creación de pedido de confirmación de pedido si se quiere reflejar el flujo de reserva de stock con más claridad.

**Further Considerations**
1. Si querés un primer corte todavía más corto, se puede dejar LineaPedido e Inventario pero sin endpoint de update general y solo con confirmación de pedido.
2. Si más adelante el proyecto crece, el siguiente salto natural es agregar Alembic y migrar de requirements.txt a pyproject.toml.
3. Si el backend se va a consumir desde notebooks o una UI web, conviene prever CORS y una convención estable de payloads desde el inicio.