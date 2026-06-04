# ============================================================
# app.py — Punto de entrada del backend Flask (MVC)
# ============================================================
from flask import Flask, jsonify
from flask_cors import CORS
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from config import Config
from controllers.experiment_controller import experiment_api
from models.database import db

app = Flask(__name__)
app.config.from_object(Config)

# Configurar CORS para permitir peticiones desde cualquier origen (especialmente local file:// o localhost)
CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})

# Registrar Blueprints de Controladores
app.register_blueprint(experiment_api)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Ruta de verificación de estado y conexión a MySQL."""
    status = {"status": "ok", "mysql_connected": False}
    try:
        conn = db.get_connection()
        if conn.is_connected():
            status["mysql_connected"] = True
    except Exception as e:
        status["mysql_error"] = str(e)
    return jsonify(status), 200


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Cierra la conexión a la base de datos al finalizar cada request context."""
    db.close()


if __name__ == '__main__':
    print(f"Iniciando Servidor Flask en puerto {Config.PORT}...")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
