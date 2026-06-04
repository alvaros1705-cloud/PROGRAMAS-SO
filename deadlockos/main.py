"""
DeadlockOS — Backend principal (Flask)
Ejecutar: python main.py
"""
from flask import Flask, request, jsonify, render_template
from typing import List, Dict
import time

app = Flask(__name__)

# ── Colores para procesos ──────────────────────
COLORS = ["#2288ff","#8855ff","#ffaa00","#00ff88","#ff5577","#00ddbb","#ff7700"]

# ─────────────────────────────────────────────
# Modelos
# ─────────────────────────────────────────────
class Process:
    def __init__(self, id, color="#2288ff", state="idle"):
        self.id    = id
        self.color = color
        self.state = state
        self.holds: List[str] = []
        self.waiting: str | None = None

    def to_dict(self):
        return {"id": self.id, "color": self.color,
                "state": self.state, "holds": self.holds, "waiting": self.waiting}

class Resource:
    def __init__(self, id, total=1):
        self.id        = id
        self.total     = total
        self.available = total
        self.heldBy:  List[str] = []

    def to_dict(self):
        return {"id": self.id, "total": self.total,
                "available": self.available, "heldBy": self.heldBy}


# Estado global del simulador

processes: List[Process] = []
resources: List[Resource] = []
event_log: List[dict]    = []
pid_counter = 1
rid_counter = 1

def _reset():
    global processes, resources, event_log, pid_counter, rid_counter
    processes, resources, event_log = [], [], []
    pid_counter = rid_counter = 1

def _log(msg: str, kind: str = "i"):
    event_log.insert(0, {"msg": msg, "kind": kind, "ts": time.strftime("%H:%M:%S")})
    if len(event_log) > 80:
        event_log.pop()

def _proc(pid) -> Process | None:
    return next((p for p in processes if p.id == pid), None)

def _res(rid) -> Resource | None:
    return next((r for r in resources if r.id == rid), None)

# Detección de deadlock — Coffman

def find_cycle() -> List[str]:
    """DFS sobre el grafo de espera (RAG). Devuelve los nodos del ciclo."""
    adj: Dict[str, List[str]] = {p.id: [] for p in processes}
    res_map = {r.id: r for r in resources}
    for p in processes:
        if p.waiting and p.waiting in res_map:
            for holder in res_map[p.waiting].heldBy:
                if holder != p.id:
                    adj[p.id].append(holder)

    visited, in_stack, cycle = {}, {}, []

    def dfs(node, path):
        visited[node] = in_stack[node] = True
        for nb in adj.get(node, []):
            if not visited.get(nb):
                if dfs(nb, path + [nb]):
                    return True
            elif in_stack.get(nb):
                i = path.index(nb) if nb in path else 0
                cycle.extend(path[i:])
                return True
        in_stack[node] = False
        return False

    for p in processes:
        if not visited.get(p.id):
            dfs(p.id, [p.id])

    return list(dict.fromkeys(cycle))

def coffman_status() -> dict:
    cycle = find_cycle()
    return {
        "mutual_exclusion": any(r.heldBy for r in resources),
        "hold_wait":        any(p.holds and p.waiting for p in processes),
        "no_preemption":    any(p.holds and p.waiting for p in processes),
        "circular_wait":    bool(cycle),
        "deadlock":         bool(cycle),
        "cycle":            cycle,
    }

def _state_response(extra=None):
    c = coffman_status()
    if c["deadlock"]:
        _log(f"⚠ DEADLOCK: {' → '.join(c['cycle'])}", "e")
    data = {
        "ok": True,
        "processes": [p.to_dict() for p in processes],
        "resources":  [r.to_dict() for r in resources],
        "coffman": c,
        "log": event_log[:20],
    }
    if extra:
        data.update(extra)
    return jsonify(data)


# Rutas HTML

@app.get("/")          
def boot():      return render_template("boot.html")
@app.get("/login")     
def login():     return render_template("login.html")
@app.get("/desktop")   
def desktop():   return render_template("desktop.html")
@app.get("/intro")     
def intro():     return render_template("intro.html")
@app.get("/recursos")  
def recursos():  return render_template("recursos.html")
@app.get("/coffman")   
def coffman():   return render_template("coffman.html")
@app.get("/simulador") 
def simulador(): return render_template("simulador.html")
@app.get("/resumen")   
def resumen():   return render_template("resumen.html")


# API — Autenticación

@app.post("/api/auth")
def authenticate():
    d = request.get_json() or {}
    ok = d.get("user") in ("estudiante", "guest") and d.get("password") == "1234"
    if not ok:
        return jsonify({"detail": "Credenciales incorrectas"}), 401
    return jsonify({"ok": True, "user": d["user"], "role": "student"})


# API — Estado del simulador

@app.get("/api/sim/state")
def get_state():
    return _state_response()


# API — Acciones del simulador

@app.post("/api/sim/action")
def sim_action():
    global pid_counter, rid_counter
    d      = request.get_json() or {}
    action = d.get("action")
    pid    = d.get("pid")
    rid    = d.get("rid")

    # ── Resetear ──────────────────────────────
    if action == "reset":
        _reset()
        _log("Simulador reiniciado", "i")

    # ── Agregar proceso ───────────────────────
    elif action == "add_process":
        p = Process(id=f"P{pid_counter}", color=COLORS[(len(processes)) % len(COLORS)])
        pid_counter += 1
        processes.append(p)
        _log(f"{p.id} creado", "i")

    # ── Agregar recurso ───────────────────────
    elif action == "add_resource":
        r = Resource(id=f"R{rid_counter}")
        rid_counter += 1
        resources.append(r)
        _log(f"{r.id} creado", "i")

    # ── Asignar recurso a proceso ─────────────
    elif action == "assign":
        p, r = _proc(pid), _res(rid)
        if not p or not r:
            return jsonify({"detail": "Proceso o recurso no encontrado"}), 400
        if r.available <= 0:
            return jsonify({"detail": f"{rid} sin instancias disponibles"}), 400
        if rid in p.holds:
            return jsonify({"detail": f"{pid} ya retiene {rid}"}), 400
        r.available -= 1; r.heldBy.append(pid)
        p.holds.append(rid); p.state = "running"
        if p.waiting == rid: p.waiting = None
        _log(f"{pid} obtuvo {rid}", "s")
        # Resolver esperas pendientes
        for other in processes:
            if other.waiting == rid and r.available > 0:
                r.available -= 1; r.heldBy.append(other.id)
                other.holds.append(rid); other.waiting = None; other.state = "running"
                _log(f"{other.id} obtuvo {rid} (espera resuelta)", "s")
                break

    # ── Solicitar recurso (bloquearse) ────────
    elif action == "request":
        p, r = _proc(pid), _res(rid)
        if not p or not r:
            return jsonify({"detail": "Proceso o recurso no encontrado"}), 400
        if rid in p.holds:
            return jsonify({"detail": f"{pid} ya tiene {rid}"}), 400
        if r.available > 0:
            return jsonify({"detail": f"{rid} está disponible — usa 'assign'"}), 400
        p.waiting = rid; p.state = "blocked"
        _log(f"{pid} espera {rid} (bloqueado)", "w")

    # ── Liberar recurso ───────────────────────
    elif action == "release":
        p, r = _proc(pid), _res(rid)
        if not p or not r:
            return jsonify({"detail": "Proceso o recurso no encontrado"}), 400
        if rid not in p.holds:
            return jsonify({"detail": f"{pid} no retiene {rid}"}), 400
        r.available += 1
        r.heldBy = [x for x in r.heldBy if x != pid]
        p.holds   = [x for x in p.holds   if x != rid]
        if not p.holds and not p.waiting: p.state = "idle"
        _log(f"{pid} liberó {rid}", "s")
        for other in processes:
            if other.waiting == rid and r.available > 0:
                r.available -= 1; r.heldBy.append(other.id)
                other.holds.append(rid); other.waiting = None; other.state = "running"
                _log(f"{other.id} obtuvo {rid} (espera resuelta)", "s")
                break

    # ── Eliminar proceso ──────────────────────
    elif action == "remove_process":
        p = _proc(pid)
        if not p:
            return jsonify({"detail": "Proceso no encontrado"}), 400
        for held_rid in p.holds:
            r = _res(held_rid)
            if r:
                r.available += 1
                r.heldBy = [x for x in r.heldBy if x != pid]
        for r in resources:
            r.heldBy = [x for x in r.heldBy if x != pid]
        processes[:] = [x for x in processes if x.id != pid]
        _log(f"{pid} eliminado", "w")

    # ── Eliminar recurso ──────────────────────
    elif action == "remove_resource":
        r = _res(rid)
        if not r:
            return jsonify({"detail": "Recurso no encontrado"}), 400
        for p in processes:
            if rid in p.holds:
                p.holds = [x for x in p.holds if x != rid]
                if not p.holds and not p.waiting: p.state = "idle"
            if p.waiting == rid:
                p.waiting = None
                p.state = "idle" if not p.holds else "running"
        resources[:] = [x for x in resources if x.id != rid]
        _log(f"{rid} eliminado", "w")

    # ── Cargar escenario preset ───────────────
    elif action == "preset":
        _reset()
        {"simple": _preset_simple, "triangle": _preset_triangle,
         "safe": _preset_safe, "complex": _preset_complex
        }.get(d.get("preset",""), lambda: None)()
        _log(f"Escenario '{d.get('preset')}' cargado", "w")

    return _state_response()


# API — Datos educativos (solo lectura)

@app.get("/api/coffman/theory")
def coffman_theory():
    return jsonify({"conditions": [
        {"id":1,"name":"Exclusión Mutua",  "key":"mutual_exclusion",
         "desc":"Al menos un recurso es de uso exclusivo: solo un proceso puede usarlo a la vez."},
        {"id":2,"name":"Retención y Espera","key":"hold_wait",
         "desc":"Un proceso retiene recursos mientras espera obtener otros que poseen terceros."},
        {"id":3,"name":"No Apropiación",   "key":"no_preemption",
         "desc":"Los recursos no pueden quitarse forzosamente; el proceso los libera voluntariamente."},
        {"id":4,"name":"Espera Circular",  "key":"circular_wait",
         "desc":"Existe una cadena cerrada P1→P2→…→Pn→P1 donde cada proceso espera al siguiente."},
    ]})

@app.get("/api/resources/types")
def resource_types():
    return jsonify({"types": [
        {"id":"apropiable",   "name":"Apropiable",   "icon":"💨","color":"#33ffaa",
         "desc":"Puede retirarse al proceso sin fallo.", "example":"CPU, RAM"},
        {"id":"no_apropiable","name":"No Apropiable","icon":"🔐","color":"#ff5577",
         "desc":"Solo el proceso lo libera voluntariamente.", "example":"Impresora, mutex"},
        {"id":"compartido",   "name":"Compartido",   "icon":"🌐","color":"#22aaff",
         "desc":"Varios procesos lo usan simultáneamente.", "example":"Archivos de solo lectura"},
        {"id":"exclusivo",    "name":"Exclusivo",    "icon":"⛔","color":"#ffcc22",
         "desc":"Solo un proceso a la vez; genera exclusión mutua.", "example":"Puerto serial"},
    ]})

@app.get("/health")
def health():
    return jsonify({"status":"ok","version":"1.0.0","uptime":time.time()})


# Helpers internos — presets

def _add_proc(color):
    global pid_counter
    p = Process(id=f"P{pid_counter}", color=color)
    pid_counter += 1; processes.append(p); return p

def _add_res():
    global rid_counter
    r = Resource(id=f"R{rid_counter}")
    rid_counter += 1; resources.append(r); return r

def _do_assign(pid, rid):
    p, r = _proc(pid), _res(rid)
    r.available -= 1; r.heldBy.append(pid)
    p.holds.append(rid); p.state = "running"

def _do_request(pid, rid):
    p = _proc(pid); p.waiting = rid; p.state = "blocked"

def _preset_simple():
    _add_proc("#2288ff"); _add_proc("#8855ff")
    _add_res();           _add_res()
    _do_assign("P1","R1"); _do_assign("P2","R2")
    _do_request("P1","R2"); _do_request("P2","R1")

def _preset_triangle():
    _add_proc("#2288ff"); _add_proc("#ffaa00"); _add_proc("#00ff88")
    _add_res();           _add_res();           _add_res()
    _do_assign("P1","R1"); _do_assign("P2","R2"); _do_assign("P3","R3")
    _do_request("P1","R2"); _do_request("P2","R3"); _do_request("P3","R1")

def _preset_safe():
    _add_proc("#2288ff"); _add_proc("#8855ff"); _add_proc("#00ff88")
    _add_res();           _add_res()
    _do_assign("P1","R1"); _do_assign("P2","R2"); _do_request("P1","R2")

def _preset_complex():
    _add_proc("#2288ff"); _add_proc("#8855ff"); _add_proc("#ffaa00"); _add_proc("#ff5577")
    _add_res();           _add_res();           _add_res()
    _do_assign("P1","R1"); _do_assign("P2","R2"); _do_assign("P3","R3")
    _do_request("P1","R2"); _do_request("P2","R3"); _do_request("P3","R1")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
