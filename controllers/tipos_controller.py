from flask import Blueprint, jsonify, request
from services.services import (
    get_all_tipos, get_tipo_by_id, create_tipo, update_tipo, delete_tipo
)

tipo_bp = Blueprint('tipo_bp', __name__)

@tipo_bp.route('/tipos', methods=['GET'])
def get_tipos():
    return jsonify(get_all_tipos()), 200

@tipo_bp.route('/tipos/<int:tipo_id>', methods=['GET'])
def get_tipo(tipo_id):
    tipo = get_tipo_by_id(tipo_id)
    if tipo is None:
        return jsonify({'error': 'Tipo not found'}), 404
    return jsonify(tipo), 200

@tipo_bp.route('/tipos', methods=['POST'])
def create_tipo_route():
    if not request.json or 'nombre' not in request.json:
        return jsonify({'error': 'Bad request'}), 400
    tipo = create_tipo(request.json)
    return jsonify(tipo), 201

@tipo_bp.route('/tipos/<int:tipo_id>', methods=['PUT'])
def update_tipo_route(tipo_id):
    if not request.json:
        return jsonify({'error': 'Bad request'}), 400
    tipo = update_tipo(tipo_id, request.json)
    if tipo is None:
        return jsonify({'error': 'Tipo not found'}), 404
    return jsonify(tipo), 200

@tipo_bp.route('/tipos/<int:tipo_id>', methods=['DELETE'])
def delete_tipo_route(tipo_id):
    success = delete_tipo(tipo_id)
    if not success:
        return jsonify({'error': 'Tipo not found'}), 404
    return jsonify({'result': 'Tipo deleted'}), 200
