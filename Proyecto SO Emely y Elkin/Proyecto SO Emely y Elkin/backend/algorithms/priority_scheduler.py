# ============================================================
# algorithms/priority_scheduler.py — Priority Scheduling (No Expropiativo)
# ============================================================
from typing import List, Dict, Any
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from algorithms.base_algorithm import BaseScheduler
from models.process_model import Process


class PriorityScheduler(BaseScheduler):
    """Algoritmo de Prioridad - No expropiativo (menor número = mayor prioridad)."""

    def run(self, processes: List[Process], **kwargs) -> Dict[str, Any]:
        procs = [p.clone() for p in processes]
        current_time = 0
        timeline = []
        completed = []
        completed_count = 0
        n = len(procs)

        while completed_count < n:
            available = [p for p in procs if p.arrival_time <= current_time and not p.is_completed]
            
            if len(available) > 0:
                # Menor número de prioridad corre primero; si empatan, por tiempo de llegada
                available.sort(key=lambda x: (x.priority, x.arrival_time))
                current_proc = available[0]
                
                start = current_time
                current_time += current_proc.burst_time
                current_proc.completion_time = current_time
                current_proc.is_completed = True
                
                timeline.append({"pid": current_proc.pid, "start": start, "end": current_time})
                completed.append(current_proc)
                completed_count += 1
            else:
                current_time += 1

        return self.calculate_metrics(completed, timeline)
