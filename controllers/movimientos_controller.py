import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.services import (
    get_movimientos_usuario_actual,
    get_movimiento_by_id,
    create_movimiento,
    update_movimiento,
    delete_movimiento,
    get_resumen_usuario
)

logger = logging.getLogger(__name__)
movimiento_bp = Blueprint("movimiento_bp", __name__, url_prefix="/api")

@movimiento_bp.route("/movimientos", methods=["GET"])
@jwt_required()
def get_movimientos():
    usuario_id = int(get_jwt_identity())
    movimientos = get_movimientos_usuario_actual(usuario_id)
    return jsonify(movimientos), 200

@movimiento_bp.route("/movimientos/<int:mov_id>", methods=["GET"])
@jwt_required()
def get_movimiento(mov_id):
    usuario_id = int(get_jwt_identity())
    movimiento = get_movimiento_by_id(mov_id, usuario_id)
    if not movimiento:
        return jsonify({"error": "Movimiento no encontrado"}), 404
    return jsonify(movimiento), 200

@movimiento_bp.route("/movimientos", methods=["POST"])
@jwt_required()
def create_movimiento_route():
    usuario_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or "monto" not in data or "tipo_id" not in data:
        return jsonify({"error": "monto y tipo_id son obligatorios"}), 400
    
    data["usuario_id"] = usuario_id
    movimiento = create_movimiento(data)
    return jsonify(movimiento), 201

@movimiento_bp.route("/movimientos/<int:mov_id>", methods=["PUT"])
@jwt_required()
def update_movimiento_route(mov_id):
    usuario_id = int(get_jwt_identity())
    data = request.get_json()
    
    movimiento = update_movimiento(mov_id, data, usuario_id)
    if not movimiento:
        return jsonify({"error": "Movimiento no encontrado"}), 404
    
    return jsonify(movimiento), 200

@movimiento_bp.route("/movimientos/<int:mov_id>", methods=["DELETE"])
@jwt_required()
def delete_movimiento_route(mov_id):
    usuario_id = int(get_jwt_identity())
    success = delete_movimiento(mov_id, usuario_id)
    
    if not success:
        return jsonify({"error": "Movimiento no encontrado"}), 404
    
    return jsonify({"message": "Movimiento eliminado"}), 200

@movimiento_bp.route("/resumen", methods=["GET"])
@jwt_required()
def get_resumen():
    usuario_id = int(get_jwt_identity())
    resumen = get_resumen_usuario(usuario_id)
    return jsonify(resumen), 200