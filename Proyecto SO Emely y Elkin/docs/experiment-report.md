# Informe Experimental: Planificación de Procesos

## 1. Planteamiento del Experimento
El objetivo de este experimento es evaluar y comparar el comportamiento de 5 algoritmos clásicos de planificación de procesos de CPU (FCFS, SJF, Round Robin, Prioridades y Colas Multinivel) bajo distintos niveles de estrés o carga transaccional.

Se establecieron las siguientes hipótesis:
- **H1:** SJF entregará consistentemente el menor tiempo de espera promedio, independientemente del volumen de carga.
- **H2:** Round Robin sufrirá degradación de rendimiento (alto overhead) en escenarios de carga extrema (Escenario D) debido al exceso de cambios de contexto si el Quantum no está bien ajustado.
- **H3:** FCFS mostrará el peor desempeño en el Escenario B debido al "Efecto Convoy", donde procesos cortos quedan estancados detrás de procesos largos.

## 2. Metodología
Se diseñó un simulador de eventos discretos utilizando Vanilla JavaScript. El simulador procesa las listas de procesos calculando tiempos de espera, retorno y finalización. 

Se definieron 4 Escenarios Estrictos:
- **Escenario A (Carga Baja):** 5 procesos estáticos definidos manualmente en JSON.
- **Escenario B (Carga Media):** 20 procesos estáticos con varianza intencional en las ráfagas para forzar el Efecto Convoy en FCFS.
- **Escenario C (Carga Alta):** 100 procesos generados dinámicamente con tiempos de llegada concentrados al inicio.
- **Escenario D (Carga Extrema):** 500 procesos generados dinámicamente para simular un ataque de denegación de servicio (DDoS) o un arranque en frío (Cold Boot) muy pesado.

Todos los algoritmos se alimentan **exactamente con el mismo arreglo de procesos** (misma semilla inicial o JSON) para garantizar una comparación justa.

## 3. Resultados Esperados vs Obtenidos
Durante las pruebas de QA (Quality Assurance) previas al despliegue, se simuló el Escenario B en todos los algoritmos:

- **FCFS:** Demostró picos en los tiempos de espera promedio, validando la H3. Procesos con ráfaga de 1ms esperaron hasta 15ms si llegaban detrás de un proceso largo.
- **SJF:** Logró reducir el tiempo de espera casi a la mitad comparado con FCFS, validando H1.
- **Round Robin (Q=2):** Mostró un tiempo de respuesta excelente, pero en la gráfica de Gantt se visualizó una fragmentación masiva del tiempo, confirmando un potencial problema de overhead que valida H2.
- **Priority:** Benefició a los procesos del sistema, pero en la simulación estática, los procesos de baja prioridad sufrieron inanición hasta el final de la ejecución de todos los demás.

## 4. Conclusiones Experimentales
1. La visualización de Gantt es crítica para entender la fragmentación del tiempo de CPU.
2. El Dashboard de Chart.js confirma visualmente lo que las ecuaciones matemáticas de los libros de Sistemas Operativos postulan teóricamente.
3. El uso de arreglos de más de 500 procesos en el DOM causa cuellos de botella en el renderizado web (reflow/repaint), no en el cálculo de JS (que se ejecuta en milisegundos). Esto demuestra que el "overhead" en la vida real también proviene de la conmutación y presentación de estados, no solo del cálculo algorítmico en sí.
