# ============================================================
# models/process_model.py — Clase POO: Proceso
# ============================================================


class Process:
    """
    Representa un proceso del sistema operativo con sus atributos
    de planificación (llegada, ráfaga, prioridad) y los resultados
    calculados (completión, retorno, espera).
    """

    def __init__(self, pid: str, arrival_time: int, burst_time: int, priority: int = 1):
        # Atributos de entrada
        self.pid          = pid
        self.arrival_time = arrival_time
        self.burst_time   = burst_time
        self.priority     = priority

        # Atributos de ejecución (mutables)
        self.remaining_time  = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time    = 0
        self.is_completed    = False

    # ----------------------------------------------------------
    # Métodos de utilidad
    # ----------------------------------------------------------
    def clone(self) -> 'Process':
        """Retorna una copia independiente del proceso (para no mutar el original)."""
        return Process(
            pid          = self.pid,
            arrival_time = self.arrival_time,
            burst_time   = self.burst_time,
            priority     = self.priority
        )

    def to_dict(self) -> dict:
        """Serializa el proceso a dict para JSON / MySQL."""
        return {
            'pid'            : self.pid,
            'arrival_time'   : self.arrival_time,
            'burst_time'     : self.burst_time,
            'priority'       : self.priority,
            'completion_time': self.completion_time,
            'turnaround_time': self.turnaround_time,
            'waiting_time'   : self.waiting_time
        }

    def __repr__(self) -> str:
        return (f"Process(pid={self.pid}, arrival={self.arrival_time}, "
                f"burst={self.burst_time}, priority={self.priority})")

    # ----------------------------------------------------------
    # Factory: crea procesos desde dict (payload JSON o MySQL row)
    # ----------------------------------------------------------
    @classmethod
    def from_dict(cls, data: dict) -> 'Process':
        return cls(
            pid          = str(data.get('pid', 'Px')),
            arrival_time = int(data.get('arrivalTime', data.get('arrival_time', 0))),
            burst_time   = int(data.get('burstTime',  data.get('burst_time',  1))),
            priority     = int(data.get('priority', 1))
        )
