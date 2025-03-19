import mysql.connector
from app.database import get_connection

class UserDAO:
    @staticmethod
    def create_user(fullName, username, email, password_hash):
        """Inserta un nuevo usuario en la base de datos"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = """INSERT INTO users (full_name, username, email, password_hash) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (fullName, username, email, password_hash))
            connection.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error en create_user: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def get_user_by_username(username):
        """Busca un usuario por su nombre de usuario"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        except mysql.connector.Error as e:
            print(f"Error en get_user_by_email: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Obtiene los datos del usuario por su id"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = """SELECT id, full_name, username, email, created_at FROM users WHERE id = %s"""
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            return user
        except mysql.connector.Error as e:
            print(f"Error en get_user_by_id: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def update_user(user_id, full_name, username, email):
        """Actualiza los datos de un usuario"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = """UPDATE users SET full_name = %s, username = %s, email = %s 
                       WHERE id = %s"""
            cursor.execute(query, (full_name, username, email, user_id))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as e:
            print(f"Error en update_user: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def delete_user(user_id):
        """Elimina un usuario por su ID"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as e:
            print(f"Error en delete_user: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
