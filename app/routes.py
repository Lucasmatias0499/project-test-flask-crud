from flask import Blueprint, request, jsonify
from app.user_repository import UserRepository
from app.models import User


user_bp = Blueprint('users', __name__)
user_repo = UserRepository()


@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    error = User.validate_name(name)
    if error:
        return jsonify({"error": error}), 400
    user_id = user_repo.add(name)
    return jsonify({"id": user_id, "name": name}), 201