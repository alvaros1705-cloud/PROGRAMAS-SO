# ============================================================
# controllers/experiment_controller.py — Controlador de Experimentos
# ============================================================
from flask import Blueprint, request, jsonify
import sys, os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.process_model import Process
from models.experiment_model import Experiment
from models.simulation_model import Simulation

# Algoritmos
from algorithms.fcfs import FCFS
from algorithms.sjf import SJF
from algorithms.round_robin import RoundRobin
from algorithms.priority_scheduler import PriorityScheduler
from algorithms.mlq import MLQ

experiment_api = Blueprint('experiment_api', __name__)

# Generador de procesos para cargas de trabajo C y D (para simetría con js/simulator.js)
def generate_random_processes(count: int) -> list:
    procs = []
    # Usar una semilla aleatoria consistente o aleatoria pura
    for i in range(1, count + 1):
        procs.append(Process(
            pid=f"P{i}",
            arrival_time=random.randint(0, count * 2),
            burst_time=random.randint(1, 15),
            priority=random.randint(1, 5)
        ))
    procs.sort(key=lambda x: x.arrival_time)
    return procs

# Escenarios predefinidos locales para consistencia
SCENARIOS = {
    "A": [
        Process("P1", 0, 5, 3),
        Process("P2", 1, 3, 1),
        Process("P3", 2, 8, 4),
        Process("P4", 3, 2, 2),
        Process("P5", 4, 4, 5)
    ],
    "B": [
        Process("P1", 0, 6, 2),
        Process("P2", 1, 4, 4),
        Process("P3", 2, 9, 1),
        Process("P4", 2, 2, 5),
        Process("P5", 3, 5, 3),
        Process("P6", 4, 7, 2),
        Process("P7", 5, 3, 4),
        Process("P8", 5, 1, 1),
        Process("P9", 6, 8, 5),
        Process("P10", 7, 4, 3),
        Process("P11", 8, 6, 2),
        Process("P12", 9, 2, 4),
        Process("P13", 10, 5, 1),
        Process("P14", 11, 7, 5),
        Process("P15", 12, 3, 3),
        Process("P16", 13, 8, 2),
        Process("P17", 14, 4, 4),
        Process("P18", 15, 1, 1),
        Process("P19", 16, 6, 5),
        Process("P20", 17, 2, 3)
    ]
}


@experiment_api.route('/api/experiments', methods=['POST'])
def run_experiment():
    """
    Ejecuta un experimento de planificación de procesos:
    1. Carga o genera la lista de procesos según el escenario.
    2. Ejecuta FCFS, SJF, RR, PRIORITY, y MLQ en el mismo escenario.
    3. Registra el Experimento en MySQL.
    4. Guarda los resultados y procesos de cada simulación en MySQL.
    5. Retorna la comparación completa.
    """
    try:
        data = request.json or {}
        scenario = data.get('scenario', 'A')
        quantum = int(data.get('quantum', 2))
        custom_name = data.get('name', f"Comparativa Escenario {scenario}")

        # Cargar u obtener procesos de la carga
        if scenario == 'A':
            base_procs = [p.clone() for p in SCENARIOS['A']]
        elif scenario == 'B':
            base_procs = [p.clone() for p in SCENARIOS['B']]
        elif scenario == 'C':
            base_procs = generate_random_processes(100)
        elif scenario == 'D':
            base_procs = generate_random_processes(500)
        else:
            # Procesos personalizados recibidos por request
            custom_procs = data.get('processes', [])
            if not custom_procs:
                return jsonify({"error": "Escenario o procesos inválidos"}), 400
            base_procs = [Process.from_dict(p) for p in custom_procs]
            scenario = "CUSTOM"

        num_processes = len(base_procs)

        # Crear el Experimento en la base de datos
        experiment = Experiment(name=custom_name, scenario=scenario, num_processes=num_processes, quantum=quantum)
        exp_id = experiment.save()

        # Instanciar algoritmos
        algorithms = {
            "FCFS": FCFS(),
            "SJF": SJF(),
            "RR": RoundRobin(),
            "PRIORITY": PriorityScheduler(),
            "MLQ": MLQ()
        }

        comparison_results = {}

        for algo_name, algo_instance in algorithms.items():
            # Ejecutar simulación
            result = algo_instance.run(base_procs, quantum=quantum)
            
            # Guardar Simulación en DB
            sim = Simulation(
                experiment_id=exp_id,
                algorithm=algo_name,
                avg_waiting_time=result['averages']['waiting_time'],
                avg_turnaround=result['averages']['turnaround_time'],
                throughput=result['averages']['throughput'],
                cpu_utilization=result['averages']['cpu_utilization']
            )
            sim_id = sim.save()
            
            # Guardar procesos de la simulación
            sim.save_processes(result['processes'])

            # Añadir a la respuesta
            comparison_results[algo_name] = {
                "id": sim_id,
                "averages": result['averages'],
                "timeline": result['timeline'],
                "processes": result['processes']
            }

        return jsonify({
            "message": "Experimento completado y guardado en SQLite con éxito.",
            "experiment_id": exp_id,
            "name": custom_name,
            "scenario": scenario,
            "num_processes": num_processes,
            "quantum": quantum,
            "results": comparison_results
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@experiment_api.route('/api/experiments', methods=['GET'])
def get_all_experiments():
    """Obtiene la lista de todos los experimentos ejecutados."""
    try:
        experiments = Experiment.get_all()
        return jsonify(experiments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@experiment_api.route('/api/experiments/<int:exp_id>', methods=['GET'])
def get_experiment_detail(exp_id):
    """Obtiene el detalle completo de un experimento."""
    try:
        experiment = Experiment.get_by_id(exp_id)
        if not experiment:
            return jsonify({"error": "Experimento no encontrado"}), 404
        return jsonify(experiment), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@experiment_api.route('/api/experiments/<int:exp_id>', methods=['PUT'])
def update_experiment_name(exp_id):
    """Actualiza el nombre de un experimento."""
    try:
        data = request.json or {}
        new_name = data.get('name')
        if not new_name:
            return jsonify({"error": "El nombre es requerido"}), 400
        
        success = Experiment.update_name(exp_id, new_name)
        return jsonify({"message": "Nombre de experimento actualizado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@experiment_api.route('/api/experiments/<int:exp_id>', methods=['DELETE'])
def delete_experiment(exp_id):
    """Elimina un experimento y sus datos relacionados."""
    try:
        success = Experiment.delete(exp_id)
        return jsonify({"message": "Experimento eliminado con éxito de SQLite"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
