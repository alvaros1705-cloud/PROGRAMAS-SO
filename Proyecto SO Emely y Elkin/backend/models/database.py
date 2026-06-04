# ============================================================
# models/database.py — Capa de conexión SQLite (Singleton)
# ============================================================
import sqlite3
import threading
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import Config


class Database:
    """
    Clase Singleton para gestionar la conexión a SQLite de forma
    segura entre hilos (thread-safe) y transparente.
    """
    _instance = None
    _local = threading.local()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def _conn(self):
        return getattr(self._local, 'conn', None)

    @_conn.setter
    def _conn(self, value):
        self._local.conn = value

    def get_connection(self):
        """Retorna una conexión activa para el hilo actual; la crea si no existe."""
        if self._conn is None:
            # Asegurar que el directorio de la base de datos exista
            db_dir = os.path.dirname(Config.DB_PATH)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            
            # Conectar a la base de datos SQLite
            self._conn = sqlite3.connect(Config.DB_PATH)
            self._conn.row_factory = sqlite3.Row
            
            # Habilitar soporte de claves foráneas
            self._conn.execute("PRAGMA foreign_keys = ON;")
            
            # Inicializar la base de datos si las tablas no existen
            self._init_db()
            
        return self._conn

    def _init_db(self):
        """Crea la estructura de tablas local si no existe."""
        cursor = self._conn.cursor()
        
        # Tabla de Experimentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL DEFAULT 'Experimento sin nombre',
                scenario TEXT NOT NULL,
                num_processes INTEGER NOT NULL,
                quantum INTEGER NOT NULL DEFAULT 2,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Tabla de Simulaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS simulations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id INTEGER NOT NULL,
                algorithm TEXT NOT NULL,
                avg_waiting_time REAL DEFAULT 0,
                avg_turnaround REAL DEFAULT 0,
                throughput REAL DEFAULT 0,
                cpu_utilization REAL DEFAULT 0,
                FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE
            );
        """)
        
        # Tabla de Procesos individuales de cada simulación
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS simulation_processes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id INTEGER NOT NULL,
                pid TEXT NOT NULL,
                arrival_time INTEGER NOT NULL,
                burst_time INTEGER NOT NULL,
                priority INTEGER NOT NULL DEFAULT 1,
                completion_time INTEGER DEFAULT 0,
                turnaround_time INTEGER DEFAULT 0,
                waiting_time INTEGER DEFAULT 0,
                FOREIGN KEY (simulation_id) REFERENCES simulations(id) ON DELETE CASCADE
            );
        """)
        
        # Índices para rendimiento
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_simulations_experiment ON simulations(experiment_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_processes_simulation ON simulation_processes(simulation_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_experiments_created ON experiments(created_at);")
        
        # Vista de comparación de experimentos
        cursor.execute("DROP VIEW IF EXISTS vw_experiment_comparison;")
        cursor.execute("""
            CREATE VIEW vw_experiment_comparison AS
            SELECT
                e.id AS experiment_id,
                e.name AS experiment_name,
                e.scenario,
                e.num_processes,
                e.quantum,
                e.created_at,
                s.algorithm,
                s.avg_waiting_time,
                s.avg_turnaround,
                s.throughput,
                s.cpu_utilization
            FROM experiments e
            JOIN simulations s ON s.experiment_id = e.id
            ORDER BY e.created_at DESC, s.algorithm;
        """)
        
        self._conn.commit()

    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        """
        Ejecuta una consulta SQL adaptando el marcador %s a ? de forma dinámica
        para compatibilidad con los modelos existentes.
        """
        query = query.replace('%s', '?')
        
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
                # Retornar como lista de diccionarios normales para evitar problemas de compatibilidad
                return [dict(row) for row in result]
            else:
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Error ejecutando consulta: {e}\nQuery: {query}")
        finally:
            cursor.close()

    def execute_many(self, query: str, data: list):
        """Ejecuta inserción múltiple en lote adaptando los marcadores a SQLite."""
        query = query.replace('%s', '?')
        
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.executemany(query, data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Error en execute_many: {e}")
        finally:
            cursor.close()

    def close(self):
        """Cierra la conexión a la base de datos del hilo actual si está abierta."""
        if self._conn is not None:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None


# Instancia global accesible desde los modelos
db = Database()
