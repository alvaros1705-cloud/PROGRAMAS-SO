# DeadlockOS — Sistema Operativo Educativo

Aplicación web educativa sobre el **bloqueo mutuo (deadlock)** y las **condiciones de Coffman**, construida con **FastAPI** (backend) y **HTML/CSS/JS** (frontend) con plantillas Jinja2.

---

## 📁 Estructura del proyecto

```
deadlockos/
├── main.py                  ← Backend FastAPI (API + rutas de páginas)
├── requirements.txt
├── templates/               ← Plantillas Jinja2 (HTML)
│   ├── base.html            ← Template base heredado por todos
│   ├── boot.html            ← Pantalla de inicio (boot sequence)
│   ├── login.html           ← Autenticación
│   ├── desktop.html         ← Escritorio principal
│   ├── intro.html           ← Módulo 1: Introducción
│   ├── recursos.html        ← Módulo 2: Tipos de recursos
│   ├── coffman.html         ← Módulo 3: Condiciones de Coffman
│   ├── simulador.html       ← Módulo 4: Simulador interactivo
│   └── resumen.html         ← Módulo 5: Resumen y prevención
└── static/
    ├── css/
    │   └── global.css       ← Estilos globales compartidos
    └── js/
        └── shared.js        ← JS compartido: API helper, notificaciones, reloj
```

---

## 🚀 Instalación y ejecución

### 1. Crear entorno virtual (recomendado)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el servidor
```bash
uvicorn main:app --reload --port 8000
```

### 4. Abrir en el navegador
```
http://localhost:8000
```

---

## 🔐 Credenciales de acceso

| Usuario      | Contraseña | Rol      |
|--------------|-----------|----------|
| `estudiante` | `1234`    | Estudiante |
| `guest`      | `1234`    | Invitado  |

---

## 🗺️ Flujo de navegación

```
/ (boot) → /login → /desktop → /intro → /recursos → /coffman → /simulador → /resumen
```

Cada módulo tiene botones **← Anterior** y **Siguiente →** en la parte inferior.  
La barra de navegación superior permite saltar entre módulos en cualquier momento.

---

## 🔌 API REST

| Método | Ruta               | Descripción                        |
|--------|--------------------|------------------------------------|
| POST   | `/api/auth`        | Autenticación                      |
| GET    | `/api/sim/state`   | Estado actual del simulador        |
| POST   | `/api/sim/action`  | Ejecutar acción en el simulador    |
| GET    | `/api/coffman/theory` | Definiciones de las 4 condiciones |
| GET    | `/api/resources/types` | Tipos de recursos              |
| GET    | `/health`          | Estado del servidor                |

### Ejemplo: cargar escenario predefinido
```bash
curl -X POST http://localhost:8000/api/sim/action \
  -H "Content-Type: application/json" \
  -d '{"action": "preset", "preset": "triangle"}'
```

### Ejemplo: asignar recurso a proceso
```bash
curl -X POST http://localhost:8000/api/sim/action \
  -H "Content-Type: application/json" \
  -d '{"action": "assign", "pid": "P1", "rid": "R1"}'
```

### Acciones disponibles en `/api/sim/action`

| `action`        | Parámetros adicionales | Descripción                    |
|-----------------|----------------------|--------------------------------|
| `add_process`   | —                    | Agrega un proceso              |
| `add_resource`  | —                    | Agrega un recurso              |
| `assign`        | `pid`, `rid`         | Asigna recurso a proceso       |
| `request`       | `pid`, `rid`         | Proceso solicita recurso       |
| `release`       | `pid`, `rid`         | Proceso libera recurso         |
| `reset`         | —                    | Reinicia el simulador          |
| `preset`        | `preset` (nombre)    | Carga escenario predefinido    |

### Escenarios predefinidos

| Nombre     | Descripción                              |
|-----------|------------------------------------------|
| `simple`   | Deadlock con 2 procesos y 2 recursos    |
| `triangle` | Deadlock triangular con 3 procesos      |
| `safe`     | Sistema sin deadlock (3 procesos)       |
| `complex`  | Deadlock complejo con 4 procesos        |

---

## 📚 Contenido educativo

| Módulo | Ruta          | Contenido                                      |
|--------|--------------|------------------------------------------------|
| 1      | `/intro`     | Conceptos base, ciclo de vida de procesos      |
| 2      | `/recursos`  | Tipos de recursos, tabla de asignación         |
| 3      | `/coffman`   | 4 condiciones, detector interactivo            |
| 4      | `/simulador` | Simulador con grafo RAG en tiempo real         |
| 5      | `/resumen`   | Síntesis y estrategias de prevención           |

---

## ⚙️ Tecnologías

- **Backend**: FastAPI + Uvicorn + Pydantic v2 + Jinja2
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **Fuentes**: Orbitron, Share Tech Mono, Exo 2 (Google Fonts)
- **Sin dependencias JS externas** — todo vanilla JS

---

## 📖 Referencia bibliográfica

> Coffman, E. G., Elphick, M., & Shoshani, A. (1971).  
> *System deadlocks*. ACM Computing Surveys, 3(2), 67–78.
