# ============================================================
# algorithms/base_algorithm.py — Clase abstracta base
# ============================================================
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.process_model import Process


class BaseScheduler(ABC):
    """
    Clase abstracta que define la interfaz común para todos los
    algoritmos de planificación de procesos de la CPU.
    """

    @abstractmethod
    def run(self, processes: List[Process], **kwargs) -> Dict[str, Any]:
        """
        Ejecuta el algoritmo de planificación.
        Retorna un diccionario con:
        - timeline: lista de bloques de tiempo {pid, start, end}
        - processes: lista de procesos completados con sus tiempos calculados
        - averages: {waiting_time, turnaround_time, throughput, cpu_utilization}
        """
        pass

    def calculate_metrics(self, completed_processes: List[Process], timeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcula las métricas de rendimiento globales del sistema."""
        total_turnaround = 0
        total_waiting = 0
        max_time = 0
        total_burst = 0

        for p in completed_processes:
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            total_turnaround += p.turnaround_time
            total_waiting += p.waiting_time
            total_burst += p.burst_time
            if p.completion_time > max_time:
                max_time = p.completion_time

        n = len(completed_processes)
        if n == 0 or max_time == 0:
            return {
                "processes": [p.to_dict() for p in completed_processes],
                "timeline": timeline,
                "averages": {
                    "waiting_time": 0.00,
                    "turnaround_time": 0.00,
                    "throughput": 0.0000,
                    "cpu_utilization": 0.00
                }
            }

        return {
            "processes": [p.to_dict() for p in completed_processes],
            "timeline": timeline,
            "averages": {
                "waiting_time": round(total_waiting / n, 2),
                "turnaround_time": round(total_turnaround / n, 2),
                "throughput": round(n / max_time, 6),
                "cpu_utilization": round((total_burst / max_time) * 100, 2)
            }
        }
