import mysql.connector
from app.config import Config

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None
