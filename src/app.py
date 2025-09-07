from flask import Flask
import sys
import os

# Asegurar que Python vea las carpetas del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Importar Blueprints
from Controllers.usuarios_controller import usuario_bp
from Controllers.tipos_controller import tipo_bp
from Controllers.movimientos_controller import movimiento_bp

# Importar base de datos y modelos
from Config.database import engine
from Models.agenda import Base

# Crear tablas si no existen
def create_tables():
    Base.metadata.create_all(bind=engine)

# Crear la app Flask
app = Flask(__name__)

# Registrar los Blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(tipo_bp)
app.register_blueprint(movimiento_bp)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0')
