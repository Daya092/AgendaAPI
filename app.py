import sys
import os
from flask import Flask
from services.services import init_default_tipos
# ------------------------------
# Configurar el path del proyecto
# ------------------------------
# Permite que Python encuentre los módulos controllers y services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ------------------------------
# Importar Blueprints
# ------------------------------
from controllers.usuarios_controller import usuario_bp
from controllers.tipos_controller import tipo_bp
from controllers.movimientos_controller import movimiento_bp

# ------------------------------
# Crear la app Flask
# ------------------------------
app = Flask(__name__)
init_default_tipos()
# ------------------------------
# Registrar los Blueprints
# ------------------------------
app.register_blueprint(usuario_bp)
app.register_blueprint(tipo_bp)
app.register_blueprint(movimiento_bp)

# ------------------------------
# Ejecutar la app
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
