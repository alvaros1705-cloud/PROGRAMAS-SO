# ============================================================
# algorithms/fcfs.py — First Come, First Served (FCFS)
# ============================================================
from typing import List, Dict, Any
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from algorithms.base_algorithm import BaseScheduler
from models.process_model import Process


class FCFS(BaseScheduler):
    """Algoritmo de planificación First Come, First Served (FCFS) - No Expropiativo."""

    def run(self, processes: List[Process], **kwargs) -> Dict[str, Any]:
        # Clonar y ordenar por tiempo de llegada
        procs = [p.clone() for p in processes]
        procs.sort(key=lambda x: x.arrival_time)

        current_time = 0
        timeline = []
        completed = []

        for p in procs:
            if current_time < p.arrival_time:
                current_time = p.arrival_time  # CPU Idle
            
            start = current_time
            current_time += p.burst_time
            p.completion_time = current_time
            p.is_completed = True
            
            timeline.append({"pid": p.pid, "start": start, "end": current_time})
            completed.append(p)

        return self.calculate_metrics(completed, timeline)
