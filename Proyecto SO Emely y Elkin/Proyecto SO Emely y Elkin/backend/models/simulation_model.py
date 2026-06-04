# ============================================================
# models/simulation_model.py — CRUD de Simulaciones en MySQL
# ============================================================
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.database import db


class Simulation:
    """
    Representa la ejecución de UN algoritmo dentro de un experimento.
    Maneja la persistencia en la tabla `simulations` y
    `simulation_processes`.
    """

    def __init__(self, experiment_id: int, algorithm: str,
                 avg_waiting_time: float = 0, avg_turnaround: float = 0,
                 throughput: float = 0, cpu_utilization: float = 0,
                 sim_id: int = None):
        self.id               = sim_id
        self.experiment_id    = experiment_id
        self.algorithm        = algorithm
        self.avg_waiting_time = avg_waiting_time
        self.avg_turnaround   = avg_turnaround
        self.throughput       = throughput
        self.cpu_utilization  = cpu_utilization

    # ----------------------------------------------------------
    # CREATE
    # ----------------------------------------------------------
    def save(self) -> int:
        """Inserta la simulación en MySQL y retorna el ID generado."""
        query = """
            INSERT INTO simulations
                (experiment_id, algorithm, avg_waiting_time,
                 avg_turnaround, throughput, cpu_utilization)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.id = db.execute_query(query, (
            self.experiment_id,
            self.algorithm,
            self.avg_waiting_time,
            self.avg_turnaround,
            self.throughput,
            self.cpu_utilization
        ))
        return self.id

    def save_processes(self, processes: list):
        """
        Inserta en batch los procesos individuales de esta simulación.
        processes: lista de dicts con claves pid, arrival_time, burst_time,
                   priority, completion_time, turnaround_time, waiting_time
        """
        if not processes:
            return
        query = """
            INSERT INTO simulation_processes
                (simulation_id, pid, arrival_time, burst_time, priority,
                 completion_time, turnaround_time, waiting_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = [
            (
                self.id,
                p['pid'],
                p['arrival_time'],
                p['burst_time'],
                p['priority'],
                p['completion_time'],
                p['turnaround_time'],
                p['waiting_time']
            )
            for p in processes
        ]
        db.execute_many(query, data)

    # ----------------------------------------------------------
    # READ
    # ----------------------------------------------------------
    @staticmethod
    def get_by_experiment(experiment_id: int) -> list:
        """Retorna todas las simulaciones de un experimento con sus métricas."""
        query = """
            SELECT id, experiment_id, algorithm,
                   avg_waiting_time, avg_turnaround,
                   throughput, cpu_utilization
            FROM simulations
            WHERE experiment_id = %s
            ORDER BY algorithm
        """
        return db.execute_query(query, (experiment_id,), fetch=True)

    @staticmethod
    def get_processes(simulation_id: int) -> list:
        """Retorna los procesos individuales de una simulación."""
        query = """
            SELECT pid, arrival_time, burst_time, priority,
                   completion_time, turnaround_time, waiting_time
            FROM simulation_processes
            WHERE simulation_id = %s
            ORDER BY pid
        """
        return db.execute_query(query, (simulation_id,), fetch=True)

    def to_dict(self) -> dict:
        return {
            'id'              : self.id,
            'experiment_id'   : self.experiment_id,
            'algorithm'       : self.algorithm,
            'avg_waiting_time': float(self.avg_waiting_time),
            'avg_turnaround'  : float(self.avg_turnaround),
            'throughput'      : float(self.throughput),
            'cpu_utilization' : float(self.cpu_utilization)
        }
