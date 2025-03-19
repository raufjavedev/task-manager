from flask import Blueprint, request, jsonify, session
from app.service.task_service import TaskService

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/create", methods=["POST"])
def create_task():
    """Crea una nueva tarea para el usuario autenticado"""
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Usuario no autenticado."}), 401
    
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    due_date = data.get("due_date")
    status = data.get("status", "pending")

    if not title or not due_date:
        return jsonify({"success": False, "message": "Título y fecha de vencimiento son obligatorios."}), 400

    response = TaskService.create_task(session["user_id"], title, description, due_date, status)
    return jsonify(response), (201 if response["success"] else 400)

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    """Obtiene todas las tareas del usuario autenticado"""
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Usuario no autenticado."}), 401

    response = TaskService.get_tasks_by_user(session["user_id"])
    return jsonify(response), (200 if response["success"] else 404)

@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Obtiene una tarea específica por ID"""
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Usuario no autenticado."}), 401

    response = TaskService.get_task_by_id(task_id)
    return jsonify(response), (200 if response["success"] else 404)

@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Actualiza una tarea existente"""
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Usuario no autenticado."}), 401

    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    status = data.get("status")
    due_date = data.get("due_date")

    if not title or not status or not due_date:
        return jsonify({"success": False, "message": "Título, estado y fecha de vencimiento son obligatorios."}), 400

    response = TaskService.update_task(task_id, title, description, status, due_date)
    return jsonify(response), (200 if response["success"] else 400)

@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Elimina una tarea por ID"""
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Usuario no autenticado."}), 401

    response = TaskService.delete_task(task_id)
    return jsonify(response), (200 if response["success"] else 400)
