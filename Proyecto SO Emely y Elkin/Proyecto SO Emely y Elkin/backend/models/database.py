# ============================================================
# models/database.py — Capa de conexión MySQL (Singleton)
# ============================================================
import mysql.connector
from mysql.connector import Error
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import Config


class Database:
    """
    Clase Singleton para gestionar la conexión a MySQL.
    Garantiza una única instancia de conexión durante la vida
    de la aplicación.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def get_connection(self):
        """Retorna una conexión activa; la crea si no existe o fue cerrada."""
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(
                    host=Config.DB_HOST,
                    port=Config.DB_PORT,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME,
                    autocommit=False,
                    charset='utf8mb4'
                )
        except Error as e:
            raise ConnectionError(f"No se pudo conectar a MySQL: {e}")
        return self._connection

    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        """
        Ejecuta una consulta SQL.
        - Si fetch=True retorna los resultados (SELECT).
        - Si fetch=False ejecuta INSERT/UPDATE/DELETE y retorna lastrowid.
        """
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                conn.commit()
                return cursor.lastrowid
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Error ejecutando consulta: {e}\nQuery: {query}")
        finally:
            cursor.close()

    def execute_many(self, query: str, data: list):
        """Ejecuta INSERT múltiple (executemany) — para insertar lista de procesos."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.executemany(query, data)
            conn.commit()
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Error en execute_many: {e}")
        finally:
            cursor.close()

    def close(self):
        """Cierra la conexión si está abierta."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None


# Instancia global accesible desde los modelos
db = Database()
