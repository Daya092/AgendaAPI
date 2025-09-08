from flask import Blueprint, jsonify, request
from services.services import (
    get_all_usuarios, get_usuario_by_id, create_usuario, update_usuario, delete_usuario
)

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    return jsonify(get_all_usuarios()), 200

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    usuario = get_usuario_by_id(usuario_id)
    if usuario is None:
        return jsonify({'error': 'Usuario not found'}), 404
    return jsonify(usuario), 200

@usuario_bp.route('/usuarios', methods=['POST'])
def create_usuario_route():
    if not request.json or 'nombre' not in request.json or 'email' not in request.json:
        return jsonify({'error': 'Bad request'}), 400
    usuario = create_usuario(request.json)
    return jsonify(usuario), 201

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def update_usuario_route(usuario_id):
    if not request.json:
        return jsonify({'error': 'Bad request'}), 400
    usuario = update_usuario(usuario_id, request.json)
    if usuario is None:
        return jsonify({'error': 'Usuario not found'}), 404
    return jsonify(usuario), 200

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def delete_usuario_route(usuario_id):
    success = delete_usuario(usuario_id)
    if not success:
        return jsonify({'error': 'Usuario not found'}), 404
    return jsonify({'result': 'Usuario deleted'}), 200
