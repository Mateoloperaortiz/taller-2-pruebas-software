# Evidencias de ejecución

Registros y capturas obtenidos el 23 de septiembre de 2026 al ejecutar la solución.
Las imágenes muestran la app local en el navegador; no son imágenes de ejemplo
extraídas del enunciado. Los registros del paso 7 contienen fallos intencionales.

| Paso | Evidencia |
| --- | --- |
| 0 | [Repositorio de la entrega](https://github.com/Mateoloperaortiz/taller-2-pruebas-software) |
| 3 | [Colección Postman ejecutada con Newman](paso03_postman.txt) y [respuesta recibida](paso03_usuario1.json) |
| 5 | [Orden con API real](paso05_app_real.png), [reinicio de Flask](paso05_persistencia_reinicio.png) y [consulta SQLite](paso05_sqlite.json) |
| 6 | [Test llamado unitario](paso06_unit_real.txt) y [test de integración](paso06_integration_real.txt) |
| 7 | [Falla del primer test](paso07_unit_falla.txt), [falla del segundo](paso07_integration_falla.txt), [captura de la app](paso07_app_falla.png) y [verificación de filas](paso07_app.txt) |
| 8 | [App con Fake](paso08_app_fake.png) y [orden en SQLite](paso08_sqlite.json) |
| 9 | [Pruebas unitarias con Stub](paso09_stub.txt) |
| 10 | [Integración con Fake](paso10_fake.txt) |
| CI local | [Suite sin red](suite_sin_red.txt) y [resumen del entorno](resumen.json) |

Para regenerar los logs de pytest: `python scripts/collect_evidence.py`.
Para regenerar la consulta Postman, ejecutar el comando Newman del README.
Las capturas se tomaron al crear las órdenes desde el formulario; las bases
empleadas para esas demostraciones no se suben a GitHub.
