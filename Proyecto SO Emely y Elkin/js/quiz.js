// js/quiz.js - Módulo de Evaluación Rediseñado (10 Preguntas con Feedback Inmediato)

const quizData = [
    {
        q: "¿Qué significa el acrónimo FCFS?",
        options: ["First Come First Served", "Fast CPU Fast Schedule", "First Core First System", "Final Context Final State"],
        ans: 0,
        explanation: "Los procesos se ejecutan estrictamente según su orden de llegada a la cola de listos."
    },
    {
        q: "¿Cuál es el principal problema del algoritmo SJF (Shortest Job First)?",
        options: ["Alto número de cambios de contexto", "Incapacidad de conocer con exactitud la ráfaga futura", "Solo funciona en sistemas de un núcleo", "Es muy injusto con los procesos cortos"],
        ans: 1,
        explanation: "SJF requiere conocer el tiempo exacto que un proceso ocupará la CPU en el futuro, lo cual es prácticamente imposible de predecir en la vida real."
    },
    {
        q: "En Round Robin, el intervalo de tiempo fijo asignado a cada proceso se llama:",
        options: ["Slice de Memoria", "Burst Time", "Quantum", "Deadline"],
        ans: 2,
        explanation: "El Quantum es el límite de tiempo que un proceso puede usar la CPU antes de ser interrumpido y devuelto a la cola."
    },
    {
        q: "¿Qué sucede en Round Robin si el Quantum es excesivamente grande?",
        options: ["El sistema colapsa", "Se comporta exactamente como FCFS", "Se vuelve el algoritmo más rápido", "Se convierte en un SJF"],
        ans: 1,
        explanation: "Si el Quantum es infinito o muy grande, los procesos terminan su ejecución antes de ser interrumpidos, operando como un FCFS tradicional."
    },
    {
        q: "El problema de la 'Inanición' (Starvation) en la planificación por prioridades ocurre cuando:",
        options: ["Un proceso corto nunca se ejecuta porque llegan procesos más largos", "Un proceso de baja prioridad nunca obtiene la CPU porque siempre hay procesos de mayor prioridad", "La CPU se sobrecalienta", "Falta memoria RAM"],
        ans: 1,
        explanation: "Los procesos de baja prioridad pueden quedar bloqueados indefinidamente si siguen llegando procesos con alta prioridad al sistema."
    },
    {
        q: "¿Cuál es la técnica estándar para solucionar la Inanición?",
        options: ["Envejecimiento (Aging)", "Reinicio del Sistema", "Expropiación (Preemption)", "Uso exclusivo de FCFS"],
        ans: 0,
        explanation: "El Aging aumenta gradualmente la prioridad de los procesos a medida que esperan en la cola, garantizando que eventualmente se ejecuten."
    },
    {
        q: "El Tiempo de Retorno (Turnaround Time) se calcula como:",
        options: ["Tiempo de Finalización + Tiempo de Llegada", "Tiempo de Llegada - Tiempo de Ráfaga", "Tiempo de Finalización - Tiempo de Llegada", "Tiempo de Espera - Tiempo de Ráfaga"],
        ans: 2,
        explanation: "Es el tiempo total transcurrido desde que un proceso entra al sistema hasta que finaliza completamente."
    },
    {
        q: "¿Qué es el 'Efecto Convoy' en FCFS?",
        options: ["Procesos cortos atrapados detrás de un proceso largo", "Muchos procesos ejecutándose a la vez", "Procesos largos atrapados detrás de un proceso corto", "Sincronización de múltiples núcleos"],
        ans: 0,
        explanation: "Cuando un proceso intensivo en CPU entra primero, todos los procesos rápidos detrás de él deben esperar demasiado tiempo, reduciendo el Throughput."
    },
    {
        q: "Un proceso ligado a E/S (I/O-bound) pasa la mayor parte de su tiempo:",
        options: ["Calculando algoritmos matemáticos", "Esperando respuestas de red, disco o usuario", "Haciendo cambios de contexto", "En estado de Terminado"],
        ans: 1,
        explanation: "Estos procesos generan pequeñas ráfagas de CPU seguidas de largas esperas por dispositivos externos."
    },
    {
        q: "Un 'Cambio de Contexto' (Context Switch) implica:",
        options: ["Cambiar de usuario en el SO", "Guardar el estado del proceso actual y cargar el del siguiente", "Cambiar de monitor", "Borrar la memoria caché"],
        ans: 1,
        explanation: "Es la operación donde la CPU detiene un proceso, guarda sus registros y punteros, y restaura los del nuevo proceso a ejecutar. Genera un costo computacional (overhead)."
    }
];

let currentQuestionIndex = 0;
let quizScore = 0;

document.addEventListener('DOMContentLoaded', () => {
    const btnStart = document.getElementById('btn-start-quiz');
    if(btnStart) {
        // Aseguramos remover listeners previos si existen para evitar doble ejecución
        btnStart.replaceWith(btnStart.cloneNode(true));
        document.getElementById('btn-start-quiz').addEventListener('click', startQuiz);
    }
});

function startQuiz() {
    currentQuestionIndex = 0;
    quizScore = 0;
    renderQuestion();
}

function renderQuestion() {
    const container = document.getElementById('quiz-container');
    if(currentQuestionIndex >= quizData.length) {
        showFinalResults();
        return;
    }

    const q = quizData[currentQuestionIndex];
    let html = `
        <h2>Evaluación Interactiva</h2>
        <p class="text-muted">Pregunta ${currentQuestionIndex + 1} de ${quizData.length}</p>
        <div class="card" style="border: 1px solid var(--accent-primary);">
            <p style="font-size: 1.1rem; font-weight: bold; color: var(--text-primary);">${q.q}</p>
            <div id="options-container" style="margin-top: 15px;">
    `;

    q.options.forEach((opt, idx) => {
        html += `
            <label style="display: block; padding: 10px; background: var(--bg-primary); margin-bottom: 8px; border-radius: 6px; cursor: pointer; border: 1px solid var(--bg-card); transition: all 0.2s;">
                <input type="radio" name="q_opt" value="${idx}"> ${opt}
            </label>
        `;
    });

    html += `
            </div>
            <div id="feedback-area" style="margin-top: 20px; display: none; padding: 15px; border-radius: 6px;"></div>
            <button id="btn-verify" class="btn btn-primary mt-3">Verificar Respuesta</button>
            <button id="btn-next" class="btn btn-secondary mt-3" style="display: none;">Siguiente Pregunta</button>
        </div>
    `;

    container.innerHTML = html;

    document.getElementById('btn-verify').addEventListener('click', verifyAnswer);
    document.getElementById('btn-next').addEventListener('click', () => {
        currentQuestionIndex++;
        renderQuestion();
    });
}

function verifyAnswer() {
    const selected = document.querySelector('input[name="q_opt"]:checked');
    if(!selected) {
        alert("Por favor, selecciona una opción antes de verificar.");
        return;
    }

    const ansIdx = parseInt(selected.value);
    const q = quizData[currentQuestionIndex];
    const isCorrect = (ansIdx === q.ans);
    
    // Deshabilitar radios
    document.querySelectorAll('input[name="q_opt"]').forEach(r => r.disabled = true);
    
    const feedbackArea = document.getElementById('feedback-area');
    document.getElementById('btn-verify').style.display = 'none';
    document.getElementById('btn-next').style.display = 'inline-flex';

    feedbackArea.style.display = 'block';

    if(isCorrect) {
        quizScore++;
        feedbackArea.style.backgroundColor = 'rgba(16, 185, 129, 0.1)'; // Fondo esmeralda semitransparente
        feedbackArea.style.border = '1px solid rgba(16, 185, 129, 0.2)';
        feedbackArea.style.borderLeft = '4px solid var(--accent-success)';
        feedbackArea.innerHTML = `
            <h4 style="color: var(--accent-success); margin-bottom: 5px;">¡Correcto!</h4>
            <p style="color: var(--text-primary); font-size: 0.95rem;">${q.explanation}</p>
        `;
    } else {
        feedbackArea.style.backgroundColor = 'rgba(239, 68, 68, 0.1)'; // Fondo coral semitransparente
        feedbackArea.style.border = '1px solid rgba(239, 68, 68, 0.2)';
        feedbackArea.style.borderLeft = '4px solid var(--accent-danger)';
        feedbackArea.innerHTML = `
            <h4 style="color: var(--accent-danger); margin-bottom: 5px;">Incorrecto</h4>
            <p style="color: var(--text-primary); font-weight: bold; margin-bottom: 5px;">La respuesta correcta era: ${q.options[q.ans]}</p>
            <p style="color: var(--text-secondary); font-size: 0.95rem;">${q.explanation}</p>
        `;
    }
}

function showFinalResults() {
    const container = document.getElementById('quiz-container');
    const percentage = (quizScore / quizData.length) * 100;
    
    let html = `
        <h2>Resultados de la Evaluación</h2>
        <div class="card text-center" style="padding: 30px;">
            <h1 style="font-size: 4rem; color: ${percentage >= 70 ? 'var(--accent-primary)' : '#EF5350'};">${quizScore} / ${quizData.length}</h1>
            <h3>Porcentaje de Acierto: ${percentage}%</h3>
    `;

    if(percentage >= 80) {
        html += '<p style="margin-top: 15px; color: var(--text-secondary);">¡Excelente trabajo! Has demostrado un conocimiento sólido de los algoritmos y métricas de planificación.</p>';
    } else if (percentage >= 60) {
        html += '<p style="margin-top: 15px; color: var(--text-secondary);">Buen desempeño, aunque todavía hay espacio para mejorar. Revisa los conceptos donde fallaste.</p>';
    } else {
        html += '<p style="margin-top: 15px; color: var(--text-secondary);">Parece que necesitas repasar. Te recomendamos volver a leer el material teórico e interactuar más con el simulador.</p>';
    }

    html += `<button id="btn-restart-quiz" class="btn btn-primary mt-3">Reintentar Evaluación</button></div>`;
    
    container.innerHTML = html;
    document.getElementById('btn-restart-quiz').addEventListener('click', startQuiz);
}
