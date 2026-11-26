DASHBOARD UCL 2026/27 — PRIMER PAQUETE

Contenido:
- index.html: dashboard adaptado a móvil.
- config.js: configuración de URL de datos.
- data.json: vacío deliberadamente, sin resultados ficticios.
- scripts/update_data.py: descarga y validación desde API Ninjas.
- .github/workflows/update-data.yml: actualización programada 3 veces al día y manual.

IMPORTANTE: Este paquete es la base funcional, pero NO está conectado aún. Para activar los datos:
1) Crear/obtener una API key gratuita de API Ninjas en https://api-ninjas.com/.
2) En GitHub, en el repositorio, Settings > Secrets and variables > Actions > New repository secret.
3) Nombre: API_NINJAS_KEY; valor: pegar la clave. Guardar.
4) Subir los archivos de este paquete al repositorio (incluida carpeta .github/workflows).
5) En Actions, ejecutar “Actualizar datos UCL” > Run workflow. Verificar que termina verde.
6) Para alojar dashboard/data.json, activar GitHub Pages (Settings > Pages > Deploy from branch, branch main, folder /root) o usar una publicación estática compatible.

No compartir ni publicar la API key. No colocarla en index.html/config.js.

NOTA SOBRE ACODE: abrir index.html como archivo local puede limitar fetch() por restricciones del navegador. Para datos automáticos, se recomienda abrir el dashboard desde el sitio publicado (GitHub Pages), no desde file://.
La app refresca al abrir, al pulsar Actualizar y cada 30 minutos mientras esté abierta. La programación externa de GitHub Actions se ejecuta 3 veces al día.
Los bombos oficiales no se han cargado en este paquete; se incorporarán únicamente tras verificación oficial.
