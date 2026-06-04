// js/simulator.js - Motor del Simulador, Integración de API, Gantt e Historial CRUD

let currentExperimentData = null; // Guarda los resultados del experimento activo
let isBackendOnline = false;

document.addEventListener('DOMContentLoaded', () => {
    checkBackendConnection();

    // Elementos del laboratorio
    const btnRun = document.getElementById('btn-run');
    const btnReset = document.getElementById('btn-reset');
    const btnRefreshHistory = document.getElementById('btn-refresh-history');
    
    // Selectores de Algoritmo en Gantt y Tabla
    const ganttAlgoSelect = document.getElementById('gantt-algo-select');
    const tableAlgoSelect = document.getElementById('table-algo-select');

    if (btnRun) {
        btnRun.addEventListener('click', runExperiment);
    }
    if (btnReset) {
        btnReset.addEventListener('click', resetSimulation);
    }
    if (btnRefreshHistory) {
        btnRefreshHistory.addEventListener('click', loadHistoryList);
    }

    if (ganttAlgoSelect) {
        ganttAlgoSelect.addEventListener('change', () => {
            if (currentExperimentData) {
                const algo = ganttAlgoSelect.value;
                const algoResult = currentExperimentData.results[algo];
                if (algoResult) {
                    renderGantt(algoResult.timeline);
                }
            }
        });
    }

    if (tableAlgoSelect) {
        tableAlgoSelect.addEventListener('change', () => {
            if (currentExperimentData) {
                const algo = tableAlgoSelect.value;
                const algoResult = currentExperimentData.results[algo];
                if (algoResult) {
                    renderTable(algoResult.processes);
                }
            }
        });
    }
    
    // Cargar historial si cambia de pestaña a Historial
    const dbNavLink = document.querySelector('a[data-target="module-db"]');
    if (dbNavLink) {
        dbNavLink.addEventListener('click', loadHistoryList);
    }
});

/**
 * Verifica la conexión con el servidor Flask.
 */
async function checkBackendConnection() {
    const badge = document.getElementById('db-status-badge');
    const warning = document.getElementById('connection-warning');
    
    try {
        const health = await SimulatorAPI.checkHealth();
        if (health.status === 'ok' && health.mysql_connected) {
            isBackendOnline = true;
            if (badge) {
                badge.innerText = 'Servidor: Conectado (MySQL)';
                badge.className = 'badge badge-success mb-3 text-center';
            }
            if (warning) warning.style.display = 'none';
        } else {
            setOfflineUI(badge, warning, health.mysql_error || 'MySQL desconectado');
        }
    } catch (e) {
        setOfflineUI(badge, warning, e.message);
    }
}

function setOfflineUI(badge, warning, reason) {
    isBackendOnline = false;
    if (badge) {
        badge.innerText = 'Servidor: Desconectado (Offline)';
        badge.className = 'badge badge-danger mb-3 text-center';
    }
    if (warning) {
        warning.style.display = 'block';
        warning.innerHTML = `⚠️ El backend Python o MySQL no están activos (${reason}). Se ejecutará en modo local sin persistencia en BD.`;
    }
}

/**
 * Genera procesos para cargas de trabajo C y D en modo local (fallback).
 */
function generateProcessesLocal(count) {
    let procs = [];
    for (let i = 1; i <= count; i++) {
        procs.push({
            pid: `P${i}`,
            arrivalTime: Math.floor(Math.random() * (count * 2)),
            burstTime: Math.floor(Math.random() * 15) + 1,
            priority: Math.floor(Math.random() * 5) + 1
        });
    }
    return procs.sort((a, b) => a.arrivalTime - b.arrivalTime);
}

/**
 * Carga o clona procesos del escenario (modo local).
 */
function getProcessesLocal(scenarioId) {
    if (typeof GLOBAL_SCENARIOS === 'undefined') {
        console.error("GLOBAL_SCENARIOS no definido. Revisa scenarios.js");
        return [];
    }
    if (scenarioId === 'C') return generateProcessesLocal(100);
    if (scenarioId === 'D') return generateProcessesLocal(500);

    let data = GLOBAL_SCENARIOS[scenarioId];
    if (!data) return [];
    return JSON.parse(JSON.stringify(data));
}

/**
 * Ejecuta el Experimento Comparativo.
 */
async function runExperiment() {
    const statusBox = document.getElementById('execution-status');
    const scenario = document.getElementById('scenario-select').value;
    const quantum = parseInt(document.getElementById('quantum-input').value) || 2;
    const expNameInput = document.getElementById('exp-name-input').value.trim();
    const expName = expNameInput || `Comparativa Escenario ${scenario}`;

    if (statusBox) {
        statusBox.innerHTML = '<p class="text-primary"><span class="spinner"></span> Procesando experimento...</p>';
    }

    try {
        if (isBackendOnline) {
            // --- MODO ONLINE (FLASK + MYSQL) ---
            const response = await SimulatorAPI.runExperiment(scenario, quantum, expName);
            currentExperimentData = response;
            statusBox.innerHTML = '<p style="color:var(--accent-success); font-weight:bold;">✓ Experimento guardado en MySQL con éxito.</p>';
            loadHistoryList(); // Recargar historial automáticamente
        } else {
            // --- MODO OFFLINE (FALLBACK LOCAL) ---
            const localProcs = getProcessesLocal(scenario);
            if (localProcs.length === 0) throw new Error("No hay procesos en el escenario.");
            
            // Ejecutar localmente todos los algoritmos
            const results = {};
            results["FCFS"] = SchedulerAlgorithms.fcfs(localProcs);
            results["SJF"] = SchedulerAlgorithms.sjf(localProcs);
            results["RR"] = SchedulerAlgorithms.roundRobin(localProcs, quantum);
            results["PRIORITY"] = SchedulerAlgorithms.priority(localProcs);
            results["MLQ"] = SchedulerAlgorithms.mlq(localProcs);

            currentExperimentData = {
                name: expName,
                scenario: scenario,
                num_processes: localProcs.length,
                quantum: quantum,
                results: results
            };
            statusBox.innerHTML = '<p style="color:var(--accent-warning); font-weight:bold;">⚠ Simulación completada en modo Local (Sin persistencia).</p>';
        }

        // Renderizar vistas con los datos cargados
        displayExperimentResults();

    } catch (error) {
        console.error("Error running experiment:", error);
        if (statusBox) {
            statusBox.innerHTML = `<p style="color:var(--accent-danger)">Error: ${error.message}</p>`;
        }
    }
}

/**
 * Muestra las tablas, diagramas y gráficas con base en `currentExperimentData`
 */
function displayExperimentResults() {
    if (!currentExperimentData) return;

    // 1. Renderizar tabla comparativa general
    const tbody = document.getElementById('comparison-table-body');
    if (tbody) {
        tbody.innerHTML = '';
        
        let bestWaiting = Infinity;
        let bestAlgo = '';

        Object.keys(currentExperimentData.results).forEach(algo => {
            const metrics = currentExperimentData.results[algo].averages;
            const row = document.createElement('tr');
            
            const wTime = parseFloat(metrics.waitingTime !== undefined ? metrics.waitingTime : metrics.waiting_time);
            const tTime = parseFloat(metrics.turnaroundTime !== undefined ? metrics.turnaroundTime : metrics.turnaround_time);
            const throughput = parseFloat(metrics.throughput);
            const cpu = parseFloat(metrics.cpuUtilization !== undefined ? metrics.cpuUtilization : metrics.cpu_utilization);

            if (wTime < bestWaiting) {
                bestWaiting = wTime;
                bestAlgo = algo;
            }

            row.innerHTML = `
                <td><strong>${algo}</strong></td>
                <td>${wTime.toFixed(2)}</td>
                <td>${tTime.toFixed(2)}</td>
                <td>${throughput.toFixed(6)}</td>
                <td>${cpu.toFixed(2)}%</td>
            `;
            tbody.appendChild(row);
        });

        // Inyectar tarjetas destacadas / recomendación
        renderHighlights(bestAlgo, bestWaiting);
    }

    // 2. Disparar evento para que charts.js actualice las gráficas comparativas
    window.dispatchEvent(new CustomEvent('experimentCompleted', { detail: currentExperimentData }));

    // 3. Renderizar primer Gantt y primera tabla del selector por defecto
    const currentGanttAlgo = document.getElementById('gantt-algo-select').value;
    const currentTableAlgo = document.getElementById('table-algo-select').value;

    const ganttData = currentExperimentData.results[currentGanttAlgo];
    const tableData = currentExperimentData.results[currentTableAlgo];

    if (ganttData) renderGantt(ganttData.timeline);
    if (tableData) renderTable(tableData.processes);
}

/**
 * Destaca el mejor algoritmo en base al tiempo de espera.
 */
function renderHighlights(bestAlgo, bestWaiting) {
    const container = document.getElementById('comparison-highlights');
    if (!container) return;

    const descriptions = {
        'FCFS': 'Ideal para ejecuciones sencillas y sin interrupciones, pero susceptible al Efecto Convoy.',
        'SJF': 'Minimiza de manera óptima el tiempo medio de espera, pero puede causar inanición de procesos largos.',
        'RR': 'Equitativo y excelente para entornos interactivos (tiempo compartido), depende en gran medida del Quantum.',
        'PRIORITY': 'Prioriza tareas críticas de usuario o sistema, pero requiere mecanismos de envejecimiento para evitar inanición.',
        'MLQ': 'Organiza procesos de forma híbrida en colas segregadas, aplicando distintas políticas a cada una.'
    };

    container.innerHTML = `
        <div class="comparison-card winner">
            <h3>Algoritmo Recomendado</h3>
            <p style="font-size: 1.5rem; font-weight: 800; margin: 10px 0; color: var(--accent-success);">${bestAlgo}</p>
            <p class="text-muted" style="font-size: 0.85rem;">Es el algoritmo óptimo para esta carga de trabajo, logrando el menor tiempo de espera promedio (${bestWaiting} unidades).</p>
        </div>
        <div class="card" style="margin: 0; background: rgba(99, 102, 241, 0.05);">
            <h3>Carga de Trabajo Analizada</h3>
            <p style="font-size: 1.5rem; font-weight: 800; margin: 10px 0; color: var(--accent-secondary);">${currentExperimentData.num_processes} Procesos</p>
            <p class="text-muted" style="font-size: 0.85rem;">Escenario ${currentExperimentData.scenario} (Quantum ${currentExperimentData.quantum}). ${descriptions[bestAlgo] || ''}</p>
        </div>
    `;
}

/**
 * Limpia la pantalla de simulación actual.
 */
function resetSimulation() {
    const statusBox = document.getElementById('execution-status');
    if (statusBox) statusBox.innerHTML = '<p class="text-muted">Esperando inicio...</p>';
    
    document.getElementById('exp-name-input').value = '';
    
    const tbody = document.getElementById('comparison-table-body');
    if (tbody) tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Ejecuta una simulación en el laboratorio para ver los resultados.</td></tr>';
    
    const ganttBox = document.getElementById('gantt-chart-container');
    if (ganttBox) ganttBox.innerHTML = '';
    
    const tbodyProcs = document.querySelector('#process-table tbody');
    if (tbodyProcs) tbodyProcs.innerHTML = '';

    const highlights = document.getElementById('comparison-highlights');
    if (highlights) highlights.innerHTML = '';

    currentExperimentData = null;
    window.dispatchEvent(new CustomEvent('simulationReset'));
}

/**
 * Renderiza la tabla de procesos.
 */
function renderTable(processes) {
    const tbody = document.querySelector('#process-table tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    // Limitar a los primeros 100 procesos para optimizar UI en Cargas D
    const toRender = processes.slice(0, 100);
    
    toRender.forEach(p => {
        let tr = document.createElement('tr');
        const arrival = p.arrival_time !== undefined ? p.arrival_time : p.arrivalTime;
        const burst = p.burst_time !== undefined ? p.burst_time : p.burstTime;
        const completion = p.completion_time !== undefined ? p.completion_time : p.completionTime;
        const turnaround = p.turnaround_time !== undefined ? p.turnaround_time : p.turnaroundTime;
        const waiting = p.waiting_time !== undefined ? p.waiting_time : p.waitingTime;

        tr.innerHTML = `
            <td data-label="PID"><strong>${p.pid}</strong></td>
            <td data-label="Llegada">${arrival}</td>
            <td data-label="Ráfaga">${burst}</td>
            <td data-label="Prioridad"><span class="badge ${p.priority <= 2 ? 'badge-danger' : 'badge-success'}">${p.priority}</span></td>
            <td data-label="Fin">${completion}</td>
            <td data-label="Retorno">${turnaround}</td>
            <td data-label="Espera">${waiting}</td>
        `;
        tbody.appendChild(tr);
    });

    if (processes.length > 100) {
        let tr = document.createElement('tr');
        tr.innerHTML = `<td colspan="7" class="text-center text-muted">Mostrando los primeros 100 de ${processes.length} procesos...</td>`;
        tbody.appendChild(tr);
    }
}

/**
 * Renderiza el diagrama de Gantt.
 */
function renderGantt(timeline) {
    const container = document.getElementById('gantt-chart-container');
    if (!container) return;
    
    container.innerHTML = '';
    if (!timeline || timeline.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">No hay datos para mostrar el diagrama.</p>';
        return;
    }

    const toRender = timeline.slice(0, 200);
    const colors = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#3b82f6'];
    const maxTime = timeline[timeline.length - 1].end;
    
    toRender.forEach(block => {
        let duration = block.end - block.start;
        let num = parseInt(block.pid.replace(/\D/g, '')) || 0;
        let color = colors[num % colors.length];

        let bar = document.createElement('div');
        bar.className = 'gantt-bar-animated';
        bar.style.display = 'inline-block';
        bar.style.height = '40px';
        bar.style.minWidth = '40px';
        
        let widthPct = Math.max((duration / maxTime) * 100, 2); 
        bar.style.width = timeline.length > 50 ? '45px' : `${widthPct}%`; 
        
        bar.style.backgroundColor = color;
        bar.style.color = '#fff';
        bar.style.textAlign = 'center';
        bar.style.lineHeight = '40px';
        bar.style.marginRight = '2px';
        bar.style.borderRadius = '4px';
        bar.style.fontSize = '0.8rem';
        bar.style.fontWeight = 'bold';
        bar.style.position = 'relative';

        bar.innerText = block.pid;
        bar.title = `${block.pid}: ${block.start} -> ${block.end} ${block.queue ? `(${block.queue})` : ''}`;

        container.appendChild(bar);
    });

    if (timeline.length > 200) {
        let ellip = document.createElement('div');
        ellip.style.display = 'inline-block';
        ellip.style.marginLeft = '10px';
        ellip.style.color = 'var(--text-secondary)';
        ellip.style.lineHeight = '40px';
        ellip.innerText = `... y ${timeline.length - 200} bloques de contexto más.`;
        container.appendChild(ellip);
    }
}

/**
 * Carga e inyecta la lista de experimentos desde MySQL (CRUD: Read).
 */
async function loadHistoryList() {
    const container = document.getElementById('history-list-container');
    if (!container) return;

    if (!isBackendOnline) {
        container.innerHTML = `
            <div class="text-center py-4">
                <p class="text-danger">⚠ Servidor offline</p>
                <p class="text-muted" style="font-size: 0.85rem;">Inicie el servidor de Python (Flask) y XAMPP MySQL para ver el historial de simulaciones persistido.</p>
            </div>
        `;
        return;
    }

    try {
        container.innerHTML = '<p class="text-muted text-center py-4"><span class="spinner"></span> Cargando experimentos...</p>';
        const experiments = await SimulatorAPI.getExperiments();

        if (experiments.length === 0) {
            container.innerHTML = '<p class="text-muted text-center py-4">No hay experimentos registrados en la base de datos MySQL.</p>';
            return;
        }

        container.innerHTML = '';
        experiments.forEach(exp => {
            const card = document.createElement('div');
            card.className = 'experiment-card';
            card.innerHTML = `
                <div>
                    <strong style="color: var(--accent-secondary); font-size: 1.1rem;" id="exp-title-${exp.id}">${exp.name}</strong>
                    <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px;">
                        Carga: ${exp.scenario} | Procesos: ${exp.num_processes} | Quantum: ${exp.quantum} | Fecha: ${exp.created_at}
                    </div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn btn-primary" onclick="loadExperimentDetail(${exp.id})" style="padding: 6px 12px; font-size: 0.75rem;">Ver</button>
                    <button class="btn btn-secondary" onclick="renameExperimentPrompt(${exp.id})" style="padding: 6px 12px; font-size: 0.75rem;">Editar</button>
                    <button class="btn btn-danger" onclick="deleteExperimentClick(${exp.id})" style="padding: 6px 12px; font-size: 0.75rem;">Eliminar</button>
                </div>
            `;
            container.appendChild(card);
        });

    } catch (e) {
        container.innerHTML = `<p class="text-danger text-center py-4">Error al cargar historial: ${e.message}</p>`;
    }
}

/**
 * Carga el detalle completo de un experimento desde MySQL (CRUD: Read Detail).
 */
async function loadExperimentDetail(id) {
    try {
        const detail = await SimulatorAPI.getExperimentDetail(id);
        if (!detail) return;

        // Estructurar el detalle en la estructura del simulador local
        currentExperimentData = {
            id: detail.id,
            name: detail.name,
            scenario: detail.scenario,
            num_processes: detail.num_processes,
            quantum: detail.quantum,
            results: {}
        };

        detail.simulations.forEach(sim => {
            currentExperimentData.results[sim.algorithm] = {
                averages: {
                    waitingTime: sim.avg_waiting_time,
                    turnaroundTime: sim.avg_turnaround,
                    throughput: sim.throughput,
                    cpuUtilization: sim.cpu_utilization
                },
                timeline: sim.processes.map(p => ({
                    pid: p.pid,
                    // Recrear una línea de tiempo simulada en base a llegada y fin
                    start: Math.max(0, p.completion_time - p.burst_time),
                    end: p.completion_time
                })),
                processes: sim.processes
            };
        });

        // Mostrar resultados
        displayExperimentResults();

        // Mover a la pestaña comparativa
        const compNavLink = document.querySelector('a[data-target="module-7"]');
        if (compNavLink) compNavLink.click();

        alert(`Experimento "${detail.name}" cargado con éxito en el visualizador.`);

    } catch (e) {
        alert('Error al cargar detalle del experimento: ' + e.message);
    }
}

/**
 * Lanza prompt para renombrar experimento (CRUD: Update).
 */
async function renameExperimentPrompt(id) {
    const titleEl = document.getElementById(`exp-title-${id}`);
    const currentName = titleEl ? titleEl.innerText : "";
    const newName = prompt("Introduce el nuevo nombre para este experimento:", currentName);
    
    if (newName && newName.trim() !== "" && newName !== currentName) {
        try {
            await SimulatorAPI.updateExperimentName(id, newName.trim());
            alert('Nombre actualizado con éxito.');
            loadHistoryList();
        } catch (e) {
            alert('Error al renombrar: ' + e.message);
        }
    }
}

/**
 * Elimina un experimento (CRUD: Delete).
 */
async function deleteExperimentClick(id) {
    if (confirm("¿Estás seguro de que deseas eliminar este experimento de la base de datos? Se borrarán todas sus simulaciones.")) {
        try {
            await SimulatorAPI.deleteExperiment(id);
            alert('Experimento eliminado.');
            loadHistoryList();
            
            // Si el experimento activo fue eliminado, resetear visualizador
            if (currentExperimentData && currentExperimentData.id === id) {
                resetSimulation();
            }
        } catch (e) {
            alert('Error al eliminar: ' + e.message);
        }
    }
}

// Inyectar en window para llamadas inline onclick
window.loadExperimentDetail = loadExperimentDetail;
window.renameExperimentPrompt = renameExperimentPrompt;
window.deleteExperimentClick = deleteExperimentClick;
