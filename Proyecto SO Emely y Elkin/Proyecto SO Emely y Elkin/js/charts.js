// js/charts.js - Dashboard Analítico de Comparación Side-by-Side usando Chart.js

let chartTimesInstance = null;
let chartPerfInstance = null;

// Colores Neón Premium para el Dark Mode Glassmorphism
const colorWaiting = 'rgba(99, 102, 241, 0.8)';   // Indigo
const colorTurnaround = 'rgba(6, 182, 212, 0.8)'; // Cian
const colorThroughput = 'rgba(16, 185, 129, 0.8)'; // Esmeralda
const colorCpu = 'rgba(245, 158, 11, 0.8)';        // Ámbar

const borderWaiting = 'rgba(99, 102, 241, 1)';
const borderTurnaround = 'rgba(6, 182, 212, 1)';
const borderThroughput = 'rgba(16, 185, 129, 1)';
const borderCpu = 'rgba(245, 158, 11, 1)';

const textLight = '#94a3b8'; // Gris azulado de la tipografía

document.addEventListener('DOMContentLoaded', () => {
    initEmptyCharts();
    
    // Escuchar cuando el experimento completo termina
    window.addEventListener('experimentCompleted', (e) => {
        updateCharts(e.detail.results);
    });

    window.addEventListener('simulationReset', () => {
        initEmptyCharts();
    });
});

/**
 * Inicializa las gráficas con valores vacíos.
 */
function initEmptyCharts() {
    const algos = ['FCFS', 'SJF', 'RR', 'PRIORITY', 'MLQ'];

    const dataTimes = {
        labels: algos,
        datasets: [
            {
                label: 'Espera Promedio',
                data: [0, 0, 0, 0, 0],
                backgroundColor: colorWaiting,
                borderColor: borderWaiting,
                borderWidth: 1
            },
            {
                label: 'Retorno Promedio',
                data: [0, 0, 0, 0, 0],
                backgroundColor: colorTurnaround,
                borderColor: borderTurnaround,
                borderWidth: 1
            }
        ]
    };

    const dataPerf = {
        labels: algos,
        datasets: [
            {
                label: 'Throughput (Proc/Unidad)',
                data: [0, 0, 0, 0, 0],
                backgroundColor: colorThroughput,
                borderColor: borderThroughput,
                borderWidth: 1,
                yAxisID: 'y1'
            },
            {
                label: 'Uso de CPU (%)',
                data: [0, 0, 0, 0, 0],
                backgroundColor: colorCpu,
                borderColor: borderCpu,
                borderWidth: 1,
                yAxisID: 'y'
            }
        ]
    };

    renderTimesChart(dataTimes);
    renderPerfChart(dataPerf);
}

/**
 * Actualiza las gráficas con los resultados comparativos.
 */
function updateCharts(results) {
    const algos = ['FCFS', 'SJF', 'RR', 'PRIORITY', 'MLQ'];
    
    const waitingData = [];
    const turnaroundData = [];
    const throughputData = [];
    const cpuData = [];

    algos.forEach(algo => {
        const metrics = results[algo] ? results[algo].averages : {};
        const wTime = parseFloat(metrics.waitingTime !== undefined ? metrics.waitingTime : (metrics.waiting_time !== undefined ? metrics.waiting_time : 0));
        const tTime = parseFloat(metrics.turnaroundTime !== undefined ? metrics.turnaroundTime : (metrics.turnaround_time !== undefined ? metrics.turnaround_time : 0));
        const throughput = parseFloat(metrics.throughput !== undefined ? metrics.throughput : 0);
        const cpu = parseFloat(metrics.cpuUtilization !== undefined ? metrics.cpuUtilization : (metrics.cpu_utilization !== undefined ? metrics.cpu_utilization : 0));

        waitingData.push(wTime);
        turnaroundData.push(tTime);
        throughputData.push(throughput);
        cpuData.push(cpu);
    });

    const dataTimes = {
        labels: algos,
        datasets: [
            {
                label: 'Espera Promedio',
                data: waitingData,
                backgroundColor: colorWaiting,
                borderColor: borderWaiting,
                borderWidth: 1,
                borderRadius: 4
            },
            {
                label: 'Retorno Promedio',
                data: turnaroundData,
                backgroundColor: colorTurnaround,
                borderColor: borderTurnaround,
                borderWidth: 1,
                borderRadius: 4
            }
        ]
    };

    const dataPerf = {
        labels: algos,
        datasets: [
            {
                label: 'Throughput (Proc/Unidad)',
                data: throughputData,
                backgroundColor: colorThroughput,
                borderColor: borderThroughput,
                borderWidth: 1,
                borderRadius: 4,
                yAxisID: 'y1'
            },
            {
                label: 'Uso de CPU (%)',
                data: cpuData,
                backgroundColor: colorCpu,
                borderColor: borderCpu,
                borderWidth: 1,
                borderRadius: 4,
                yAxisID: 'y'
            }
        ]
    };

    renderTimesChart(dataTimes);
    renderPerfChart(dataPerf);
}

/**
 * Renderiza el gráfico de Tiempos (Espera vs Retorno).
 */
function renderTimesChart(data) {
    const ctx = document.getElementById('chart-times');
    if (!ctx) return;
    if (chartTimesInstance) {
        chartTimesInstance.destroy();
    }
    chartTimesInstance = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: textLight, font: { family: 'Outfit' } }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#e2e8f0',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: textLight, font: { family: 'Outfit' } },
                    title: { display: true, text: 'Unidades de Tiempo', color: textLight }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: textLight, font: { family: 'Outfit' } }
                }
            }
        }
    });
}

/**
 * Renderiza el gráfico de Rendimiento (CPU % en eje izquierdo, Throughput en eje derecho).
 */
function renderPerfChart(data) {
    const ctx = document.getElementById('chart-performance');
    if (!ctx) return;
    if (chartPerfInstance) {
        chartPerfInstance.destroy();
    }
    chartPerfInstance = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: textLight, font: { family: 'Outfit' } }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#e2e8f0',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: textLight, font: { family: 'Outfit' } },
                    title: { display: true, text: 'Uso CPU (%)', color: textLight }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    beginAtZero: true,
                    grid: { drawOnChartArea: false }, // Evita superposición de grillas
                    ticks: { color: textLight, font: { family: 'Outfit' } },
                    title: { display: true, text: 'Throughput (Proc/Unidad)', color: textLight }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: textLight, font: { family: 'Outfit' } }
                }
            }
        }
    });
}
