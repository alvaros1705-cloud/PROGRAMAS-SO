# ============================================================
# config.py — Configuración central del sistema
# ============================================================

class Config:
    """Configuración de la aplicación Flask."""

    # ---- Base de datos MySQL (XAMPP) ----
    DB_HOST     = 'localhost'
    DB_PORT     = 3306
    DB_USER     = 'root'
    DB_PASSWORD = ''          # XAMPP no tiene contraseña por defecto
    DB_NAME     = 'os_scheduler_sim'

    # ---- Flask ----
    DEBUG       = True
    PORT        = 5000
    SECRET_KEY  = 'os-scheduler-secret-2026'

    # ---- CORS (permite que el frontend llame al backend) ----
    CORS_ORIGINS = '*'        # En producción restringir al dominio del frontend
