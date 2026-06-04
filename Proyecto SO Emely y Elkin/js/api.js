// js/api.js - Capa de comunicación REST con el backend Flask (MVC) o persistencia en LocalStorage

const API_BASE_URL = 'http://localhost:5000/api';

class LocalBrowserStorage {
    static _getKey() {
        return 'os_scheduler_local_experiments';
    }

    static _getRawList() {
        const raw = localStorage.getItem(this._getKey());
        return raw ? JSON.parse(raw) : [];
    }

    static _saveRawList(list) {
        localStorage.setItem(this._getKey(), JSON.stringify(list));
    }

    static getExperiments() {
        const list = this._getRawList();
        return list.map(exp => ({
            id: exp.id,
            name: exp.name,
            scenario: exp.scenario,
            num_processes: exp.num_processes,
            quantum: exp.quantum,
            created_at: exp.created_at,
            simulations: exp.simulations.map(s => ({
                algorithm: s.algorithm,
                avg_waiting_time: s.avg_waiting_time,
                avg_turnaround: s.avg_turnaround,
                throughput: s.throughput,
                cpu_utilization: s.cpu_utilization
            }))
        }));
    }

    static getExperimentDetail(id) {
        const list = this._getRawList();
        const found = list.find(exp => exp.id === id);
        return found || null;
    }

    static saveExperiment(scenario, quantum, name, results) {
        const list = this._getRawList();
        const nextId = list.length > 0 ? Math.max(...list.map(e => e.id)) + 1 : 1;
        
        // Estructurar el experimento con simulaciones completas y procesos
        const newExperiment = {
            id: nextId,
            name: name,
            scenario: scenario,
            num_processes: Object.values(results)[0].processes.length,
            quantum: quantum,
            created_at: new Date().toLocaleString('es-ES') + ' (Local)',
            simulations: Object.keys(results).map((algo, index) => {
                const res = results[algo];
                const metrics = res.averages;
                return {
                    id: nextId * 100 + index,
                    algorithm: algo,
                    avg_waiting_time: metrics.waitingTime !== undefined ? metrics.waitingTime : metrics.waiting_time,
                    avg_turnaround: metrics.turnaroundTime !== undefined ? metrics.turnaroundTime : metrics.turnaround_time,
                    throughput: metrics.throughput,
                    cpu_utilization: metrics.cpuUtilization !== undefined ? metrics.cpuUtilization : metrics.cpu_utilization,
                    processes: res.processes.map(p => ({
                        pid: p.pid,
                        arrival_time: p.arrival_time !== undefined ? p.arrival_time : p.arrivalTime,
                        burst_time: p.burst_time !== undefined ? p.burst_time : p.burstTime,
                        priority: p.priority,
                        completion_time: p.completion_time !== undefined ? p.completion_time : p.completionTime,
                        turnaround_time: p.turnaround_time !== undefined ? p.turnaround_time : p.turnaroundTime,
                        waiting_time: p.waiting_time !== undefined ? p.waiting_time : p.waitingTime
                    }))
                };
            })
        };

        list.push(newExperiment);
        this._saveRawList(list);
        
        return {
            message: "Experimento completado y guardado en el navegador con éxito.",
            experiment_id: nextId,
            name: name,
            scenario: scenario,
            num_processes: newExperiment.num_processes,
            quantum: quantum,
            results: results
        };
    }

    static updateExperimentName(id, name) {
        const list = this._getRawList();
        const found = list.find(exp => exp.id === id);
        if (!found) throw new Error("Experimento no encontrado en almacenamiento local");
        found.name = name;
        this._saveRawList(list);
        return { message: "Nombre de experimento actualizado con éxito en almacenamiento local" };
    }

    static deleteExperiment(id) {
        let list = this._getRawList();
        const exists = list.some(exp => exp.id === id);
        if (!exists) throw new Error("Experimento no encontrado en almacenamiento local");
        list = list.filter(exp => exp.id !== id);
        this._saveRawList(list);
        return { message: "Experimento eliminado con éxito de almacenamiento local" };
    }
}

class SimulatorAPI {
    static isOnline = false;

    /**
     * Verifica si el backend está activo y conectado a la base de datos local SQLite.
     */
    static async checkHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) {
                this.isOnline = false;
                return { status: 'offline', mysql_connected: false };
            }
            const data = await response.json();
            this.isOnline = (data.status === 'ok' && data.mysql_connected);
            return data;
        } catch (e) {
            this.isOnline = false;
            return { status: 'offline', mysql_connected: false, error: e.message };
        }
    }

    /**
     * Ejecuta un experimento comparativo (corre los 5 algoritmos) en el backend y los guarda.
     */
    static async runExperiment(scenario, quantum, name) {
        if (!this.isOnline) {
            throw new Error("El simulador se encuentra en modo local de navegador. Use la persistencia local.");
        }
        try {
            const response = await fetch(`${API_BASE_URL}/experiments`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ scenario, quantum, name })
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error al ejecutar el experimento');
            }
            return await response.json();
        } catch (e) {
            console.error('API Error:', e);
            throw e;
        }
    }

    /**
     * Obtiene el listado de todos los experimentos guardados.
     */
    static async getExperiments() {
        if (!this.isOnline) {
            return LocalBrowserStorage.getExperiments();
        }
        try {
            const response = await fetch(`${API_BASE_URL}/experiments`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Error al obtener la lista de experimentos');
            return await response.json();
        } catch (e) {
            console.error('API Error, cayendo a almacenamiento local:', e);
            return LocalBrowserStorage.getExperiments();
        }
    }

    /**
     * Obtiene el detalle completo de un experimento por su ID.
     */
    static async getExperimentDetail(id) {
        if (!this.isOnline) {
            return LocalBrowserStorage.getExperimentDetail(id);
        }
        try {
            const response = await fetch(`${API_BASE_URL}/experiments/${id}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) {
                return LocalBrowserStorage.getExperimentDetail(id);
            }
            return await response.json();
        } catch (e) {
            console.error('API Error, buscando en almacenamiento local:', e);
            return LocalBrowserStorage.getExperimentDetail(id);
        }
    }

    /**
     * Actualiza el nombre de un experimento.
     */
    static async updateExperimentName(id, name) {
        if (!this.isOnline) {
            return LocalBrowserStorage.updateExperimentName(id, name);
        }
        try {
            const response = await fetch(`${API_BASE_URL}/experiments/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name })
            });
            if (!response.ok) {
                return LocalBrowserStorage.updateExperimentName(id, name);
            }
            return await response.json();
        } catch (e) {
            console.error('API Error, actualizando en almacenamiento local:', e);
            return LocalBrowserStorage.updateExperimentName(id, name);
        }
    }

    /**
     * Elimina un experimento.
     */
    static async deleteExperiment(id) {
        if (!this.isOnline) {
            return LocalBrowserStorage.deleteExperiment(id);
        }
        try {
            const response = await fetch(`${API_BASE_URL}/experiments/${id}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) {
                return LocalBrowserStorage.deleteExperiment(id);
            }
            return await response.json();
        } catch (e) {
            console.error('API Error, eliminando en almacenamiento local:', e);
            return LocalBrowserStorage.deleteExperiment(id);
        }
    }
}

window.LocalBrowserStorage = LocalBrowserStorage;
window.SimulatorAPI = SimulatorAPI;
