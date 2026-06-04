# Manual de Usuario - OVA Planificación de Procesos

Bienvenido al Objeto Virtual de Aprendizaje (OVA) diseñado para la comprensión y análisis empírico de la planificación de procesos en Sistemas Operativos.

## 1. Navegación General
La interfaz principal se divide en dos secciones fundamentales:
- **Barra Lateral (Sidebar):** Ubicada a la izquierda, contiene los enlaces a los 9 módulos del aprendizaje. Al hacer clic en cualquiera de ellos, la vista principal hará una transición suave (Fade In) hacia el contenido correspondiente.
- **Área Principal:** Donde se visualiza el contenido académico, el simulador y las gráficas.

## 2. Módulos Teóricos (1 al 5 y 9)
En estos módulos encontrarás toda la fundamentación teórica necesaria. 
- Puedes leer los conceptos.
- Tienes acceso a un Glosario.
- Los algoritmos están explicados con sus pros y contras.
Te recomendamos leer estos módulos antes de utilizar el laboratorio interactivo.

## 3. Uso del Laboratorio Interactivo (Módulo 6)
El laboratorio te permite simular en tiempo real cómo la CPU procesa cargas de trabajo.

**Pasos para simular:**
1. Ve al Módulo 6: "Laboratorio".
2. En el panel de "Configuración", selecciona el **Algoritmo** que deseas probar (FCFS, SJF, RR, Prioridad, MLQ).
3. Si seleccionas **Round Robin (RR)**, aparecerá un campo adicional llamado "Quantum". Ingresa un valor numérico (recomendado entre 1 y 5).
4. Selecciona el **Escenario de Carga**:
   - **Carga Baja (A):** 5 procesos. Ideal para ver paso a paso.
   - **Carga Media (B):** 20 procesos.
   - **Carga Alta (C):** 100 procesos generados dinámicamente.
   - **Carga Extrema (D):** 500 procesos generados dinámicamente.
5. Haz clic en **"Ejecutar Simulación"**.
6. Observa el estado, el Diagrama de Gantt animado y la tabla de procesos actualizada.

*Nota:* Para escenarios mayores a 100 procesos, la interfaz limitará el renderizado visual de la tabla y el diagrama de Gantt para evitar bloqueos del navegador (congelamientos), pero los cálculos estadísticos tomarán en cuenta el 100% de los procesos.

## 4. Uso del Dashboard Analítico (Módulo 7)
Inmediatamente después de ejecutar una simulación, navega al Módulo 7 para ver los resultados estadísticos:
- El gráfico de **Tiempos** te mostrará el promedio de Espera y Retorno en barras comparativas.
- El gráfico de **Rendimiento** te mostrará el Throughput (multiplicado por 100 para ser visible en la escala) y el porcentaje de Utilización de la CPU.

## 5. Módulo de Evaluación (Módulo 8)
- Haz clic en "Comenzar Evaluación".
- Responde a las 20 preguntas seleccionando la opción correcta.
- Al finalizar, haz clic en "Enviar Respuestas".
- El sistema te mostrará tu puntaje sobre 20, tu porcentaje de éxito y una recomendación personalizada basada en tu desempeño.
