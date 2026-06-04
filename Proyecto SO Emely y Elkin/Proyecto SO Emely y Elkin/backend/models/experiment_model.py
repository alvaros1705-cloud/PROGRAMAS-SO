# ============================================================
# models/experiment_model.py — CRUD de Experimentos en MySQL
# ============================================================
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.database import db


class Experiment:
    """
    Agrupa varias simulaciones (una por algoritmo) bajo un mismo
    escenario y quantum, permitiendo la comparación entre algoritmos.
    """

    def __init__(self, name: str, scenario: str, num_processes: int,
                 quantum: int = 2, exp_id: int = None):
        self.id            = exp_id
        self.name          = name
        self.scenario      = scenario
        self.num_processes = num_processes
        self.quantum       = quantum

    # ----------------------------------------------------------
    # CREATE
    # ----------------------------------------------------------
    def save(self) -> int:
        """Inserta el experimento en MySQL y retorna su ID."""
        query = """
            INSERT INTO experiments (name, scenario, num_processes, quantum)
            VALUES (%s, %s, %s, %s)
        """
        self.id = db.execute_query(query, (
            self.name, self.scenario, self.num_processes, self.quantum
        ))
        return self.id

    # ----------------------------------------------------------
    # READ
    # ----------------------------------------------------------
    @staticmethod
    def get_all() -> list:
        """
        Lista todos los experimentos con sus métricas agregadas
        (una fila por algoritmo por experimento).
        """
        query = """
            SELECT
                e.id, e.name, e.scenario, e.num_processes, e.quantum,
                e.created_at,
                s.algorithm,
                s.avg_waiting_time, s.avg_turnaround,
                s.throughput, s.cpu_utilization
            FROM experiments e
            JOIN simulations s ON s.experiment_id = e.id
            ORDER BY e.created_at DESC, s.algorithm
        """
        rows = db.execute_query(query, fetch=True)
        # Agrupar por experimento
        experiments = {}
        for r in rows:
            eid = r['id']
            if eid not in experiments:
                experiments[eid] = {
                    'id'           : eid,
                    'name'         : r['name'],
                    'scenario'     : r['scenario'],
                    'num_processes': r['num_processes'],
                    'quantum'      : r['quantum'],
                    'created_at'   : str(r['created_at']),
                    'simulations'  : []
                }
            experiments[eid]['simulations'].append({
                'algorithm'       : r['algorithm'],
                'avg_waiting_time': float(r['avg_waiting_time'] or 0),
                'avg_turnaround'  : float(r['avg_turnaround'] or 0),
                'throughput'      : float(r['throughput'] or 0),
                'cpu_utilization' : float(r['cpu_utilization'] or 0)
            })
        return list(experiments.values())

    @staticmethod
    def get_by_id(exp_id: int) -> dict:
        """Retorna el detalle completo de un experimento con sus simulaciones."""
        # Datos del experimento
        exp_query = """
            SELECT id, name, scenario, num_processes, quantum, created_at
            FROM experiments WHERE id = %s
        """
        rows = db.execute_query(exp_query, (exp_id,), fetch=True)
        if not rows:
            return None
        exp = rows[0]
        result = {
            'id'           : exp['id'],
            'name'         : exp['name'],
            'scenario'     : exp['scenario'],
            'num_processes': exp['num_processes'],
            'quantum'      : exp['quantum'],
            'created_at'   : str(exp['created_at']),
            'simulations'  : []
        }

        # Simulaciones con sus procesos
        sims_query = """
            SELECT id, algorithm, avg_waiting_time, avg_turnaround,
                   throughput, cpu_utilization
            FROM simulations WHERE experiment_id = %s ORDER BY algorithm
        """
        sims = db.execute_query(sims_query, (exp_id,), fetch=True)
        for s in sims:
            procs_query = """
                SELECT pid, arrival_time, burst_time, priority,
                       completion_time, turnaround_time, waiting_time
                FROM simulation_processes WHERE simulation_id = %s
                ORDER BY pid
            """
            procs = db.execute_query(procs_query, (s['id'],), fetch=True)
            result['simulations'].append({
                'id'              : s['id'],
                'algorithm'       : s['algorithm'],
                'avg_waiting_time': float(s['avg_waiting_time'] or 0),
                'avg_turnaround'  : float(s['avg_turnaround'] or 0),
                'throughput'      : float(s['throughput'] or 0),
                'cpu_utilization' : float(s['cpu_utilization'] or 0),
                'processes'       : [dict(p) for p in procs]
            })
        return result

    # ----------------------------------------------------------
    # UPDATE
    # ----------------------------------------------------------
    @staticmethod
    def update_name(exp_id: int, new_name: str) -> bool:
        """Renombra un experimento."""
        query = "UPDATE experiments SET name = %s WHERE id = %s"
        db.execute_query(query, (new_name, exp_id))
        return True

    # ----------------------------------------------------------
    # DELETE
    # ----------------------------------------------------------
    @staticmethod
    def delete(exp_id: int) -> bool:
        """Elimina un experimento y en cascada sus simulaciones y procesos."""
        query = "DELETE FROM experiments WHERE id = %s"
        db.execute_query(query, (exp_id,))
        return True

    def to_dict(self) -> dict:
        return {
            'id'           : self.id,
            'name'         : self.name,
            'scenario'     : self.scenario,
            'num_processes': self.num_processes,
            'quantum'      : self.quantum
        }
