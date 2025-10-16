import sys
import os

# Añadir el directorio padre (workspace) al path antes de importar módulos locales
_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from datetime import timedelta
from config.database import engine, Base, SessionLocal
from models.agenda import Usuario, Movimiento, TipoMovi

# Intentar cargar configuración JWT desde el módulo config.jwt
try:
    import config.jwt as jwt_conf
except Exception:
    jwt_conf = None

app = Flask(__name__)

# Configuración JWT: preferir variable de entorno, luego config.jwt, luego valores por defecto
app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY",
    getattr(jwt_conf, "JWT_SECRET_KEY", None) if jwt_conf is not None else None,
)

if not app.config["JWT_SECRET_KEY"]:
    raise ValueError("❌ JWT_SECRET_KEY no está definida en las variables de entorno ni en config/jwt.py")

app.config["JWT_TOKEN_LOCATION"] = getattr(jwt_conf, "JWT_TOKEN_LOCATION", ["headers"]) if jwt_conf else ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = getattr(jwt_conf, "JWT_ACCESS_TOKEN_EXPIRES", timedelta(hours=1)) if jwt_conf else timedelta(hours=1)
app.config["JWT_HEADER_NAME"] = getattr(jwt_conf, "JWT_HEADER_NAME", "Authorization") if jwt_conf else "Authorization"
app.config["JWT_HEADER_TYPE"] = getattr(jwt_conf, "JWT_HEADER_TYPE", "Bearer") if jwt_conf else "Bearer"
# Si tu config/jwt.py ya usa ints (segundos) para JWT_ACCESS_TOKEN_EXPIRES, se respetará ese valor.

# Inicializar JWT
jwt = JWTManager(app)

# Crear tablas DESPUÉS de importar todos los modelos
Base.metadata.create_all(bind=engine)

@app.route('/')
def health_check():
    return jsonify({"status": "OK", "message": "AgendaAPI funcionando"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

