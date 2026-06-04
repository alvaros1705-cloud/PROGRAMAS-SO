# Reporte de QA (Quality Assurance) y Optimización

## 1. Pruebas QA Realizadas

### Pruebas Funcionales
- **Algoritmos:** Se verificó matemáticamente que FCFS respeta la cola estricta y que RR reparte el tiempo según el quantum establecido. El overhead de cambios de contexto es visible.
- **Simulador:** El paso de parámetros de la UI a los algoritmos (`app.js` -> `algorithms.js` -> `simulator.js`) ocurre sin pérdida de datos.
- **Gráficos:** El disparador de eventos personalizados (`simulationCompleted`) inyecta correctamente el `throughput` y `waiting time` en la instancia de Chart.js.

### Pruebas Visuales y de Navegación
- **Layout:** El Sidebar actúa correctamente tanto en Desktop (fijo) como en Mobile (stack vertical superior).
- **Smooth Scrolling:** La transición entre los 9 módulos oculta y muestra los contenidos a través de `display: none` y clases activas sin necesidad de recargar el navegador, garantizando la experiencia de Single Page Application (SPA).

### Pruebas Responsive
- **Media Queries (992px y 768px):** Ajustan las grillas (`.grid-3` a `.grid-2` a `1fr`).
- **Tablas en Móvil:** Se aplicó CSS especial para transformar la tabla de procesos en un formato de "tarjetas" legibles en pantallas pequeñas mediante `display: block` y pseudo-elementos (`::before`).

## 2. Optimizaciones Implementadas

- **Rendimiento del DOM:** En escenarios masivos (Escenario D con 500 procesos), el DOM intentaría crear 500 filas de tabla y potencialmente cientos o miles de nodos `<div>` para el Gantt. Esto congelaría el hilo principal de JavaScript. Se implementó un "limitador de renderizado visual" que corta la visualización a los primeros 100/200 procesos, mientras que el cálculo estadístico y matemático se realiza sobre la totalidad de los 500 procesos.
- **Modularización:** El código Vanilla JS se separó en `app.js` (UI), `algorithms.js` (matemática), `simulator.js` (DOM) y `charts.js` (Dashboard).
- **Lazy Content Injection:** El masivo texto académico (3800 palabras) se almacena en un archivo separado (`data-content.js`) y se inyecta en la estructura de `index.html` después de cargar el DOM inicial, para no bloquear el First Contentful Paint (FCP).

## 3. Estado Final
[X] Sin errores críticos en la consola JS.
[X] Navegación fluida.
[X] Cálculos algorítmicos precisos (verificados con casos teóricos clásicos).
