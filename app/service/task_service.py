from app.dao.task_dao import TaskDAO

class TaskService:
    @staticmethod
    def create_task(user_id, title, description, due_date, status="pending"):
        """Crea una nueva tarea"""
        task_id = TaskDAO.create_task(user_id, title, description, due_date, status)
        if task_id:
            return {"success": True, "task_id": task_id, "message": "Tarea creada exitosamente."}
        return {"success": False, "message": "Error al crear la tarea."}

    @staticmethod
    def get_tasks_by_user(user_id):
        """Obtiene todas las tareas de un usuario"""
        tasks = TaskDAO.get_tasks_by_user(user_id)
        return {"success": True, "tasks": tasks} if tasks else {"success": False, "message": "No se encontraron tareas."}

    @staticmethod
    def get_task_by_id(task_id):
        """Obtiene una tarea específica"""
        task = TaskDAO.get_task_by_id(task_id)
        return {"success": True, "task": task} if task else {"success": False, "message": "Tarea no encontrada."} 

    @staticmethod
    def update_task(task_id, title, description, status, due_date):
        """Actualiza una tarea"""
        success = TaskDAO.update_task(task_id, title, description, status, due_date)
        return {"success": success, "message": "Tarea actualizada correctamente." if success else "Error al actualizar tarea."}

    @staticmethod
    def delete_task(task_id):
        """Elimina una tarea"""
        success = TaskDAO.delete_task(task_id)
        return {"success": success, "message": "Tarea eliminada correctamente." if success else "Error al eliminar tarea."}
