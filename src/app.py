import sys
import os
from flask import Flask


# Configurar el path del proyecto

# Permite que Python encuentre los módulos controllers, services, etc.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Importar base de datos y modelos

from config.database import engine
from models.agenda import Base

# Importar Blueprints y servicios

from controllers.usuarios_controller import usuario_bp
from controllers.tipos_controller import tipo_bp
from controllers.movimientos_controller import movimiento_bp
from services.services import init_default_tipos


# Crear tablas si no existen

def create_tables():
    Base.metadata.create_all(bind=engine)


# Crear la app Flask

app = Flask(__name__)
app.register_blueprint(usuario_bp)
app.register_blueprint(tipo_bp)
app.register_blueprint(movimiento_bp)


# Ejecutar la app

if __name__ == '__main__':
    create_tables()          #  Igual que en el ejemplo
    init_default_tipos()     # Inserta los tipos por defecto
    app.run(debug=True, host='0.0.0.0', port=5000)
