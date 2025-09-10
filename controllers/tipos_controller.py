from flask import Blueprint, jsonify
from services.services import get_all_tipos

tipo_bp = Blueprint('tipo_bp', __name__)

@tipo_bp.route('/tipos', methods=['GET'])
def get_tipos():
    return jsonify(get_all_tipos()), 200

