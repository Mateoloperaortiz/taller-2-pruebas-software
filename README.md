# Taller 2 de Pruebas de Software

Aplicación de órdenes con Python, Flask y SQLite para estudiar pruebas unitarias,
pruebas de integración y dobles de prueba. Desarrollo de los pasos 0 a 10 del
enunciado, con evidencia de éxito, falla de la dependencia externa y recuperación.

**Entrega:** [informe con todas las respuestas](docs/INFORME.md),
[versión en Word](docs/Taller2_resuelto.docx),
[evidencias de ejecución](evidencias/) y [workflow de CI](.github/workflows/ci.yml).

## Instalación y ejecución

Requiere Python 3.11 o posterior.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

En Windows, activa el entorno con `.venv\Scripts\Activate.ps1` desde PowerShell.
Abre <http://127.0.0.1:5000>. Si el puerto está ocupado, usa `PORT=5055 python app.py`.
La base `orders.db` se crea junto a `app.py`. No se publica en Git.

## Reproducir los escenarios

La entrega queda en el estado del paso 8, con `FakeUserRepository` por defecto.
En macOS y Linux:

```bash
# Pasos 3 a 6: consulta a la API real
USER_REPOSITORY=real python app.py

# Paso 7: excepción intencional en el repositorio real
USER_REPOSITORY=real SIMULATE_USER_API_FAILURE=1 python app.py

# Paso 8: funciona incluso con la falla del repositorio real activada
USER_REPOSITORY=fake SIMULATE_USER_API_FAILURE=1 python app.py
```

Detén cada servidor con Ctrl+C antes de iniciar el siguiente. En PowerShell,
establece las variables con `$env:USER_REPOSITORY="real"` y
`$env:SIMULATE_USER_API_FAILURE="1"`; luego ejecuta `python app.py`.
Para restaurar la API, elimina la variable o cambia su valor a `0`.

La falla se activa mediante una variable para conservar ambas versiones del
ejercicio sin borrar código. El repositorio lanza exactamente
`ConnectionError("User service unavailable")` antes de hacer la petición.

## Pruebas

```bash
# Suite determinista: no necesita internet y bloquea conexiones de red
python -m pytest -m "not external" -v

# Los cuatro archivos pedidos por el taller
python -m pytest test_unit_real_api.py -v
python -m pytest test_integration_real_api.py -v
python -m pytest test_unit_with_stub.py -v
python -m pytest test_integration_with_fake.py -v

# Suite completa, incluida la API real
python -m pytest -v

# Fallas esperadas del paso 7: ambos comandos deben salir con código 1
SIMULATE_USER_API_FAILURE=1 python -m pytest test_unit_real_api.py -v
SIMULATE_USER_API_FAILURE=1 python -m pytest test_integration_real_api.py -v

# Volver a generar los registros de los pasos 6 a 10
python scripts/collect_evidence.py
```

Las pruebas de integración crean una base SQLite temporal por caso y comprueban
la persistencia desde otra sesión. No usan ni borran las órdenes de la app.

El nombre `test_unit_real_api.py` se conserva por trazabilidad con el enunciado:
**su contenido es una prueba de integración**, pues usa API y SQLite reales.
El test con Stub sí aísla todas las dependencias, incluida la sesión de BD.

## Postman

Importa [la colección](postman/Taller2.postman_collection.json) y ejecuta
**Consultar usuario 1**. Verifica HTTP 200, ID 1 y el correo esperado.
También puede ejecutarse con el runner de colecciones de Postman:

```bash
npx --yes newman@6.2.1 run postman/Taller2.postman_collection.json
```

## Integración continua

GitHub Actions instala Python 3.11 y ejecuta el test con Stub, la integración
con Fake y los tests de Flask en cada push o pull request a `main`.
La API externa se verifica por separado para que una caída ajena no determine
el resultado de CI.

## Estructura

```text
app.py                         Formulario Flask e inyección de dependencias
contracts.py                   Contratos de las dependencias de create_order
database.py / models.py         SQLite y entidad Order
order_service.py               Lógica de creación de órdenes
user_repository.py             Repositorios real y Fake
test_*.py / conftest.py         Pruebas y aislamiento
postman/                       Colección del paso 3
docs/                          Informe y respuestas del taller
evidencias/                    Salidas reales y capturas
scripts/collect_evidence.py     Reproducción de las pruebas
.github/workflows/ci.yml        Pipeline completado
```

La notificación se imprime en consola, como en la aplicación base. Esta entrega
es una aplicación didáctica local y no implementa envío real de correos.
