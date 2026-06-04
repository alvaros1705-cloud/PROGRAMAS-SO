# ============================================================
# algorithms/sjf.py — Shortest Job First (SJF) No Expropiativo
# ============================================================
from typing import List, Dict, Any
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from algorithms.base_algorithm import BaseScheduler
from models.process_model import Process


class SJF(BaseScheduler):
    """Algoritmo Shortest Job First (SJF) - No Expropiativo."""

    def run(self, processes: List[Process], **kwargs) -> Dict[str, Any]:
        procs = [p.clone() for p in processes]
        current_time = 0
        timeline = []
        completed = []
        n = len(procs)
        completed_count = 0

        while completed_count < n:
            # Obtener procesos que ya llegaron y no han sido completados
            available = [p for p in procs if p.arrival_time <= current_time and not p.is_completed]
            
            if len(available) > 0:
                # Ordenar por ráfaga más corta (burst_time) y desempate por tiempo de llegada
                available.sort(key=lambda x: (x.burst_time, x.arrival_time))
                current_proc = available[0]
                
                start = current_time
                current_time += current_proc.burst_time
                current_proc.completion_time = current_time
                current_proc.is_completed = True
                
                timeline.append({"pid": current_proc.pid, "start": start, "end": current_time})
                completed.append(current_proc)
                completed_count += 1
            else:
                current_time += 1  # CPU Idle

        return self.calculate_metrics(completed, timeline)
