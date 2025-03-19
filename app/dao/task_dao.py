import mysql.connector
from app.database import get_connection

class TaskDAO:
    @staticmethod
    def create_task(user_id, title, description, due_date, status):
        """Inserta una nueva tarea en la base de datos"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = """INSERT INTO tasks (user_id, title, description, status, due_date) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (user_id, title, description, status, due_date))
            connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error as e:
            print(f"Error en create_task: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def get_tasks_by_user(user_id):
        """Obtiene todas las tareas de un usuario"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM tasks WHERE user_id = %s ORDER BY created_at DESC"
            cursor.execute(query, (user_id,))
            tasks = cursor.fetchall()
            return tasks
        except mysql.connector.Error as e:
            print(f"Error en get_tasks_by_user: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def get_task_by_id(task_id):
        """Obtiene una tarea específica por su ID"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM tasks WHERE id = %s"
            cursor.execute(query, (task_id,))
            task = cursor.fetchone()
            return task
        except mysql.connector.Error as e:
            print(f"Error en get_task_by_id: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def update_task(task_id, title, description, status, due_date):
        """Actualiza una tarea existente"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = """UPDATE tasks SET title = %s, description = %s, 
                       status = %s, due_date = %s WHERE id = %s"""
            cursor.execute(query, (title, description, status, due_date, task_id))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as e:
            print(f"Error en update_task: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def delete_task(task_id):
        """Elimina una tarea por su ID"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = "DELETE FROM tasks WHERE id = %s"
            cursor.execute(query, (task_id,))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as e:
            print(f"Error en delete_task: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def delete_task_by_user_id(user_id):
        """Elimina toda la tarea asociada a un usuario"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = "DELETE FROM tasks WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            
            if cursor.rowcount > 0:
                connection.commit()
                return True
            else:
                connection.rollback()  # Rollback si no se eliminó ninguna fila
                return False

        except mysql.connector.Error as e:
            if connection:
                connection.rollback()  # Rollback en caso de error
            print(f"Error en delete_task: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

