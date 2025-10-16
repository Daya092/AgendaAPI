import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError
from services.services import (
    get_all_usuarios,
    get_usuario_by_id,
    create_usuario,
    update_usuario,
    delete_usuario,
    authenticate_user,
)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

usuario_bp = Blueprint("usuario_bp", __name__, url_prefix="/api")

# --- Manejador de errores JWT ---
def register_jwt_error_handlers(app):
    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth_error(e):
        logger.warning("Intento de acceso sin autenticación JWT")
        return jsonify({
            "error": "No autenticado. Debe enviar un token JWT válido en el header Authorization."
        }), 401


# ------------------ LOGIN ------------------
@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("name") or data.get("username")
    password = data.get("password")

    if not username or not password:
        logger.warning("Login fallido: usuario o contraseña no proporcionados")
        return jsonify({"error": "El nombre de usuario y la contraseña son obligatorios"}), 400

    user = authenticate_user(username, password)
    if not user:
        logger.warning(f"Login fallido para usuario: {username}")
        return jsonify({"error": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=str(user.id))
    logger.info(f"Usuario autenticado: {username}")
    return jsonify({
        "access_token": access_token,
        "user": {"id": user.id, "name": user.name, "correo": user.correo}
    }), 200


# ------------------ CRUD USUARIOS ------------------
@usuario_bp.route("/usuarios", methods=["GET"])
@jwt_required()
def get_usuarios():
    users = get_all_usuarios()
    logger.info("Consulta de todos los usuarios")
    return jsonify(users), 200


@usuario_bp.route("/usuarios/<int:usuario_id>", methods=["GET"])
@jwt_required()
def get_usuario(usuario_id):
    usuario = get_usuario_by_id(usuario_id)
    if usuario is None:
        logger.warning(f"Usuario no encontrado: {usuario_id}")
        return jsonify({"error": "Usuario no encontrado"}), 404
    logger.info(f"Consulta de usuario por ID: {usuario_id}")
    return jsonify(usuario), 200


@usuario_bp.route("/usuarios", methods=["POST"])
def create_usuario_route():
    data = request.get_json(silent=True)
    if not data or "name" not in data or "correo" not in data or "password" not in data:
        logger.warning("Registro fallido: datos incompletos")
        return jsonify({"error": "name, correo y password son obligatorios"}), 400

    usuario = create_usuario(data)
    logger.info(f"Usuario creado: {data.get('name')}")
    return jsonify(usuario), 201


@usuario_bp.route("/usuarios/<int:usuario_id>", methods=["PUT"])
@jwt_required()
def update_usuario_route(usuario_id):
    data = request.get_json(silent=True)
    if not data:
        logger.warning("Update fallido: body vacío")
        return jsonify({"error": "Bad request"}), 400

    usuario = update_usuario(usuario_id, data)
    if usuario is None:
        logger.warning(f"Usuario no encontrado para actualizar: {usuario_id}")
        return jsonify({"error": "Usuario no encontrado"}), 404

    logger.info(f"Usuario actualizado: {usuario_id}")
    return jsonify(usuario), 200


@usuario_bp.route("/usuarios/<int:usuario_id>", methods=["DELETE"])
@jwt_required()
def delete_usuario_route(usuario_id):
    success = delete_usuario(usuario_id)
    if not success:
        logger.warning(f"Usuario no encontrado para eliminar: {usuario_id}")
        return jsonify({"error": "Usuario no encontrado"}), 404

    logger.info(f"Usuario eliminado: {usuario_id}")
    return jsonify({"result": "Usuario eliminado"}), 200
