// js/api.js - Capa de comunicación REST con el backend Flask (MVC)

const API_BASE_URL = 'http://localhost:5000/api';

class SimulatorAPI {
    /**
     * Verifica si el backend está activo y conectado a la base de datos MySQL.
     */
    static async checkHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) return { status: 'offline', mysql_connected: false };
            return await response.json();
        } catch (e) {
            return { status: 'offline', mysql_connected: false, error: e.message };
        }
    }

    /**
     * Ejecuta un experimento comparativo (corre los 5 algoritmos) en el backend y los guarda en MySQL.
     */
    static async runExperiment(scenario, quantum, name) {
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
     * Obtiene el listado de todos los experimentos guardados (CRUD: Read List).
     */
    static async getExperiments() {
        try {
            const response = await fetch(`${API_BASE_URL}/experiments`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Error al obtener la lista de experimentos');
            return await response.json();
        } catch (e) {
            console.error('API Error:', e);
            throw e;
        }
    }

    /**
     * Obtiene el detalle completo de un experimento por su ID (CRUD: Read Detail).
     */
    static async getExperimentDetail(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/experiments/${id}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Error al obtener el detalle del experimento');
            return await response.json();
        } catch (e) {
            console.error('API Error:', e);
            throw e;
        }
    }

    /**
     * Actualiza el nombre de un experimento (CRUD: Update).
     */
    static async updateExperimentName(id, name) {
        try {
            const response = await fetch(`${API_BASE_URL}/experiments/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name })
            });
            if (!response.ok) throw new Error('Error al actualizar el nombre del experimento');
            return await response.json();
        } catch (e) {
            console.error('API Error:', e);
            throw e;
        }
    }

    /**
     * Elimina un experimento de MySQL (CRUD: Delete).
     */
    static async deleteExperiment(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/experiments/${id}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });
            if (!response.ok) throw new Error('Error al eliminar el experimento');
            return await response.json();
        } catch (e) {
            console.error('API Error:', e);
            throw e;
        }
    }
}
window.SimulatorAPI = SimulatorAPI;
