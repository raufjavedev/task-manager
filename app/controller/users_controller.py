from flask import Blueprint, request, jsonify, session
from app.service.user_service import UserService

users_bp = Blueprint("users", __name__)

@users_bp.route("/register", methods=["POST"])
def register():
    """Registra un nuevo usuario"""
    data = request.get_json()
    fullName = data.get("username")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"success": False, "message": "Todos los campos son obligatorios."}), 400

    response = UserService.register_user(fullName, username, email, password)
    return jsonify(response), (201 if response["success"] else 400)

@users_bp.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Actualiza usuario exitente"""
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    full_name = data.get("fullName")

    if not username or not email:
        return jsonify({"success": False, "message": "Todos los campos son obligatorios."}), 400

    response = UserService.update_user(user_id, full_name, username, email)
    return jsonify(response), (201 if response["success"] else 400)

@users_bp.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Elimina un usuario por ID"""
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Usuario no autenticado."}), 401

    response = UserService.delete_user(user_id)
    return jsonify(response), (200 if response["success"] else 400)


@users_bp.route("/login", methods=["POST"])
def login():
    """Autentica un usuario"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Usuario y contraseña requeridos."}), 400

    response = UserService.login_user(username, password)
    
    if response["success"]:
        session["user_id"] = response["user"]["id"]  # Guardar ID del usuario en sesión
        return jsonify(response), 200
    else:
        return jsonify(response), 401

@users_bp.route("/logout", methods=["POST"])
def logout():
    """Cierra sesión del usuario"""
    session.pop("user_id", None)
    return jsonify({"success": True, "message": "Sesión cerrada correctamente."}), 200

@users_bp.route("/profile", methods=["GET"])
def get_profile():
    """Obtiene el perfil del usuario autenticado"""
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Usuario no autenticado."}), 401

    response = UserService.get_user_by_id(session["user_id"])
    return jsonify(response), (200 if response["success"] else 404)
