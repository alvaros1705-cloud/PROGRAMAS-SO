// js/data-content.js - Contenido Teórico Reducido e Interactivo

const academicContent = {
    intro: `
        <p>La <strong>Planificación de Procesos</strong> es el mecanismo que utiliza el Sistema Operativo para decidir qué proceso obtiene acceso a la CPU y por cuánto tiempo. Su objetivo es maximizar la eficiencia y mantener una respuesta rápida.</p>
        <p>A continuación, explora los conceptos clave usando las tarjetas interactivas:</p>
    `,
    fundamentals: `
        <div class="grid-3 mt-2">
            <!-- Flip Card 1 -->
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <h3>Scheduler</h3>
                        <p class="text-muted">(Planificador)</p>
                    </div>
                    <div class="flip-card-back">
                        <p><strong>Definición:</strong> Módulo del SO que selecciona el siguiente proceso a ejecutar.</p>
                        <p><strong>Ejemplo:</strong> Como un semáforo que da paso a los autos (procesos) hacia la autopista (CPU).</p>
                    </div>
                </div>
            </div>
            <!-- Flip Card 2 -->
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <h3>Throughput</h3>
                        <p class="text-muted">(Rendimiento)</p>
                    </div>
                    <div class="flip-card-back">
                        <p><strong>Definición:</strong> Cantidad de procesos completados por unidad de tiempo.</p>
                        <p><strong>Ejemplo:</strong> Atender a 50 clientes por hora en un banco.</p>
                    </div>
                </div>
            </div>
            <!-- Flip Card 3 -->
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <h3>Overhead</h3>
                        <p class="text-muted">(Sobrecarga)</p>
                    </div>
                    <div class="flip-card-back">
                        <p><strong>Definición:</strong> Tiempo de CPU desperdiciado en tareas administrativas (ej. Cambio de Contexto).</p>
                        <p><strong>Ejemplo:</strong> El tiempo que tardas en guardar un libro y sacar otro para estudiar.</p>
                    </div>
                </div>
            </div>
        </div>
    `,
    states: `
        <p>Un proceso pasa por varios estados durante su vida:</p>
        <ul style="color: var(--text-secondary); margin-left:20px; line-height: 1.8;">
            <li><span class="badge badge-success">Nuevo</span> Creado, aún no admitido.</li>
            <li><span class="badge badge-warning">Listo</span> Esperando su turno de CPU en memoria.</li>
            <li><span class="badge badge-danger">En Ejecución</span> Ocupando físicamente la CPU.</li>
            <li><span class="badge badge-warning">En Espera</span> Bloqueado, esperando lectura de disco/red.</li>
            <li><span class="badge badge-success">Terminado</span> Ejecución finalizada.</li>
        </ul>
    `,
    criteria: `
        <p>Métricas que buscaremos optimizar:</p>
        <ul style="color: var(--text-secondary); margin-left:20px; line-height: 1.8;">
            <li><strong>Tiempo de Espera:</strong> Tiempo en la cola de listos sin usar CPU. <em>(Queremos minimizarlo)</em>.</li>
            <li><strong>Tiempo de Retorno:</strong> Desde que nace hasta que muere. <em>(Queremos minimizarlo)</em>.</li>
            <li><strong>Uso de CPU:</strong> Porcentaje de tiempo que la CPU está activa. <em>(Queremos maximizarlo al 100%)</em>.</li>
        </ul>
    `,
    metricsCards: `
        <div class="card"><h3 class="card-title">Tiempo de Espera</h3><p>Métrica principal para evaluar un algoritmo. Es la suma de todos los tiempos inactivos en la cola.</p></div>
        <div class="card"><h3 class="card-title">Tiempo de Retorno</h3><p>Tiempo de Espera + Tiempo de Ráfaga de CPU. Indica la velocidad real que percibe el usuario.</p></div>
        <div class="card"><h3 class="card-title">Throughput & CPU</h3><p>Alta utilización de CPU + Alto Throughput = Sistema Optimizado.</p></div>
    `,
    optimization: `
        <p>En el mundo real, los SO optimizan la CPU usando técnicas dinámicas:</p>
        <div class="grid-2 mt-2">
            <div class="card" style="margin-bottom:0;">
                <h3 style="color:var(--accent-primary);">Envejecimiento (Aging)</h3>
                <p>Previene la <strong>Inanición</strong> aumentando la prioridad de los procesos que llevan mucho tiempo esperando.</p>
            </div>
            <div class="card" style="margin-bottom:0;">
                <h3 style="color:var(--accent-primary);">Colas Multinivel Retroalimentadas</h3>
                <p>Mueve los procesos entre distintas colas. Si un proceso consume mucha CPU, se castiga bajándolo de prioridad.</p>
            </div>
        </div>
    `,
    algorithms: `
        <p>Haz clic en cada algoritmo para ver su resumen:</p>
        <div id="alg-accordion" class="mt-2">
            <div class="accordion-item">
                <div class="accordion-header">1. FCFS (First Come, First Served) <span>+</span></div>
                <div class="accordion-body">
                    <p><strong>Definición:</strong> Atiende estricamente en orden de llegada.</p>
                    <p><strong>Desventaja:</strong> Sufre el <em>Efecto Convoy</em> (procesos cortos se atascan tras uno largo).</p>
                </div>
            </div>
            <div class="accordion-item">
                <div class="accordion-header">2. SJF (Shortest Job First) <span>+</span></div>
                <div class="accordion-body">
                    <p><strong>Definición:</strong> Ejecuta primero el proceso con la ráfaga más corta.</p>
                    <p><strong>Ventaja:</strong> Matemáticamente garantiza el menor tiempo de espera promedio.</p>
                </div>
            </div>
            <div class="accordion-item">
                <div class="accordion-header">3. Round Robin (RR) <span>+</span></div>
                <div class="accordion-body">
                    <p><strong>Definición:</strong> Asigna a cada proceso un turno fijo de tiempo llamado <em>Quantum</em>.</p>
                    <p><strong>Característica:</strong> Excelente para sistemas interactivos y equitativo.</p>
                </div>
            </div>
            <div class="accordion-item">
                <div class="accordion-header">4. Prioridades <span>+</span></div>
                <div class="accordion-body">
                    <p><strong>Definición:</strong> Ejecuta al proceso con el número de prioridad más crítico.</p>
                    <p><strong>Riesgo:</strong> Puede causar inanición a procesos de baja prioridad.</p>
                </div>
            </div>
            <div class="accordion-item">
                <div class="accordion-header">5. Colas Multinivel (MLQ) <span>+</span></div>
                <div class="accordion-body">
                    <p><strong>Definición:</strong> Separa procesos en colas distintas (ej. Sistema vs Usuario) usando distintos algoritmos por cola.</p>
                </div>
            </div>
        </div>
    `,
    conclusions: [
        "1. No existe el 'algoritmo perfecto'; la elección depende de si priorizamos el tiempo de respuesta (interactivo) o el throughput (batch).",
        "2. El Overhead del cambio de contexto es el peor enemigo del rendimiento en sistemas modernos.",
        "3. El análisis empírico con Simuladores y Diagramas de Gantt revela problemas invisibles teóricamente, como el Efecto Convoy."
    ],
    recommendations: [
        "Para procesos interactivos, usa siempre un derivado de Round Robin con un Quantum balanceado.",
        "Aplica Aging (Envejecimiento) a todas las colas de prioridad estática."
    ],
    bibliography: `
        <ul style="color: var(--text-secondary); margin-left:20px;">
            <li>Silberschatz, A., Galvin, P., & Gagne, G. (2018). <em>Operating System Concepts</em> (10th ed.). Wiley.</li>
            <li>Tanenbaum, A. S. (2014). <em>Modern Operating Systems</em>. Pearson.</li>
        </ul>
    `
};

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('intro-content').innerHTML = academicContent.intro;
    document.getElementById('fundamentals-content').innerHTML = academicContent.fundamentals;
    document.getElementById('states-content').innerHTML = academicContent.states;
    document.getElementById('criteria-content').innerHTML = academicContent.criteria;
    document.getElementById('metrics-cards').innerHTML = academicContent.metricsCards;
    document.getElementById('optimization-content').innerHTML = academicContent.optimization;
    document.getElementById('algorithms-list').innerHTML = academicContent.algorithms;
    
    const conclList = document.getElementById('conclusions-list');
    conclList.innerHTML = '';
    academicContent.conclusions.forEach(c => {
        let li = document.createElement('li');
        li.textContent = c;
        li.style.marginBottom = '10px';
        conclList.appendChild(li);
    });

    const recList = document.getElementById('recommendations-list');
    recList.innerHTML = '';
    academicContent.recommendations.forEach(r => {
        let li = document.createElement('li');
        li.textContent = r;
        li.style.marginBottom = '10px';
        recList.appendChild(li);
    });

    document.getElementById('bibliography-content').innerHTML = academicContent.bibliography;

    // Lógica para los Acordeones
    const accHeaders = document.querySelectorAll('.accordion-header');
    accHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const item = header.parentElement;
            // Cerrar todos los demás
            document.querySelectorAll('.accordion-item').forEach(i => {
                if(i !== item) i.classList.remove('active');
            });
            // Togglear el actual
            item.classList.toggle('active');
        });
    });
});
