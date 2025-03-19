from app.dao.user_dao import UserDAO
from app.dao.task_dao import TaskDAO
from app.util.security import hash_password, check_password

class UserService:
    @staticmethod
    def register_user(fullName, username, email, password):
        """Registra un usuario si el email no está en uso y hashea la contraseña"""
        existing_user = UserDAO.get_user_by_email(username)
        if existing_user:
            return {"success": False, "message": "El email ya está registrado."}

        hashed_password = hash_password(password)  # Hasheamos la contraseña
        success = UserDAO.create_user(fullName, username, email, hashed_password)
        if success:
            return {"success": True, "message": "Usuario registrado correctamente."}
        else:
            return {"success": False, "message": "Error al registrar usuario."}

    @staticmethod
    def login_user(username, password):
        """Autentica al usuario verificando la contraseña"""
        user = UserDAO.get_user_by_username(username)
        if user and check_password(password, user["password_hash"]):  
            return {"success": True, "user": user}
        return {"success": False, "message": "Credenciales incorrectas."}

    @staticmethod
    def update_user(user_id, full_name, username, email):
        """Actualiza datos del usuario"""
        success = UserDAO.update_user(user_id, full_name, username, email)
        return {"success": success, "message": "Usuario actualizado correctamente." if success else "Error al actualizar usuario."}


    @staticmethod
    def delete_user(user_id):
        """Elimina las tareas asociadas al usuario antes de eliminar al usuario"""
        
        # Primero, eliminar las tareas del usuario
        success_delete_task = TaskDAO.delete_task_by_user_id(user_id)

        if success_delete_task: 
            # Ahora eliminar al usuario
            success = UserDAO.delete_user(user_id)
            
            return {
                "success": success,
                "message": "Usuario eliminado correctamente." if success else "Error al eliminar usuario."
            }

        return {
            "success": False,
            "message": "Error al eliminar tareas asociadas al usuario."
        }
        
    
    @staticmethod
    def get_user_by_id(user_id):
        user = UserDAO.get_user_by_id(user_id)  # Esto devuelve una lista
        if user:
            user_dict = {
                "id": user[0],
                "fullname": user[1],
                "username": user[2],
                "email": user[3],
                "created_at": user[4]
            }
            return {"success": True, "user": user_dict}
        else:
            return {"success": False, "message": "Usuario no encontrado."}

