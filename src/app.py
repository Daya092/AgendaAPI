# src/app.py
import sys
import os
from flask import Flask

# -----------------------------
# Ajustar path para imports
# -----------------------------
# Agregar la raíz del proyecto al path para poder importar carpetas al mismo nivel que src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -----------------------------
# Importar Blueprints
# -----------------------------
from controllers.usuarios_controller import usuario_bp
from controllers.tipos_controller import tipo_bp
from controllers.movimientos_controller import movimiento_bp

# -----------------------------
# Importar base de datos y modelos
# -----------------------------
from Config.database import engine  # aunque no uses DB, puedes dejarlo para futuras conexiones
from Models.agenda import Base

# -----------------------------
# Crear tablas si no existen
# -----------------------------
def create_tables():
    if engine:  # solo si tienes engine configurado
        Base.metadata.create_all(bind=engine)

# -----------------------------
# Crear la app Flask
# -----------------------------
app = Flask(__name__)

# Registrar los Blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(tipo_bp)
app.register_blueprint(movimiento_bp)

# -----------------------------
# Ejecutar la app
# -----------------------------
if __name__ == '__main__':
    create_tables()
    # Usar puerto limpio y permitir Codespaces o env variable PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

