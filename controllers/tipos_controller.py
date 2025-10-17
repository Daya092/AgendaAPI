import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.services import get_all_tipos, get_tipo_by_id, create_tipo

logger = logging.getLogger(__name__)
tipo_bp = Blueprint("tipo_bp", __name__, url_prefix="/api")

@tipo_bp.route("/tipos", methods=["GET"])
@jwt_required()
def get_tipos():
    tipos = get_all_tipos()
    return jsonify(tipos), 200

@tipo_bp.route("/tipos/<int:tipo_id>", methods=["GET"])
@jwt_required()
def get_tipo(tipo_id):
    tipo = get_tipo_by_id(tipo_id)
    if not tipo:
        return jsonify({"error": "Tipo no encontrado"}), 404
    return jsonify(tipo), 200

@tipo_bp.route("/tipos", methods=["POST"])
@jwt_required()
def create_tipo_route():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name es obligatorio"}), 400
    
    tipo = create_tipo(data)
    return jsonify(tipo), 201