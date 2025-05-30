from flask import Blueprint, request, jsonify
from app.user_repository import UserRepository
from app.models import User
import logging

user_bp = Blueprint('users', __name__)
user_repo = UserRepository()

logger = logging.getLogger(__name__)


@user_bp.route('/users', methods=['GET'])
def get_users():
    logger.info("Recebida requisição para obter todos os usuários.")
    try:
        users = user_repo.get_all()
        logger.info(f"Todos os usuários listados com sucesso")
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        logger.error(f"Erro ao obter usuários: {e}")
        return jsonify({"error": "Erro interno ao obter usuários."}), 500


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    logger.info(f"Recebida requisição para obter usuário com id={user_id}.")
    try:
        user = user_repo.get_by_id(user_id)
        if user:
            logger.info(f"Usuário encontrado: {user.to_dict()}")
            return jsonify(user.to_dict()), 200
        else:
            logger.warning(f"Usuário com id={user_id} não encontrado.")
            return jsonify({"error": "Usuário não encontrado."}), 404
    except Exception as e:
        logger.error(f"Erro ao obter usuário: {e}")
        return jsonify({"error": "Erro interno ao obter usuário."}), 500
    

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json(silent=True)
    if not data:
        logger.warning("JSON inválido ou não enviado.")
        return jsonify({"error": "JSON inválido ou não enviado."}), 400
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
    
   
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json(silent=True)
    if not data:
        logger.warning("JSON inválido ou não enviado.")
        return jsonify({"error": "JSON inválido ou não enviado."}), 400
    name = data.get('name')
    logger.info(f"Recebida requisição para atualizar usuário com id={user_id}: {data}")
    error = User.validate_name(name)
    if error:
        logger.warning(f"Falha na validação do nome: {error}")
        return jsonify({"error": error}), 400
    try:
        updated_user = user_repo.update(user_id, name)
        if not updated_user:
            logger.warning(f"Usuário com id={user_id} não encontrado para atualização.")
            return jsonify({"error": "Usuário não encontrado."}), 404
        logger.info(f"Usuário atualizado com sucesso: id={user_id}, name={name}")
        return jsonify(updated_user.to_dict()), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar usuário: {e}")
        return jsonify({"error": "Erro interno ao atualizar usuário."}), 500


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    logger.info(f"Recebida requisição para deletar usuário com id={user_id}.")
    try:
        user = user_repo.get_by_id(user_id)
        if not user:
            logger.warning(f"Tentativa de deletar usuário inexistente: id={user_id}")
            return jsonify({"error": "Usuário não encontrado."}), 404
        name = user.name
        user_repo.delete(user_id)
        logger.info(f"Usuário deletado com sucesso: id={user_id}, name={name}")
        return jsonify({"message": f"Usuário {name} deletado com sucesso."}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar usuário: {e}")
        return jsonify({"error": "Erro interno ao deletar usuário."}), 500