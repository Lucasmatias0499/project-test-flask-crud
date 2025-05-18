from flask import Blueprint, request, jsonify
from app.user_repository import UserRepository
from app.models import User
import logging

user_bp = Blueprint('users', __name__)
user_repo = UserRepository()

logger = logging.getLogger(__name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    logger.info(f"Recebida requisição para criar usuário: {data}")
    error = User.validate_name(name)
    
    if error:
        logger.warning(f"Falha na validação do nome: {error}")
        return jsonify({"error": error}), 400
    try:
        user_id = user_repo.add(name)
        logger.info(f"Usuário criado com sucesso: id={user_id}, name={name}")
        return jsonify({"id": user_id, "name": name}), 201
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {e}")
        return jsonify({"error": "Erro interno ao criar usuário."}), 500