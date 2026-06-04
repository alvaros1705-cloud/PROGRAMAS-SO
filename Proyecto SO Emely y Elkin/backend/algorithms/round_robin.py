# ============================================================
# algorithms/round_robin.py — Round Robin (RR)
# ============================================================
from typing import List, Dict, Any
from collections import deque
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from algorithms.base_algorithm import BaseScheduler
from models.process_model import Process


class RoundRobin(BaseScheduler):
    """Algoritmo Round Robin (RR) - Expropiativo con Quantum."""

    def run(self, processes: List[Process], **kwargs) -> Dict[str, Any]:
        quantum = int(kwargs.get('quantum', 2))
        
        # Clonar y ordenar por tiempo de llegada
        procs = [p.clone() for p in processes]
        procs.sort(key=lambda x: x.arrival_time)
        
        current_time = 0
        timeline = []
        ready_queue = deque()
        completed = []
        completed_count = 0
        n = len(procs)
        
        index = 0  # Índice para procesos que van llegando
        
        def enqueue_arrivals():
            nonlocal index
            while index < n and procs[index].arrival_time <= current_time:
                ready_queue.append(procs[index])
                index += 1

        enqueue_arrivals()

        while completed_count < n:
            if not ready_queue:
                current_time += 1
                enqueue_arrivals()
                continue

            current_proc = ready_queue.popleft()
            start = current_time
            
            time_to_execute = min(current_proc.remaining_time, quantum)
            current_time += time_to_execute
            current_proc.remaining_time -= time_to_execute
            
            timeline.append({"pid": current_proc.pid, "start": start, "end": current_time})
            
            enqueue_arrivals()  # Encolar nuevos procesos antes de volver a encolar el actual
            
            if current_proc.remaining_time > 0:
                ready_queue.append(current_proc)
            else:
                current_proc.completion_time = current_time
                current_proc.is_completed = True
                completed.append(current_proc)
                completed_count += 1

        return self.calculate_metrics(completed, timeline)
