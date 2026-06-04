# ============================================================
# config.py — Configuración central del sistema
# ============================================================

import os

class Config:
    """Configuración de la aplicación Flask."""

    # ---- Base de datos local (SQLite) ----
    DB_PATH     = os.path.join(os.path.dirname(__file__), 'os_scheduler_sim.db')

    # ---- Flask ----
    DEBUG       = True
    PORT        = 5000
    SECRET_KEY  = 'os-scheduler-secret-2026'

    # ---- CORS (permite que el frontend llame al backend) ----
    CORS_ORIGINS = '*'        # En producción restringir al dominio del frontend
