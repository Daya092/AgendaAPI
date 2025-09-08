from flask import Blueprint, jsonify, request
from services.services import (
    get_all_movimientos, get_movimiento_by_id, create_movimiento, update_movimiento, delete_movimiento
)

movimiento_bp = Blueprint('movimiento_bp', __name__)

@movimiento_bp.route('/movimientos', methods=['GET'])
def get_movimientos():
    return jsonify(get_all_movimientos()), 200

@movimiento_bp.route('/movimientos/<int:mov_id>', methods=['GET'])
def get_movimiento(mov_id):
    m = get_movimiento_by_id(mov_id)
    if not m:
        return jsonify({'error': 'Movimiento not found'}), 404
    return jsonify(m), 200

@movimiento_bp.route('/movimientos', methods=['POST'])
def create_movimiento_route():
    if not request.json or 'tipo_id' not in request.json or 'usuario_id' not in request.json or 'monto' not in request.json:
        return jsonify({'error': 'Bad request'}), 400
    m = create_movimiento(request.json)
    return jsonify(m), 201

@movimiento_bp.route('/movimientos/<int:mov_id>', methods=['PUT'])
def update_movimiento_route(mov_id):
    if not request.json:
        return jsonify({'error': 'Bad request'}), 400
    m = update_movimiento(mov_id, request.json)
    if not m:
        return jsonify({'error': 'Movimiento not found'}), 404
    return jsonify(m), 200

@movimiento_bp.route('/movimientos/<int:mov_id>', methods=['DELETE'])
def delete_movimiento_route(mov_id):
    success = delete_movimiento(mov_id)
    if not success:
        return jsonify({'error': 'Movimiento not found'}), 404
    return jsonify({'result': 'Movimiento deleted'}), 200

