import pygame
import sys
import random
import json
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict, Set
from enum import Enum
import math
from datetime import datetime

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 200)
RED = (220, 50, 50)
GREEN = (50, 180, 80)
YELLOW = (255, 200, 50)
GRAY = (150, 150, 150)
LIGHT_BLUE = (100, 150, 255)
DARK_GRAY = (100, 100, 100)


class ResourceType(Enum):
    CPU = 1
    RAM = 2
    DISK = 3
    NETWORK = 4
    GPU = 5


@dataclass
class Process:
    pid: int
    name: str
    x: float
    y: float
    radius: int = 25
    color: Tuple = BLUE
    resources_needed: Dict[str, int] = None
    resources_holding: Dict[str, int] = None
    is_waiting: bool = False
    wait_time: int = 0
    total_acquired: int = 0
    total_released: int = 0
    
    def __post_init__(self):
        if self.resources_needed is None:
            self.resources_needed = {}
        if self.resources_holding is None:
            self.resources_holding = {}


@dataclass
class Resource:
    rid: int
    name: str
    x: float
    y: float
    total: int
    available: int
    width: int = 50
    height: int = 40
    color: Tuple = GREEN
    times_requested: int = 0
    times_allocated: int = 0
    
    def holding_count(self) -> int:
        return self.total - self.available


class Statistics:
   
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = None
        self.total_requests = 0
        self.total_deadlocks = 0
        self.max_wait_time = 0
        self.deadlock_occurrences = []
        self.process_stats = {}
        self.resource_stats = {}
    
    def to_dict(self):
        return {
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'duration_seconds': (self.end_time - self.start_time).total_seconds() if self.end_time else 0,
            'total_requests': self.total_requests,
            'total_deadlocks': self.total_deadlocks,
            'max_wait_time': self.max_wait_time,
            'deadlock_occurrences': self.deadlock_occurrences,
            'process_stats': self.process_stats,
            'resource_stats': self.resource_stats
        }


def interactive_menu_extended():
 

    print("\n" + "="*70)
    print("  TEMA 7: ALGORITMO DEL AVESTRUZ - CONFIGURACIÓN AVANZADA")
    print("="*70)
    
    # Procesos
    while True:
        try:
            num_processes = int(input("\n¿Cuántos procesos? (2-10, default=5): ") or "5")
            if 2 <= num_processes <= 10:
                break
            print("❌ Por favor, ingresa un número entre 2 y 10")
        except ValueError:
            print("❌ Entrada inválida. Intenta de nuevo.")
    
  
    while True:
        try:
            num_resources = int(input("¿Cuántos recursos? (1-5, default=3): ") or "3")
            if 1 <= num_resources <= 5:
                break
            print("❌ Por favor, ingresa un número entre 1 y 5")
        except ValueError:
            print("❌ Entrada inválida. Intenta de nuevo.")
    

    print("\n📊 Velocidad de simulación:")
    print("   1 = ULTRA LENTO (5 FPS)")
    print("   2 = Lento (15 FPS)")
    print("   3 = Normal (30 FPS)")
    print("   4 = Rápido (60 FPS)")
    
    while True:
        try:
            speed = int(input("Selecciona velocidad (1-4, default=2): ") or "2")
            if 1 <= speed <= 4:
                break
            print("❌ Por favor, ingresa un número entre 1 y 4")
        except ValueError:
            print("❌ Entrada inválida. Intenta de nuevo.")
  

    print("\n⚙️ Probabilidades (0-100%):")
    while True:
        try:
            request_prob = int(input("Probabilidad de solicitar recurso (0-100, default=40): ") or "40")
            if 0 <= request_prob <= 100:
                break
            print("❌ Por favor, ingresa un número entre 0 y 100")
        except ValueError:
            print("❌ Entrada inválida. Intenta de nuevo.")
    
    while True:
        try:
            release_prob = int(input("Probabilidad de liberar recurso (0-100, default=30): ") or "30")
            if 0 <= release_prob <= 100:
                break
            print("❌ Por favor, ingresa un número entre 0 y 100")
        except ValueError:
            print("❌ Entrada inválida. Intenta de nuevo.")
    
    print("\n" + "="*70)
    print("📋 DEFINICIÓN DE NECESIDADES DE PROCESOS")
    print("="*70)
    
    process_requirements = []
    resource_names = ["CPU", "RAM", "DISCO", "RED", "GPU"][:num_resources]
    
    for i in range(num_processes):
        print(f"\n🔹 Proceso P{i}:")
        requirements = {}
        for j, res_name in enumerate(resource_names):
            while True:
                try:
                    need = int(input(f"   ¿Cuántos {res_name} necesita? (0-3, default=1): ") or "1")
                    if 0 <= need <= 3:
                        requirements[res_name] = need
                        break
                    print("   ❌ Ingresa 0-3")
                except ValueError:
                    print("   ❌ Entrada inválida")
        process_requirements.append(requirements)
    

    fps_map = {1: 5, 2: 15, 3: 30, 4: 60}
    
    return {
        'num_processes': num_processes,
        'num_resources': num_resources,
        'fps': fps_map[speed],
        'request_prob': request_prob / 100.0,
        'release_prob': release_prob / 100.0,
        'process_requirements': process_requirements,
        'resource_names': resource_names
    }


class OstrichAlgorithmConfigurable:
  
    
    def __init__(self, width=1200, height=800, config=None):
        self.config = config or {
            'num_processes': 5,
            'num_resources': 3,
            'request_prob': 0.4,
            'release_prob': 0.3,
            'process_requirements': [],
            'resource_names': ["CPU", "RAM", "DISK"]
        }
        self.width = width
        self.height = height
        self.processes: List[Process] = []
        self.resources: List[Resource] = []
        self.edges: List[Tuple[int, int, str]] = []
        self.time = 0
        self.deadlock_detected = False
        self.system_running = True
        self.statistics = Statistics()
        
        self._create_dynamic_state()
    
    def _create_dynamic_state(self):
    
        num_procs = self.config['num_processes']
        spacing_y = 700 // (num_procs + 1)


        for i in range(num_procs):
            requirements = self.config['process_requirements'][i] if i < len(self.config['process_requirements']) else {}
            
            process = Process(
                pid=i,
                name=f"P{i}",
                x=150,
                y=100 + (i + 1) * spacing_y,
                color=LIGHT_BLUE,
                resources_needed=requirements.copy() if requirements else {},
                resources_holding={}
            )
            self.processes.append(process)
        

        num_res = self.config['num_resources']
        resource_names = self.config['resource_names'][:num_res]
        
        spacing_x = 300 // (num_res + 1)
        
        for rid, name in enumerate(resource_names):
            total = random.randint(2, 5)
            resource = Resource(
                rid=rid,
                name=name,
                x=900 + (rid + 1) * spacing_x - 100,
                y=300,
                total=total,
                available=total,
                color=GREEN
            )
            self.resources.append(resource)
    
    def request_resource(self, process_id: int, resource_id: int, amount: int) -> bool:
    
        if process_id >= len(self.processes) or resource_id >= len(self.resources):
            return False
        
        process = self.processes[process_id]
        resource = self.resources[resource_id]
        resource_name = resource.name
        
        if resource.available >= amount:
            resource.available -= amount
            
            if resource_name not in process.resources_holding:
                process.resources_holding[resource_name] = 0
            process.resources_holding[resource_name] += amount
            
            self.edges.append((process_id, resource_id, 'allocation'))
            process.is_waiting = False
            process.total_acquired += amount
            resource.times_allocated += 1
            
            return True
        else:
            self.edges.append((process_id, resource_id, 'request'))
            process.is_waiting = True
            resource.times_requested += 1
            return False
    
    def detect_deadlock(self) -> Tuple[bool, Set[int]]:
     
        waiting_processes = {p.pid for p in self.processes if p.is_waiting}
        
        if len(waiting_processes) >= 2:
            return True, waiting_processes
        
        return False, set()
    
    def simulate_step(self):
  
        if not self.system_running:
            return
        
        self.time += 1
        self.statistics.total_requests += 1
        
 
        if random.random() < self.config['request_prob']:
            pid = random.randint(0, len(self.processes) - 1)
            rid = random.randint(0, len(self.resources) - 1)
            self.request_resource(pid, rid, 1)
        

        if random.random() < self.config['release_prob']:
            for process in self.processes:
                if process.resources_holding:
                    resource_name = random.choice(list(process.resources_holding.keys()))
                    amount = process.resources_holding[resource_name]
                    
                    for resource in self.resources:
                        if resource.name == resource_name:
                            resource.available = min(resource.available + amount, resource.total)
                            del process.resources_holding[resource_name]
                            process.is_waiting = False
                            process.total_released += amount
                            break
                    
                    self.edges = [(f, t, ty) for f, t, ty in self.edges 
                                 if not (f == process.pid)]
                    break
        
  
        deadlock_detected, deadlock_processes = self.detect_deadlock()
        
        if deadlock_detected:
            self.deadlock_detected = True
            self.statistics.total_deadlocks += 1
            self.statistics.deadlock_occurrences.append(self.time)
            
            for pid in deadlock_processes:
                if pid < len(self.processes):
                    self.processes[pid].color = RED
                    self.processes[pid].wait_time += 1
        else:
            self.deadlock_detected = False
            for process in self.processes:
                process.color = LIGHT_BLUE if not process.is_waiting else YELLOW
                if process.is_waiting:
                    process.wait_time += 1
                    self.statistics.max_wait_time = max(self.statistics.max_wait_time, process.wait_time)


class VisualizerConfigurable:
    def __init__(self, config=None):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("TEMA 7: Algoritmo del Avestruz - COMPLETO")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
        self.font_title = pygame.font.Font(None, 48)
        
        self.config = config or {}
        self.algorithm = OstrichAlgorithmConfigurable(1200, 800, self.config)
        self.running = True
        self.paused = False
    
    def draw_process(self, process: Process):
       
        pygame.draw.circle(self.screen, process.color, (int(process.x), int(process.y)), process.radius)
        pygame.draw.circle(self.screen, BLACK, (int(process.x), int(process.y)), process.radius, 2)
        
        text = self.font_small.render(process.name, True, BLACK)
        self.screen.blit(text, (int(process.x) - 10, int(process.y) - 10))
        
        resources_text = ", ".join([f"{name}:{amount}" 
                                   for name, amount in process.resources_holding.items()])
        if resources_text:
            res_surf = self.font_small.render(resources_text, True, BLACK)
            self.screen.blit(res_surf, (int(process.x) - 60, int(process.y) + 35))
    
    def draw_resource(self, resource: Resource):
       
        pygame.draw.rect(self.screen, resource.color, 
                        (resource.x - resource.width//2, resource.y - resource.height//2,
                         resource.width, resource.height))
        pygame.draw.rect(self.screen, BLACK,
                        (resource.x - resource.width//2, resource.y - resource.height//2,
                         resource.width, resource.height), 2)
        
        text = self.font_small.render(resource.name, True, BLACK)
        self.screen.blit(text, (int(resource.x) - 20, int(resource.y) - 10))
        
        avail_text = self.font_small.render(f"{resource.available}/{resource.total}", True, BLACK)
        self.screen.blit(avail_text, (int(resource.x) - 30, int(resource.y) + 10))
    
    def draw_edges(self):
        
        for from_id, to_id, edge_type in self.algorithm.edges:
            if from_id >= len(self.algorithm.processes) or to_id >= len(self.algorithm.resources):
                continue
            
            process = self.algorithm.processes[from_id]
            resource = self.algorithm.resources[to_id]
            
            color = YELLOW if edge_type == 'request' else GREEN
            line_width = 3 if edge_type == 'request' else 2
            
            pygame.draw.line(self.screen, color,
                           (int(process.x), int(process.y)),
                           (int(resource.x), int(resource.y)),
                           line_width)
            
            angle = math.atan2(resource.y - process.y, resource.x - process.x)
            arrow_size = 10
            end_x = resource.x - math.cos(angle) * (resource.width // 2)
            end_y = resource.y - math.sin(angle) * (resource.height // 2)
            
            pygame.draw.polygon(self.screen, color, [
                (end_x, end_y),
                (end_x - arrow_size * math.cos(angle - math.pi / 6),
                 end_y - arrow_size * math.sin(angle - math.pi / 6)),
                (end_x - arrow_size * math.cos(angle + math.pi / 6),
                 end_y - arrow_size * math.sin(angle + math.pi / 6))
            ])
    
    def draw_info(self):
        
        title = self.font_title.render("ALGORITMO DEL AVESTRUZ", True, BLACK)
        self.screen.blit(title, (30, 20))
        
        time_text = self.font_small.render(f"Tiempo: {self.algorithm.time}s", True, BLACK)
        self.screen.blit(time_text, (30, 80))
        
        config_text = f"P:{len(self.algorithm.processes)} R:{len(self.algorithm.resources)} FPS:{self.config.get('fps', 30)}"
        config_surf = self.font_small.render(config_text, True, DARK_GRAY)
        self.screen.blit(config_surf, (30, 120))
        
        deadlocks_text = f"Deadlocks: {self.algorithm.statistics.total_deadlocks}"
        deadlocks_surf = self.font_small.render(deadlocks_text, True, RED)
        self.screen.blit(deadlocks_surf, (30, 160))
        
        status = "DEADLOCK DETECTADO!" if self.algorithm.deadlock_detected else "Sistema Normal"
        status_color = RED if self.algorithm.deadlock_detected else GREEN
        status_text = self.font_small.render(status, True, status_color)
        self.screen.blit(status_text, (30, 200))
        
        if self.paused:
            pause_text = self.font_large.render("PAUSADO", True, RED)
            self.screen.blit(pause_text, (450, 350))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.algorithm = OstrichAlgorithmConfigurable(1200, 800, self.config)
                elif event.key == pygame.K_q:
                    self.running = False
    
    def show_final_report(self):
        
        self.algorithm.statistics.end_time = datetime.now()
        
        print("\n" + "="*70)
        print("📊 REPORTE FINAL - SIMULACIÓN DEL ALGORITMO DEL AVESTRUZ")
        print("="*70)
        
        stats = self.algorithm.statistics.to_dict()
        
        print(f"\n⏱️ DURACIÓN")
        print(f"   Inicio: {stats['start_time']}")
        print(f"   Fin: {stats['end_time']}")
        print(f"   Duración total: {stats['duration_seconds']:.2f} segundos")
        
        print(f"\n📈 ESTADÍSTICAS GENERALES")
        print(f"   Solicitudes totales: {stats['total_requests']}")
        print(f"   Deadlocks detectados: {stats['total_deadlocks']}")
        print(f"   Tiempo máximo de espera: {stats['max_wait_time']} iteraciones")
        
        print(f"\n💾 ESTADÍSTICAS POR PROCESO")
        for i, process in enumerate(self.algorithm.processes):
            print(f"\n   Proceso P{i}:")
            print(f"      Recursos adquiridos: {process.total_acquired}")
            print(f"      Recursos liberados: {process.total_released}")
            print(f"      Tiempo de espera acumulado: {process.wait_time} iteraciones")
        
        print(f"\n🔧 ESTADÍSTICAS POR RECURSO")
        for i, resource in enumerate(self.algorithm.resources):
            print(f"\n   Recurso {resource.name}:")
            print(f"      Total: {resource.total}")
            print(f"      Solicitudes: {resource.times_requested}")
            print(f"      Asignaciones: {resource.times_allocated}")
        
        if stats['total_deadlocks'] > 0:
            print(f"\n⚠️ DEADLOCKS DETECTADOS EN TIEMPOS:")
            for t in stats['deadlock_occurrences']:
                print(f"      - Tiempo {t}")
        
        print("\n" + "="*70)
        
        
        json_filename = f"reporte_simulacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        json_path = f"/Users/juanfernandojaimesperez/Desktop/TRABAJOS SISTEMAS OPERATIVOS/{json_filename}"
        
        report_data = {
            'configuracion': {
                'procesos': len(self.algorithm.processes),
                'recursos': len(self.algorithm.resources),
                'fps': self.config.get('fps', 30),
                'probabilidad_solicitud': self.config.get('request_prob', 0.4),
                'probabilidad_liberacion': self.config.get('release_prob', 0.3)
            },
            'estadisticas': stats,
            'procesos': [
                {
                    'id': p.pid,
                    'nombre': p.name,
                    'recursos_adquiridos': p.total_acquired,
                    'recursos_liberados': p.total_released,
                    'tiempo_espera': p.wait_time,
                    'recursos_necesarios': p.resources_needed
                }
                for p in self.algorithm.processes
            ],
            'recursos': [
                {
                    'id': r.rid,
                    'nombre': r.name,
                    'total': r.total,
                    'solicitudes': r.times_requested,
                    'asignaciones': r.times_allocated
                }
                for r in self.algorithm.resources
            ]
        }
        
        with open(json_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Reporte guardado en: {json_filename}")
    
    def run(self):
        while self.running:
            self.handle_events()
            
            if not self.paused:
                self.algorithm.simulate_step()
            
            self.screen.fill(WHITE)
            
            self.draw_edges()
            for process in self.algorithm.processes:
                self.draw_process(process)
            for resource in self.algorithm.resources:
                self.draw_resource(resource)
            
            self.draw_info()
            
            controls = self.font_small.render("SPACE: Pausar/Reanudar | R: Reiniciar | Q: Salir", 
                                             True, DARK_GRAY)
            self.screen.blit(controls, (30, 750))
            
            pygame.display.flip()
            self.clock.tick(self.config.get('fps', 30))
        
        self.show_final_report()
        pygame.quit()


if __name__ == "__main__":
    config = interactive_menu_extended()
    
    print("\n" + "="*70)
    print("  ✅ INICIANDO SIMULACIÓN...")
    print("="*70)
    print(f"  • Procesos: {config['num_processes']}")
    print(f"  • Recursos: {config['num_resources']}")
    print(f"  • FPS: {config['fps']}")
    print(f"  • Probabilidad de solicitud: {config['request_prob']*100:.0f}%")
    print(f"  • Probabilidad de liberación: {config['release_prob']*100:.0f}%")
    print("="*70 + "\n")
    
    visualizer = VisualizerConfigurable(config)
    visualizer.run()
