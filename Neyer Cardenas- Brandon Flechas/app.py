# -*- coding: utf-8 -*-
"""
Simulador de Flujo de Entrada/Salida (E/S) en un Sistema Computacional
Desarrollado en Python con la biblioteca gráfica estándar Tkinter.
Cumple con todos los requisitos del usuario de forma modular, visual y interactiva.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# ---------------------------------------------------------------------------
# CONSTANTES DE DISEÑO Y PALETA DE COLORES (Tema Cyberpunk Oscuro Premium)
# ---------------------------------------------------------------------------
BG_DARK = "#0a0b10"         # Fondo general ultra oscuro
BG_PANEL = "#111420"        # Fondo de paneles secundarios
BG_CARD = "#171b2d"         # Fondo por defecto de las tarjetas
BORDER_COLOR = "#2a2f44"    # Color de borde por defecto
TEXT_COLOR = "#e2e8f0"      # Texto general claro
TEXT_MUTED = "#8892b0"      # Texto secundario/deshabilitado
LOG_BG = "#06070a"          # Fondo de consola estilo terminal
LOG_FG = "#38bdf8"          # Color de texto consola (Celeste brillante)

# Colores de acento específicos por componente (etapa)
COLOR_PERIFERICO = "#10b981"  # Verde Esmeralda
COLOR_CONTROLADOR = "#0ea5e9" # Celeste / Cielo
COLOR_CPU = "#f43f5e"         # Rojo / Rosa Neón
COLOR_OS = "#f97316"          # Naranja
COLOR_RAM = "#3b82f6"         # Azul Eléctrico
COLOR_CACHE = "#8b5cf6"       # Violeta
COLOR_DISCO = "#64748b"       # Gris Metalizado

# ---------------------------------------------------------------------------
# DATOS DE LAS ETAPAS DEL FLUJO (7 COMPONENTES)
# ---------------------------------------------------------------------------
STAGES = [
    {
        "id": "periferico",
        "name": "Periférico de Entrada",
        "subtitle": "Captura física del dato (Teclado/Mouse)",
        "desc": "El usuario realiza una acción física. El hardware del dispositivo la detecta y digitaliza en datos binarios (ej: una pulsación de tecla genera un código de barrido o scan code).",
        "tech": "• Matriz eléctrica: Al presionar una tecla, se cierra un circuito eléctrico.\n• Microcontrolador interno: Registra el cambio de voltaje y aplica filtrado de rebote (debouncing).\n• Scan code: Se produce el código de la tecla física (ej. 0x1E para la tecla 'A') en el registro de salida.",
        "color": COLOR_PERIFERICO,
        "emoji": "⌨️",
        "pos": (150, 100)
    },
    {
        "id": "controlador",
        "name": "Controlador de E/S",
        "subtitle": "Enlace entre hardware y CPU",
        "desc": "El chip controlador de E/S gestiona la comunicación con el periférico. Almacena temporalmente el dato en sus registros e interrumpe al procesador para notificar la entrada.",
        "tech": "• Línea de Interrupción (IRQ 1): Envía una señal eléctrica directa a la CPU.\n• Registro de Datos (I/O Port): Almacena temporalmente el scan code binario.\n• Direccionamiento: Permite al bus de datos leer el valor del controlador utilizando su puerto base.",
        "color": COLOR_CONTROLADOR,
        "emoji": "🔌",
        "pos": (400, 100)
    },
    {
        "id": "cpu",
        "name": "CPU (Procesamiento)",
        "subtitle": "Ejecución lógica del sistema",
        "desc": "La CPU detiene su trabajo actual al recibir la interrupción, lee el dato del bus físico, lo procesa mediante la Unidad Aritmético-Lógica (ALU) y ejecuta las instrucciones del driver.",
        "tech": "• Rutina ISR: La CPU guarda su contexto de registros y salta al código del manejador de interrupciones.\n• Registros del Procesador: Carga el byte de datos directamente en registros de velocidad ultra-alta (ej. EAX/RAX).\n• Unidad de Control: Decodifica el dato y ejecuta la instrucción de transferencia a la memoria virtual.",
        "color": COLOR_CPU,
        "emoji": "⚙️",
        "pos": (650, 100)
    },
    {
        "id": "os",
        "name": "Sistema Operativo",
        "subtitle": "Gestor de memoria y software",
        "desc": "El núcleo (Kernel) del SO recibe la interrupción, traduce el código de hardware a un carácter legible por el sistema (ej. ASCII) y gestiona la llamada de escritura (write syscall) del proceso activo.",
        "tech": "• Traducción de caracteres: El subsistema del SO convierte el código binario bruto en ASCII o UTF-8.\n• Cola de Entrada: Coloca el carácter en el búfer de entrada de la aplicación activa.\n• Syscall de Escritura: Ejecuta una instrucción privilegiada del sistema (ej. sys_write) para almacenar la información.",
        "color": COLOR_OS,
        "emoji": "🧠",
        "pos": (650, 270)
    },
    {
        "id": "ram",
        "name": "Memoria RAM",
        "subtitle": "Almacenamiento temporal activo",
        "desc": "El dato traducido se almacena de forma temporal y volátil en la memoria principal (RAM) dentro del espacio del búfer reservado antes de ser persistido.",
        "tech": "• Bus de Direcciones: Selecciona la fila y columna física de la celda de memoria mediante decodificadores.\n• Celdas DRAM: El dato se almacena como cargas eléctricas en condensadores dentro del silicio.\n• Volatilidad: La memoria requiere ciclos periódicos de refresco eléctrico (~64ms) para no perder los datos.",
        "color": COLOR_RAM,
        "emoji": "📟",
        "pos": (400, 270)
    },
    {
        "id": "cache",
        "name": "Memoria Caché",
        "subtitle": "Búfer de velocidad intermedia",
        "desc": "Antes de guardarse en el disco (que es extremadamente lento en comparación con la CPU), el dato pasa por las líneas de memoria caché del procesador para optimizar y agilizar futuras lecturas y escrituras.",
        "tech": "• Celdas SRAM: Basada en transistores biestables (flip-flops), hasta 100 veces más rápida que la DRAM.\n• Política Write-Back (Escritura Diferida): El dato se escribe en la caché primero, marcándose como 'sucio' (dirty bit). Posteriormente se sincroniza en bloque con el almacenamiento secundario.\n• Línea de Caché: Transfiere datos en bloques lógicos (comúnmente de 64 bytes).",
        "color": COLOR_CACHE,
        "emoji": "⚡",
        "pos": (150, 270)
    },
    {
        "id": "disco",
        "name": "Disco Duro / SSD",
        "subtitle": "Almacenamiento no volátil persistente",
        "desc": "El controlador de almacenamiento recibe el bloque de datos y lo escribe físicamente de forma permanente en el medio físico (unidad SSD o disco magnético HDD), completando el flujo.",
        "tech": "• Persistencia SSD (NAND Flash): Atrapa electrones en celdas de compuerta aislante (Floating Gate) que retienen la carga de forma permanente sin energía eléctrica.\n• Persistencia HDD (Magnético): Un cabezal electromecánico magnetiza partículas microscópicas en un disco giratorio.\n• Sistema de Archivos: El SO escribe metadatos (FAT/MFT/Inodes) indicando dónde se ubica el dato físico.",
        "color": COLOR_DISCO,
        "emoji": "💾",
        "pos": (400, 430)
    }
]

# ---------------------------------------------------------------------------
# CLASE PRINCIPAL DE LA APLICACIÓN
# ---------------------------------------------------------------------------
class IOSimulatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Flujo de Entrada/Salida (E/S) - Arquitectura de Computadores")
        self.geometry("1200x720")
        self.center_window(1200, 720)
        self.resizable(False, False)
        
        # Configurar colores generales de Tkinter
        self.configure(bg=BG_DARK)
        
        # Variables de control
        self.current_stage = -1      # -1 = Sin iniciar. 0 a 6 = Etapas
        self.is_animating = False    # Control de si la partícula está moviéndose
        self.animation_job = None    # Almacena el ID del temporizador de animación
        self.auto_step_job = None    # Almacena el ID de la transición automática
        
        self.mode_var = tk.StringVar(value="auto")   # "auto" o "manual"
        self.speed_var = tk.StringVar(value="normal") # "slow", "normal", "fast"
        
        # Parámetros de animación (modificados por velocidad)
        self.anim_steps = 30         # Número de fotogramas por transición
        self.anim_delay = 20         # Retraso en ms por fotograma
        self.step_delay = 1200       # Retraso en ms entre etapas en modo auto
        
        # Configurar el diseño de la UI
        self.setup_ui()
        self.reiniciar_simulacion()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    # ---------------------------------------------------------------------------
    # DISEÑO Y CONSTRUCCIÓN DE LA INTERFAZ GRÁFICA
    # ---------------------------------------------------------------------------
    def setup_ui(self):
        # 1. Panel Superior (Header)
        self.header_frame = tk.Frame(self, bg=BG_DARK, padx=20, pady=15)
        self.header_frame.pack(fill="x")
        
        title_label = tk.Label(
            self.header_frame,
            text="SIMULACIÓN DE FLUJO E/S",
            font=("Segoe UI", 20, "bold"),
            fg="#ffffff",
            bg=BG_DARK
        )
        title_label.pack(anchor="w")
        
        sub_label = tk.Label(
            self.header_frame,
            text="El viaje de un dato desde los impulsos físicos de hardware hasta el almacenamiento lógico persistente",
            font=("Segoe UI", 10),
            fg=TEXT_MUTED,
            bg=BG_DARK
        )
        sub_label.pack(anchor="w", pady=(2, 10))

        # Sección para el Dato Personalizado
        self.input_frame = tk.Frame(self.header_frame, bg=BG_DARK)
        self.input_frame.pack(anchor="w")
        
        input_lbl = tk.Label(
            self.input_frame,
            text="Escribe el dato a transferir:",
            font=("Segoe UI", 10, "bold"),
            fg=TEXT_COLOR,
            bg=BG_DARK
        )
        input_lbl.pack(side="left")
        
        self.data_entry = tk.Entry(
            self.input_frame,
            font=("Segoe UI", 10),
            bg=BG_CARD,
            fg="#ffffff",
            insertbackground="#ffffff",
            bd=1,
            relief="flat",
            width=20
        )
        self.data_entry.pack(side="left", padx=10)
        self.data_entry.insert(0, "DATOS_E/S")
        
        # Etiqueta indicadora del paso actual
        self.step_badge = tk.Label(
            self.header_frame,
            text="ETAPA: 0 / 7",
            font=("Segoe UI", 11, "bold"),
            fg="#00f0ff",
            bg="#1e1b4b",
            padx=15,
            pady=5,
            bd=1,
            relief="solid"
        )
        # Usar place para situar el badge arriba a la derecha de la ventana
        self.step_badge.place(relx=0.98, rely=0.1, anchor="ne")

        # 2. Área Central (Main Splitter)
        self.main_frame = tk.Frame(self, bg=BG_DARK, padx=20, pady=5)
        self.main_frame.pack(fill="both", expand=True)

        # 2a. Canvas de Simulación (Izquierda)
        self.canvas_frame = tk.Frame(self.main_frame, bg=BG_DARK)
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        
        # Canvas de Tkinter para dibujar componentes y buses
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=800,
            height=510,
            bg=BG_DARK,
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )
        self.canvas.pack(fill="both", expand=True)

        # 2b. Panel Lateral de Información y Log (Derecha)
        self.side_frame = tk.Frame(self.main_frame, bg=BG_DARK, width=340)
        self.side_frame.pack(side="right", fill="both", padx=(20, 0))
        self.side_frame.pack_propagate(False) # Mantener ancho fijo

        # Panel Educativo
        self.info_panel = tk.Frame(self.side_frame, bg=BG_PANEL, bd=1, relief="solid", highlightbackground=BORDER_COLOR, padx=15, pady=15)
        self.info_panel.pack(fill="both", expand=True)
        
        self.info_hdr = tk.Label(
            self.info_panel,
            text="DETALLES DE LA ETAPA",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_CONTROLADOR,
            bg=BG_PANEL
        )
        self.info_hdr.pack(anchor="w")
        
        self.info_title = tk.Label(
            self.info_panel,
            text="Esperando Simulación",
            font=("Segoe UI", 15, "bold"),
            fg="#ffffff",
            bg=BG_PANEL
        )
        self.info_title.pack(anchor="w", pady=(8, 2))

        self.info_subtitle = tk.Label(
            self.info_panel,
            text="Por favor, configure y presione iniciar.",
            font=("Segoe UI", 9, "italic"),
            fg=TEXT_MUTED,
            bg=BG_PANEL
        )
        self.info_subtitle.pack(anchor="w", pady=(0, 10))
        
        # Separador decorativo
        sep = tk.Frame(self.info_panel, height=1, bg=BORDER_COLOR)
        sep.pack(fill="x", pady=5)

        # Descripción
        self.info_desc = tk.Label(
            self.info_panel,
            text="Escribe un dato en la parte superior y presiona el botón 'Iniciar Simulación' para visualizar el recorrido a través de las capas de hardware y software del computador.",
            font=("Segoe UI", 10),
            fg=TEXT_COLOR,
            bg=BG_PANEL,
            wraplength=290,
            justify="left"
        )
        self.info_desc.pack(anchor="w", pady=10)

        # Caja de detalles técnicos de bajo nivel
        self.tech_box = tk.Frame(self.info_panel, bg=BG_DARK, bd=1, relief="solid", highlightbackground=BORDER_COLOR, padx=10, pady=10)
        self.tech_box.pack(fill="x", pady=(5, 10))
        
        tech_hdr = tk.Label(
            self.tech_box,
            text="BAJO EL CAPÓ (NIVEL ARQUITECTURA)",
            font=("Segoe UI", 8, "bold"),
            fg=COLOR_PERIFERICO,
            bg=BG_DARK
        )
        tech_hdr.pack(anchor="w", pady=(0, 4))
        
        self.tech_desc = tk.Label(
            self.tech_box,
            text="Los detalles mecánicos, físicos e instrucciones del sistema se cargarán en cada paso.",
            font=("Consolas", 8),
            fg=TEXT_MUTED,
            bg=BG_DARK,
            wraplength=270,
            justify="left"
        )
        self.tech_desc.pack(anchor="w")

        # 2c. Log estilo terminal (Abajo en el panel lateral)
        log_label = tk.Label(
            self.side_frame,
            text="REGISTRO DE EVENTOS (LOG)",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_OS,
            bg=BG_DARK
        )
        log_label.pack(anchor="w", pady=(15, 4))

        self.log_frame = tk.Frame(self.side_frame, bg=LOG_BG, bd=1, relief="solid", highlightbackground=BORDER_COLOR, height=120)
        self.log_frame.pack(fill="x")
        self.log_frame.pack_propagate(False)
        
        self.log_text = tk.Text(
            self.log_frame,
            bg=LOG_BG,
            fg=LOG_FG,
            font=("Consolas", 8),
            bd=0,
            padx=8,
            pady=8,
            state="disabled",
            wrap="word"
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar para la terminal de log
        scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # 3. Panel Inferior (Controles)
        self.control_frame = tk.Frame(self, bg=BG_PANEL, bd=1, relief="solid", highlightbackground=BORDER_COLOR, padx=20, pady=15)
        self.control_frame.pack(fill="x", side="bottom")

        # Sección Botones (Izquierda)
        self.btn_frame = tk.Frame(self.control_frame, bg=BG_PANEL)
        self.btn_frame.pack(side="left")

        # Configurar botones estilizados con eventos hover
        self.btn_play = tk.Button(
            self.btn_frame,
            text="Iniciar Simulación",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            relief="flat",
            command=self.iniciar_simulacion
        )
        self.btn_play.pack(side="left", padx=(0, 10))
        self.bind_btn_hover(self.btn_play, "#1e1b4b", "#00f0ff", "#00f0ff", "#0d0d11")

        self.btn_next = tk.Button(
            self.btn_frame,
            text="Siguiente Paso",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            relief="flat",
            command=self.siguiente_paso
        )
        self.btn_next.pack(side="left", padx=(0, 10))
        self.bind_btn_hover(self.btn_next, "#2e1065", "#c084fc", "#c084fc", "#0d0d11")

        self.btn_reset = tk.Button(
            self.btn_frame,
            text="Reiniciar",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            relief="flat",
            command=self.reiniciar_simulacion
        )
        self.btn_reset.pack(side="left")
        self.bind_btn_hover(self.btn_reset, "#1c1917", "#d6d3d1", "#44403c", "#ffffff")

        # Selectores de Modo (Centro-Izquierda)
        self.mode_frame = tk.Frame(self.control_frame, bg=BG_PANEL, padx=15)
        self.mode_frame.pack(side="left", padx=10)
        
        mode_lbl = tk.Label(self.mode_frame, text="MODO DE FLUJO", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_PANEL)
        mode_lbl.pack(anchor="w", pady=(0, 2))
        
        # Radio buttons personalizados usando ttk/tk con estilos
        self.rb_auto = tk.Radiobutton(
            self.mode_frame, text="Automático", variable=self.mode_var, value="auto",
            font=("Segoe UI", 9), bg=BG_PANEL, fg=TEXT_COLOR, selectcolor=BG_DARK,
            activebackground=BG_PANEL, activeforeground=TEXT_COLOR, command=self.on_mode_change
        )
        self.rb_auto.pack(side="left", padx=(0, 10))
        
        self.rb_manual = tk.Radiobutton(
            self.mode_frame, text="Paso a Paso", variable=self.mode_var, value="manual",
            font=("Segoe UI", 9), bg=BG_PANEL, fg=TEXT_COLOR, selectcolor=BG_DARK,
            activebackground=BG_PANEL, activeforeground=TEXT_COLOR, command=self.on_mode_change
        )
        self.rb_manual.pack(side="left")

        # Selectores de Velocidad (Centro-Derecha)
        self.speed_frame = tk.Frame(self.control_frame, bg=BG_PANEL, padx=15)
        self.speed_frame.pack(side="left", padx=10)
        
        speed_lbl = tk.Label(self.speed_frame, text="VELOCIDAD (AUTO)", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_PANEL)
        speed_lbl.pack(anchor="w", pady=(0, 2))
        
        self.rb_slow = tk.Radiobutton(
            self.speed_frame, text="Lento", variable=self.speed_var, value="slow",
            font=("Segoe UI", 9), bg=BG_PANEL, fg=TEXT_COLOR, selectcolor=BG_DARK,
            activebackground=BG_PANEL, activeforeground=TEXT_COLOR, command=self.update_speed_settings
        )
        self.rb_slow.pack(side="left", padx=(0, 10))
        
        self.rb_normal = tk.Radiobutton(
            self.speed_frame, text="Normal", variable=self.speed_var, value="normal",
            font=("Segoe UI", 9), bg=BG_PANEL, fg=TEXT_COLOR, selectcolor=BG_DARK,
            activebackground=BG_PANEL, activeforeground=TEXT_COLOR, command=self.update_speed_settings
        )
        self.rb_normal.pack(side="left", padx=(0, 10))
        
        self.rb_fast = tk.Radiobutton(
            self.speed_frame, text="Rápido", variable=self.speed_var, value="fast",
            font=("Segoe UI", 9), bg=BG_PANEL, fg=TEXT_COLOR, selectcolor=BG_DARK,
            activebackground=BG_PANEL, activeforeground=TEXT_COLOR, command=self.update_speed_settings
        )
        self.rb_fast.pack(side="left")

        # Barra de Progreso Personalizada (Derecha)
        self.progress_frame = tk.Frame(self.control_frame, bg=BG_PANEL)
        self.progress_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))
        
        self.progress_lbl = tk.Label(
            self.progress_frame,
            text="PROGRESO DE LA OPERACIÓN: 0%",
            font=("Segoe UI", 8, "bold"),
            fg=TEXT_MUTED,
            bg=BG_PANEL
        )
        self.progress_lbl.pack(anchor="w", pady=(0, 2))
        
        self.progress_canvas = tk.Canvas(
            self.progress_frame,
            height=20,
            bg=BG_DARK,
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )
        self.progress_canvas.pack(fill="x", expand=True)

    # ---------------------------------------------------------------------------
    # FUNCIONES AUXILIARES DE ESTILOS (Hover y Estados)
    # ---------------------------------------------------------------------------
    def bind_btn_hover(self, btn, normal_bg, normal_fg, hover_bg, hover_fg):
        btn.config(bg=normal_bg, fg=normal_fg)
        def on_enter(e):
            if btn["state"] == "normal":
                btn.config(bg=hover_bg, fg=hover_fg)
        def on_leave(e):
            if btn["state"] == "normal":
                btn.config(bg=normal_bg, fg=normal_fg)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        # Guardar para usarlos al habilitar/deshabilitar
        btn.normal_bg = normal_bg
        btn.normal_fg = normal_fg
        btn.hover_bg = hover_bg
        btn.hover_fg = hover_fg

    def set_custom_btn_state(self, btn, state):
        if state == "disabled":
            btn.config(state="disabled", bg="#0e0f14", fg="#3a3c48")
        else:
            btn.config(state="normal", bg=btn.normal_bg, fg=btn.normal_fg)

    def write_log(self, text):
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"[{time_str}] {text}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    # ---------------------------------------------------------------------------
    # DIBUJAR COMPONENTES EN EL CANVAS
    # ---------------------------------------------------------------------------
    def create_rounded_rect(self, canvas, x1, y1, x2, y2, r, fill, outline, width, tag=""):
        # Fills
        canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, fill=fill, outline=fill, style="pieslice", tags=tag)
        canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, fill=fill, outline=fill, style="pieslice", tags=tag)
        canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, fill=fill, outline=fill, style="pieslice", tags=tag)
        canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, fill=fill, outline=fill, style="pieslice", tags=tag)
        canvas.create_rectangle(x1+r, y1, x2-r, y2, fill=fill, outline=fill, tags=tag)
        canvas.create_rectangle(x1, y1+r, x2, y2-r, fill=fill, outline=fill, tags=tag)
        
        # Outlines
        if width > 0:
            canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, outline=outline, width=width, style="arc", tags=tag)
            canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, outline=outline, width=width, style="arc", tags=tag)
            canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, outline=outline, width=width, style="arc", tags=tag)
            canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, outline=outline, width=width, style="arc", tags=tag)
            canvas.create_line(x1+r, y1, x2-r, y1, fill=outline, width=width, tags=tag)
            canvas.create_line(x2, y1+r, x2, y2-r, fill=outline, width=width, tags=tag)
            canvas.create_line(x1+r, y2, x2-r, y2, fill=outline, width=width, tags=tag)
            canvas.create_line(x1, y1+r, x1, y2-r, fill=outline, width=width, tags=tag)

    def draw_component_card(self, stage_idx):
        stage = STAGES[stage_idx]
        x, y = stage["pos"]
        w, h = 160, 80
        r = 12
        x1, y1 = x - w/2, y - h/2
        x2, y2 = x + w/2, y + h/2
        
        is_active = (self.current_stage == stage_idx)
        
        # Definir colores según estado activo
        if is_active:
            bg_color = "#1d2338"
            outline_color = stage["color"]
            outline_width = 3
            title_color = "#ffffff"
            sub_color = TEXT_COLOR
        else:
            bg_color = BG_CARD
            outline_color = BORDER_COLOR
            outline_width = 1
            title_color = TEXT_COLOR
            sub_color = TEXT_MUTED

        tag = f"comp_{stage['id']}"
        self.create_rounded_rect(self.canvas, x1, y1, x2, y2, r, fill=bg_color, outline=outline_color, width=outline_width, tag=tag)

        # Dibujar Emoji
        self.canvas.create_text(
            x - 45, y,
            text=stage["emoji"],
            font=("Segoe UI", 22),
            anchor="center",
            tags=tag
        )

        # Dibujar Título del Componente
        # Si tiene nombre largo como "Controlador de E/S", podemos abreviarlo un poco
        card_name = stage["name"]
        if "Controlador" in card_name:
            card_name = "Controlador E/S"
        elif "Sistema" in card_name:
            card_name = "Sistema Op."
        elif "Caché" in card_name:
            card_name = "Memoria Caché"
            
        self.canvas.create_text(
            x + 12, y - 12,
            text=card_name,
            font=("Segoe UI", 9, "bold"),
            fill=title_color,
            anchor="w",
            tags=tag
        )

        # Dibujar Subtítulo descriptivo corto
        sub_text = "Físico"
        if stage_idx == 1: sub_text = "Hardware"
        elif stage_idx == 2: sub_text = "Procesador"
        elif stage_idx == 3: sub_text = "Software Kernel"
        elif stage_idx == 4: sub_text = "RAM Temporal"
        elif stage_idx == 5: sub_text = "SRAM Caché"
        elif stage_idx == 6: sub_text = "Persistente"
            
        self.canvas.create_text(
            x + 12, y + 10,
            text=sub_text,
            font=("Segoe UI", 8),
            fill=sub_color,
            anchor="w",
            tags=tag
        )
        
        # Etiqueta de paso (ej. [1], [2]...) en una esquina
        self.canvas.create_text(
            x2 - 12, y1 + 12,
            text=f"P{stage_idx + 1}",
            font=("Segoe UI", 8, "bold"),
            fill=stage["color"] if is_active else TEXT_MUTED,
            anchor="center",
            tags=tag
        )

    def redraw_canvas(self):
        # Limpiar el canvas
        self.canvas.delete("all")
        
        # 1. Dibujar líneas de bus (Conexiones)
        self.draw_buses()
        
        # 2. Dibujar tarjetas de componentes
        for idx in range(len(STAGES)):
            self.draw_component_card(idx)
            
        # 3. Dibujar la partícula del dato si está activa
        if self.current_stage >= 0:
            self.draw_data_particle()

    def draw_buses(self):
        # Definir los trayectos de bus entre bloques
        bus_segments = [
            # De 0 -> 1: Periférico a Controlador
            {"start": (230, 100), "end": [(320, 100)], "stage": 0},
            # De 1 -> 2: Controlador a CPU
            {"start": (480, 100), "end": [(570, 100)], "stage": 1},
            # De 2 -> 3: CPU a SO
            {"start": (650, 140), "end": [(650, 230)], "stage": 2},
            # De 3 -> 4: SO a RAM
            {"start": (570, 270), "end": [(480, 270)], "stage": 3},
            # De 4 -> 5: RAM a Caché
            {"start": (320, 270), "end": [(230, 270)], "stage": 4},
            # De 5 -> 6: Caché a Disco (Ortogonal)
            {"start": (150, 310), "end": [(150, 430), (320, 430)], "stage": 5}
        ]
        
        for seg in bus_segments:
            # Reconstruir lista de coordenadas del trayecto
            coords = [seg["start"][0], seg["start"][1]]
            for pt in seg["end"]:
                coords.append(pt[0])
                coords.append(pt[1])
                
            # Verificar si este bus es el canal de transición activo actual
            # La transición i se activa si la animación actual corresponde al segmento de origen i
            is_active_transition = (self.is_animating and self.current_stage == seg["stage"])
            
            # Bus de fondo (ancho y apagado)
            self.canvas.create_line(
                *coords,
                fill="#161b2d",
                width=8,
                arrow=tk.LAST,
                arrowshape=(12, 14, 5),
                tags="bus"
            )
            
            # Línea de control de sincronización secundaria (borde del bus)
            self.canvas.create_line(
                *coords,
                fill=BORDER_COLOR,
                width=10,
                arrow=tk.LAST,
                arrowshape=(13, 16, 6),
                tags="bus_bg"
            )
            self.canvas.tag_lower("bus_bg")
            self.canvas.tag_lower("bus")
            
            # Si el bus está transmitiendo la señal, dibujar el canal de neón activo
            if is_active_transition:
                active_color = STAGES[seg["stage"] + 1]["color"]
                self.canvas.create_line(
                    *coords,
                    fill=active_color,
                    width=4,
                    arrow=tk.LAST,
                    arrowshape=(10, 12, 4),
                    tags="bus_active"
                )

    def draw_data_particle(self):
        # Dibujar la cápsula del dato en (self.data_x, self.data_y)
        x, y = self.data_x, self.data_y
        
        # Calcular el tamaño del pill basado en el texto
        txt_len = len(self.data_text)
        w = max(55, txt_len * 7 + 12)
        h = 24
        r = 8
        x1, y1 = x - w/2, y - h/2
        x2, y2 = x + w/2, y + h/2
        
        # Color del dato depende del componente origen o destino
        # Si está animando de i a i+1, toma el color del componente destino (etapa actual + 1)
        if self.is_animating:
            active_color = STAGES[self.current_stage + 1]["color"]
        else:
            active_color = STAGES[self.current_stage]["color"]
            
        # Dibujar sombra/resplandor del dato
        self.canvas.create_oval(x-w/2-3, y-h/2-3, x+w/2+3, y+h/2+3, fill="", outline=active_color, width=1, tags="data_glow")
        
        # Dibujar cápsula
        self.create_rounded_rect(self.canvas, x1, y1, x2, y2, r, fill="#ffffff", outline=active_color, width=2, tag="data_capsule")
        
        # Texto del dato inside the capsule
        self.canvas.create_text(
            x, y,
            text=self.data_text,
            fill="#0a0b10",
            font=("Segoe UI", 8, "bold"),
            anchor="center",
            tags="data_text"
        )

    # ---------------------------------------------------------------------------
    # GESTIÓN Y CÁLCULO DE LA ANIMACIÓN
    # ---------------------------------------------------------------------------
    def interpolate_path(self, start_pt, dest_points, num_steps):
        # Une el punto de partida con el/los de destino formando segmentos de recta continuos
        points = [start_pt] + dest_points
        
        # Calcular longitudes de cada segmento y la longitud total del camino
        lengths = []
        total_len = 0.0
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            lengths.append(dist)
            total_len += dist
            
        if total_len == 0:
            return [points[0]] * num_steps
            
        path_coords = []
        for step in range(num_steps):
            t = step / (num_steps - 1)
            target_dist = t * total_len
            
            # Encontrar el segmento correspondiente a la distancia actual
            accum_dist = 0.0
            seg_idx = 0
            for idx, dist in enumerate(lengths):
                if accum_dist + dist >= target_dist:
                    seg_idx = idx
                    break
                accum_dist += dist
            else:
                seg_idx = len(lengths) - 1
                
            seg_t = 0.0
            if lengths[seg_idx] > 0:
                seg_t = (target_dist - accum_dist) / lengths[seg_idx]
                
            p1 = points[seg_idx]
            p2 = points[seg_idx+1]
            x = p1[0] + (p2[0] - p1[0]) * seg_t
            y = p1[1] + (p2[1] - p1[1]) * seg_t
            path_coords.append((x, y))
            
        return path_coords

    def animate_step(self, coords_list, frame_idx, on_finished_callback):
        if frame_idx < len(coords_list):
            self.data_x, self.data_y = coords_list[frame_idx]
            self.redraw_canvas()
            # Programar el siguiente fotograma
            self.animation_job = self.after(self.anim_delay, self.animate_step, coords_list, frame_idx + 1, on_finished_callback)
        else:
            self.is_animating = False
            self.animation_job = None
            on_finished_callback()

    # ---------------------------------------------------------------------------
    # MAQUINA DE ESTADOS Y LÓGICA DE SIMULACIÓN
    # ---------------------------------------------------------------------------
    def update_speed_settings(self):
        # Modificar las velocidades según los radio buttons
        speed = self.speed_var.get()
        if speed == "slow":
            self.anim_steps = 45
            self.anim_delay = 30
            self.step_delay = 2000
        elif speed == "normal":
            self.anim_steps = 30
            self.anim_delay = 20
            self.step_delay = 1200
        else: # "fast"
            self.anim_steps = 15
            self.anim_delay = 10
            self.step_delay = 500

    def on_mode_change(self):
        mode = self.mode_var.get()
        if mode == "manual":
            self.btn_play.config(text="Iniciar (Paso a Paso)")
            # Habilitar el botón de siguiente paso solo si la simulación ya corre y no está animando
            if self.current_stage >= 0 and self.current_stage < 6 and not self.is_animating:
                self.set_custom_btn_state(self.btn_next, "normal")
            else:
                self.set_custom_btn_state(self.btn_next, "disabled")
        else: # "auto"
            self.btn_play.config(text="Iniciar Simulación")
            self.set_custom_btn_state(self.btn_next, "disabled")

    def highlight_stage(self, stage_idx):
        stage = STAGES[stage_idx]
        
        # 1. Actualizar textos descriptivos del panel lateral
        self.info_title.config(text=stage["name"], fg=stage["color"])
        self.info_subtitle.config(text=stage["subtitle"])
        self.info_desc.config(text=stage["desc"])
        self.tech_desc.config(text=stage["tech"])
        
        # Actualizar color del encabezado del cuadro técnico
        # Buscar el widget en la jerarquía para cambiarle el color
        for child in self.tech_box.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") == "BAJO EL CAPÓ (NIVEL ARQUITECTURA)":
                child.config(fg=stage["color"])
                break
                
        # 2. Actualizar el log de la consola
        self.write_log(f"[{stage['name']}] - {stage['subtitle']}")
        
        # 3. Actualizar la insignia de paso en la cabecera
        self.step_badge.config(text=f"ETAPA: {stage_idx + 1} / 7", fg=stage["color"])
        
        # 4. Actualizar barra de progreso
        progress_pct = int(((stage_idx + 1) / 7) * 100)
        self.draw_progress_bar(progress_pct)

    def draw_progress_bar(self, percentage):
        self.progress_lbl.config(text=f"PROGRESO DE LA OPERACIÓN: {percentage}%")
        self.progress_canvas.delete("all")
        width = self.progress_canvas.winfo_width()
        if width <= 1:
            width = 250  # Ancho por defecto al inicio
        height = 20
        
        # Fondo vacío
        self.progress_canvas.create_rectangle(0, 0, width, height, fill=BG_DARK, outline="")
        # Relleno del progreso con color de etapa actual o celeste
        fill_color = STAGES[self.current_stage]["color"] if self.current_stage >= 0 else COLOR_CONTROLADOR
        fill_width = int((percentage / 100) * width)
        
        if fill_width > 0:
            self.progress_canvas.create_rectangle(0, 0, fill_width, height, fill=fill_color, outline="")

    # ---------------------------------------------------------------------------
    # OPERACIONES DEL CONTROL DE SIMULACIÓN
    # ---------------------------------------------------------------------------
    def iniciar_simulacion(self):
        # Validar la entrada
        data_input = self.data_entry.get().strip()
        if not data_input:
            data_input = "DATOS_E/S"
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, data_input)
            
        self.data_text = data_input
        self.current_stage = 0
        self.is_animating = False
        
        # Bloquear caja de entrada y selectores para evitar cambios a mitad de ejecución
        self.data_entry.config(state="disabled")
        self.rb_auto.config(state="disabled")
        self.rb_manual.config(state="disabled")
        self.rb_slow.config(state="disabled")
        self.rb_normal.config(state="disabled")
        self.rb_fast.config(state="disabled")
        
        # Cambiar estados de botones
        self.set_custom_btn_state(self.btn_play, "disabled")
        self.set_custom_btn_state(self.btn_reset, "normal")
        
        # Registrar arranque en el log
        self.write_log(f"--- SIMULACIÓN INICIADA ---")
        self.write_log(f"Cargando dato de entrada: '{self.data_text}'")
        
        # Posición inicial de la partícula: en el centro del Periférico (primer bloque)
        self.data_x, self.data_y = STAGES[0]["pos"]
        
        # Resaltar la primera etapa
        self.highlight_stage(0)
        self.redraw_canvas()
        
        # Iniciar ciclo de flujo según el modo seleccionado
        if self.mode_var.get() == "auto":
            self.set_custom_btn_state(self.btn_next, "disabled")
            # Programar el avance automático tras una pausa educativa en el componente inicial
            self.auto_step_job = self.after(self.step_delay, self.auto_advance)
        else:
            # Modo manual: habilitar botón para que el usuario avance cuando quiera
            self.set_custom_btn_state(self.btn_next, "normal")

    def auto_advance(self):
        # Avanza automáticamente si no está en la etapa final
        if self.current_stage < 6:
            self.siguiente_paso()
            
    def siguiente_paso(self):
        # Protección contra doble clic o avances rápidos en animación
        if self.is_animating or self.current_stage < 0 or self.current_stage >= 6:
            return
            
        self.is_animating = True
        self.set_custom_btn_state(self.btn_next, "disabled")
        
        # Etapa origen actual
        curr_idx = self.current_stage
        next_idx = curr_idx + 1
        
        # Configurar la ruta física
        start_pos = STAGES[curr_idx]["pos"]
        dest_pos = STAGES[next_idx]["pos"]
        
        # Definir la trayectoria de movimiento
        # Por defecto es una línea recta entre las posiciones de las tarjetas
        path_pts = [dest_pos]
        
        # El trayecto del paso 5 al 6 (Caché a Disco) es ortogonal para no cruzar en diagonal
        if curr_idx == 5:
            # Va de (150, 270) -> (150, 430) -> (400, 430)
            path_pts = [(150, 430), (400, 430)]
            
        # Interpolación de coordenadas para animación suave
        self.update_speed_settings()
        coords = self.interpolate_path(start_pos, path_pts, self.anim_steps)
        
        # Registrar el inicio del viaje a través del bus físico
        bus_desc = "Bus del Sistema"
        if curr_idx == 0: bus_desc = "Puerto/Bus de E/S"
        elif curr_idx == 1: bus_desc = "Línea de interrupción IRQ"
        elif curr_idx == 2: bus_desc = "Canales del Chipset / Bus de Datos"
        elif curr_idx == 3: bus_desc = "Bus del Sistema / Bus de Direcciones"
        elif curr_idx == 4: bus_desc = "Bus de Memoria Interno (Caché L1/L2/L3)"
        elif curr_idx == 5: bus_desc = "Controladora SATA/NVMe PCIe"
            
        self.write_log(f"Transmitiendo dato '{self.data_text}' vía {bus_desc}...")
        
        # Callback invocado cuando la animación del movimiento concluye
        def al_finalizar_movimiento():
            self.current_stage = next_idx
            self.data_x, self.data_y = dest_pos # Ubicar exactamente en el destino
            self.highlight_stage(next_idx)
            self.redraw_canvas()
            
            # Verificar si alcanzamos el disco/SSD (final de simulación)
            if self.current_stage == 6:
                self.completar_simulacion()
            else:
                # Si el modo es auto, seguir avanzando automáticamente
                if self.mode_var.get() == "auto":
                    self.auto_step_job = self.after(self.step_delay, self.auto_advance)
                else:
                    # Si es modo manual, reactivar el botón de paso para el usuario
                    self.set_custom_btn_state(self.btn_next, "normal")
                    
        # Iniciar hilo de animación recursiva
        self.animate_step(coords, 0, al_finalizar_movimiento)

    def completar_simulacion(self):
        # Fin de simulación exitoso
        self.write_log(f"¡DATO GUARDADO CON PERSISTENCIA!")
        self.write_log(f"Proceso concluido: El dato ha sido almacenado permanentemente en el Disco/SSD.")
        self.write_log(f"--- SIMULACIÓN FINALIZADA ---")
        
        # Mostrar cartel informativo con diseño agradable
        messagebox.showinfo(
            "Simulación Completada",
            f"El dato '{self.data_text}' se ha procesado y escrito exitosamente en el Disco Duro / SSD de forma no volátil.\n\n"
            "El flujo completo ha sido representado a través de las 7 etapas lógicas y de hardware de la computadora."
        )
        
        # Asegurar barra al 100%
        self.draw_progress_bar(100)

    def reiniciar_simulacion(self):
        # Cancelar tareas pendientes de after()
        if self.animation_job:
            self.after_cancel(self.animation_job)
            self.animation_job = None
        if self.auto_step_job:
            self.after_cancel(self.auto_step_job)
            self.auto_step_job = None
            
        self.current_stage = -1
        self.is_animating = False
        
        # Habilitar los controles de configuración
        self.data_entry.config(state="normal")
        self.rb_auto.config(state="normal")
        self.rb_manual.config(state="normal")
        self.rb_slow.config(state="normal")
        self.rb_normal.config(state="normal")
        self.rb_fast.config(state="normal")
        
        # Restablecer botones
        self.set_custom_btn_state(self.btn_play, "normal")
        self.set_custom_btn_state(self.btn_next, "disabled")
        self.set_custom_btn_state(self.btn_reset, "disabled")
        
        # Limpiar textos de información
        self.info_title.config(text="Esperando Simulación", fg="#ffffff")
        self.info_subtitle.config(text="Configure y pulse 'Iniciar Simulación'")
        self.info_desc.config(
            text="Escribe un dato en la parte superior y presiona el botón 'Iniciar Simulación' para visualizar el recorrido paso a paso a través de las capas de hardware y software del ordenador."
        )
        self.tech_desc.config(text="Los detalles mecánicos, físicos e instrucciones del sistema se cargarán en cada paso.")
        
        # Reiniciar cabecera del cuadro de tecnología a color por defecto
        for child in self.tech_box.winfo_children():
            if isinstance(child, tk.Label) and child.cget("text") == "BAJO EL CAPÓ (NIVEL ARQUITECTURA)":
                child.config(fg=COLOR_PERIFERICO)
                break
                
        # Reiniciar el badge superior y progreso
        self.step_badge.config(text="ETAPA: 0 / 7", fg="#00f0ff")
        self.progress_lbl.config(text="PROGRESO DE LA OPERACIÓN: 0%")
        
        # Limpiar terminal de log
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state="disabled")
        
        # Redibujar la barra de progreso vacía
        self.draw_progress_bar(0)
        
        # Re-trazar el canvas a su estado inicial limpio
        self.redraw_canvas()


# ---------------------------------------------------------------------------
# ARRANQUE DE LA APLICACIÓN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = IOSimulatorApp()
    
    # Manejo de redimensionado inicial para la barra de progreso
    app.update()
    app.draw_progress_bar(0)
    
    # Ejecutar bucle principal de interfaz
    app.mainloop()
