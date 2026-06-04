# ============================================================
# algorithms/mlq.py — Multilevel Queue (MLQ) simplificado
# ============================================================
from typing import List, Dict, Any
from collections import deque
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from algorithms.base_algorithm import BaseScheduler
from models.process_model import Process


class MLQ(BaseScheduler):
    """
    Multilevel Queue (MLQ) simplificado.
    - Cola 1: Prioridad 1 y 2 (Round Robin con Q=2)
    - Cola 2: Prioridad 3, 4 y 5 (FCFS)
    """

    def run(self, processes: List[Process], **kwargs) -> Dict[str, Any]:
        procs = [p.clone() for p in processes]
        procs.sort(key=lambda x: x.arrival_time)
        
        current_time = 0
        timeline = []
        completed = []
        
        q1 = deque()  # RR q=2
        q2 = deque()  # FCFS
        
        completed_count = 0
        n = len(procs)
        index = 0

        def enqueue_arrivals():
            nonlocal index
            while index < n and procs[index].arrival_time <= current_time:
                # Prioridad 1 y 2 van a Q1; el resto a Q2
                if procs[index].priority <= 2:
                    q1.append(procs[index])
                else:
                    q2.append(procs[index])
                index += 1

        enqueue_arrivals()

        while completed_count < n:
            if not q1 and not q2:
                current_time += 1
                enqueue_arrivals()
                continue

            # Prioridad absoluta para Q1
            if q1:
                current_proc = q1.popleft()
                start = current_time
                quantum = 2
                
                time_to_execute = min(current_proc.remaining_time, quantum)
                current_time += time_to_execute
                current_proc.remaining_time -= time_to_execute
                
                timeline.append({"pid": current_proc.pid, "queue": "Q1 (RR)", "start": start, "end": current_time})
                enqueue_arrivals()

                if current_proc.remaining_time > 0:
                    q1.append(current_proc)
                else:
                    current_proc.completion_time = current_time
                    current_proc.is_completed = True
                    completed.append(current_proc)
                    completed_count += 1
            else:
                # Si Q1 está vacía, se ejecuta Q2 (FCFS)
                current_proc = q2.popleft()
                start = current_time
                
                # FCFS corre hasta finalizar
                current_time += current_proc.burst_time
                current_proc.remaining_time = 0
                
                timeline.append({"pid": current_proc.pid, "queue": "Q2 (FCFS)", "start": start, "end": current_time})
                enqueue_arrivals()
                
                current_proc.completion_time = current_time
                current_proc.is_completed = True
                completed.append(current_proc)
                completed_count += 1

        return self.calculate_metrics(completed, timeline)
