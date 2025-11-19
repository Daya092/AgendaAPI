from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.services import (
    get_todas_clases,
    get_horarios_disponibles,
    inscribir_en_clase,
    get_mis_clases
)

clases_bp = Blueprint("clases_bp", __name__, url_prefix="/api")

@clases_bp.route("/clases", methods=["GET"])
@jwt_required()
def obtener_clases():
    """Obtiene todas las clases disponibles"""
    clases = get_todas_clases()
    return jsonify(clases)

@clases_bp.route("/clases/<int:clase_id>/horarios", methods=["GET"])
@jwt_required()
def obtener_horarios_clase(clase_id):
    """Obtiene horarios disponibles para una clase"""
    horarios = get_horarios_disponibles(clase_id)
    return jsonify(horarios)

@clases_bp.route("/clases/inscribir", methods=["POST"])
@jwt_required()
def inscribir_clase():
    """Inscribe al usuario en una clase"""
    usuario_id = get_jwt_identity()
    data = request.get_json()
    
    horario_id = data.get("horario_id")
    fecha_clase = data.get("fecha_clase")
    
    if not horario_id or not fecha_clase:
        return jsonify({"error": "Horario ID y fecha son requeridos"}), 400
    
    resultado = inscribir_en_clase(usuario_id, horario_id, fecha_clase)
    
    if resultado.get("error"):
        return jsonify(resultado), 400
    
    return jsonify(resultado)

@clases_bp.route("/mis-clases", methods=["GET"])
@jwt_required()
def mis_clases():
    """Obtiene las clases del usuario"""
    usuario_id = get_jwt_identity()
    clases = get_mis_clases(usuario_id)
    return jsonify(clases)


@clases_bp.route("/clases/cancelar/<int:inscripcion_id>", methods=["DELETE"])
@jwt_required()
def cancelar_clase(inscripcion_id):
    """Cancela una inscripción existente"""
    usuario_id = get_jwt_identity()
    
    # Necesitarás crear esta función en services.py
    from services.services import cancelar_inscripcion
    resultado = cancelar_inscripcion(usuario_id, inscripcion_id)
    
    if resultado.get("error"):
        return jsonify(resultado), 400
    
    return jsonify(resultado)