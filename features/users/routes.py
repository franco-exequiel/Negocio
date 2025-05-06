# features/users/routes.py

from flask import Blueprint, request, jsonify, render_template
from core.db import db
from features.users.models import User
from typing import Any, Dict
from .schemas import UserCreate

users_bp = Blueprint("users", __name__, url_prefix="/users")

# HTML: vista de prueba (formulario simple)
@users_bp.route("/web", methods=["GET"])
def user_form() -> Any:
    users = User.query.all()
    return render_template("users.html", users=users)

# Obtener todos los usuarios
@users_bp.route("/", methods=["GET"])
def get_users() -> Any:
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "phone": u.phone
    } for u in users]), 200

# Obtener un usuario por ID
@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> Any:
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone
    }), 200

# Crear usuario
@users_bp.route("/", methods=["POST"])
def create_user():
    try:
        data = request.form.to_dict()
        validated = UserCreate(**data)

        user = User(
            name=validated.name,
            email=validated.email,
            phone=validated.phone,
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Usuario creado exitosamente."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Actualizar usuario
@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int) -> Any:
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data: Dict[str, Any] = request.get_json()
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.phone = data.get("phone", user.phone)

    db.session.commit()
    return jsonify({"message": "Usuario actualizado"}), 200

# Eliminar usuario
@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int) -> Any:
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200




