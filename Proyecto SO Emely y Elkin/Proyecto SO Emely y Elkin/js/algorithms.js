// js/algorithms.js - Implementación de Algoritmos de Planificación de CPU

/**
 * Cada algoritmo recibe una lista de procesos y (opcionalmente) un quantum.
 * Estructura de proceso esperada: { pid, arrivalTime, burstTime, priority }
 * Retorna: {
 *    timeline: [ { pid, start, end } ], // Para el diagrama de Gantt
 *    processes: [ { pid, arrivalTime, burstTime, priority, completionTime, turnaroundTime, waitingTime } ],
 *    averages: { waitingTime, turnaroundTime, throughput, cpuUtilization }
 * }
 */

class SchedulerAlgorithms {

    static cloneProcesses(processes) {
        return processes.map(p => ({ ...p, remainingTime: p.burstTime, isCompleted: false }));
    }

    static calculateMetrics(completedProcesses, timeline) {
        let totalTurnaround = 0;
        let totalWaiting = 0;
        let maxTime = 0;
        let totalBurst = 0;

        completedProcesses.forEach(p => {
            p.turnaroundTime = p.completionTime - p.arrivalTime;
            p.waitingTime = p.turnaroundTime - p.burstTime;
            totalTurnaround += p.turnaroundTime;
            totalWaiting += p.waitingTime;
            totalBurst += p.burstTime;
            if (p.completionTime > maxTime) maxTime = p.completionTime;
        });

        const n = completedProcesses.length;
        return {
            processes: completedProcesses,
            timeline: timeline,
            averages: {
                waitingTime: (totalWaiting / n).toFixed(2),
                turnaroundTime: (totalTurnaround / n).toFixed(2),
                throughput: (n / maxTime).toFixed(4), // Procesos por unidad de tiempo
                cpuUtilization: ((totalBurst / maxTime) * 100).toFixed(2)
            }
        };
    }

    // 1. FCFS (First Come First Served)
    static fcfs(processes) {
        let procs = this.cloneProcesses(processes).sort((a, b) => a.arrivalTime - b.arrivalTime);
        let currentTime = 0;
        let timeline = [];
        let completed = [];

        procs.forEach(p => {
            if (currentTime < p.arrivalTime) {
                currentTime = p.arrivalTime; // CPU Idle
            }
            let start = currentTime;
            currentTime += p.burstTime;
            p.completionTime = currentTime;
            
            timeline.push({ pid: p.pid, start: start, end: currentTime });
            completed.push(p);
        });

        return this.calculateMetrics(completed, timeline);
    }

    // 2. SJF (Shortest Job First) - No expropiativo
    static sjf(processes) {
        let procs = this.cloneProcesses(processes);
        let currentTime = 0;
        let timeline = [];
        let completed = [];
        let completedCount = 0;
        const n = procs.length;

        while (completedCount < n) {
            let available = procs.filter(p => p.arrivalTime <= currentTime && !p.isCompleted);
            
            if (available.length > 0) {
                available.sort((a, b) => a.burstTime - b.burstTime); // Ordenar por ráfaga más corta
                let currentProc = available[0];
                
                let start = currentTime;
                currentTime += currentProc.burstTime;
                currentProc.completionTime = currentTime;
                currentProc.isCompleted = true;
                
                timeline.push({ pid: currentProc.pid, start: start, end: currentTime });
                completed.push(currentProc);
                completedCount++;
            } else {
                currentTime++; // CPU Idle
            }
        }

        return this.calculateMetrics(completed, timeline);
    }

    // 3. Round Robin (RR)
    static roundRobin(processes, quantum) {
        let procs = this.cloneProcesses(processes).sort((a, b) => a.arrivalTime - b.arrivalTime);
        let currentTime = 0;
        let timeline = [];
        let readyQueue = [];
        let completed = [];
        let completedCount = 0;
        const n = procs.length;
        
        let index = 0; // Índice para procesos que van llegando
        
        // Función para encolar procesos que llegaron
        const enqueueArrivals = () => {
            while (index < n && procs[index].arrivalTime <= currentTime) {
                readyQueue.push(procs[index]);
                index++;
            }
        };

        enqueueArrivals();

        while (completedCount < n) {
            if (readyQueue.length === 0) {
                currentTime++;
                enqueueArrivals();
                continue;
            }

            let currentProc = readyQueue.shift();
            let start = currentTime;
            
            let timeToExecute = Math.min(currentProc.remainingTime, quantum);
            currentTime += timeToExecute;
            currentProc.remainingTime -= timeToExecute;
            
            timeline.push({ pid: currentProc.pid, start: start, end: currentTime });

            enqueueArrivals(); // Encolar nuevos antes de re-encolar el actual

            if (currentProc.remainingTime > 0) {
                readyQueue.push(currentProc);
            } else {
                currentProc.completionTime = currentTime;
                currentProc.isCompleted = true;
                completed.push(currentProc);
                completedCount++;
            }
        }

        return this.calculateMetrics(completed, timeline);
    }

    // 4. Priority Scheduling (No expropiativo, menor número = mayor prioridad)
    static priority(processes) {
        let procs = this.cloneProcesses(processes);
        let currentTime = 0;
        let timeline = [];
        let completed = [];
        let completedCount = 0;
        const n = procs.length;

        while (completedCount < n) {
            let available = procs.filter(p => p.arrivalTime <= currentTime && !p.isCompleted);
            
            if (available.length > 0) {
                // Menor número en 'priority' significa mayor prioridad
                available.sort((a, b) => a.priority - b.priority); 
                let currentProc = available[0];
                
                let start = currentTime;
                currentTime += currentProc.burstTime;
                currentProc.completionTime = currentTime;
                currentProc.isCompleted = true;
                
                timeline.push({ pid: currentProc.pid, start: start, end: currentTime });
                completed.push(currentProc);
                completedCount++;
            } else {
                currentTime++; // CPU Idle
            }
        }

        return this.calculateMetrics(completed, timeline);
    }

    // 5. Multilevel Queue (MLQ) simplificado
    // Cola 1: Prioridad 1-2 (RR q=2)
    // Cola 2: Prioridad 3-5 (FCFS)
    static mlq(processes) {
        let procs = this.cloneProcesses(processes).sort((a, b) => a.arrivalTime - b.arrivalTime);
        let currentTime = 0;
        let timeline = [];
        let completed = [];
        
        let q1 = []; // RR q=2
        let q2 = []; // FCFS
        
        let completedCount = 0;
        const n = procs.length;
        let index = 0;

        const enqueueArrivals = () => {
            while (index < n && procs[index].arrivalTime <= currentTime) {
                if (procs[index].priority <= 2) {
                    q1.push(procs[index]);
                } else {
                    q2.push(procs[index]);
                }
                index++;
            }
        };

        enqueueArrivals();

        while (completedCount < n) {
            if (q1.length === 0 && q2.length === 0) {
                currentTime++;
                enqueueArrivals();
                continue;
            }

            // Prioridad a Q1
            if (q1.length > 0) {
                let currentProc = q1.shift();
                let start = currentTime;
                let quantum = 2;
                
                let timeToExecute = Math.min(currentProc.remainingTime, quantum);
                currentTime += timeToExecute;
                currentProc.remainingTime -= timeToExecute;
                
                timeline.push({ pid: currentProc.pid, queue: 'Q1', start: start, end: currentTime });
                enqueueArrivals();

                if (currentProc.remainingTime > 0) {
                    q1.push(currentProc);
                } else {
                    currentProc.completionTime = currentTime;
                    currentProc.isCompleted = true;
                    completed.push(currentProc);
                    completedCount++;
                }
            } else if (q2.length > 0) {
                let currentProc = q2.shift();
                let start = currentTime;
                
                currentTime += currentProc.burstTime; // FCFS ejecuta completo
                currentProc.remainingTime = 0;
                
                timeline.push({ pid: currentProc.pid, queue: 'Q2', start: start, end: currentTime });
                enqueueArrivals();
                
                currentProc.completionTime = currentTime;
                currentProc.isCompleted = true;
                completed.push(currentProc);
                completedCount++;
            }
        }

        return this.calculateMetrics(completed, timeline);
    }
}
