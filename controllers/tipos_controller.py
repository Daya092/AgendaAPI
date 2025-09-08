from flask import Blueprint, jsonify
from services.services import get_all_tipos, get_tipo_by_id

tipo_bp = Blueprint('tipo_bp', __name__)

@tipo_bp.route('/tipos', methods=['GET'])
def get_tipos():
    return jsonify(get_all_tipos()), 200

@tipo_bp.route('/tipos/<int:tipo_id>', methods=['GET'])
def get_tipo(tipo_id):
    t = get_tipo_by_id(tipo_id)
    if not t:
        return jsonify({'error': 'Tipo not found'}), 404
    return jsonify(t), 200
