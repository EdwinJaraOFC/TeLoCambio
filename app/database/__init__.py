import pymysql
from flask import g
from dotenv import load_dotenv
from app.config.config import Config

# Función para obtener la conexión a la base de datos
def get_db_connection():
    try:
        if 'db_connection' not in g:
            g.db_connection = pymysql.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                db=Config.MYSQL_DB,
                port=Config.MYSQL_PORT,
                cursorclass=pymysql.cursors.DictCursor
            )
    except pymysql.MySQLError as e:
        raise RuntimeError(f"Error al conectar a la base de datos: {e}")
    return g.db_connection

# Cerrar la conexión al final de cada solicitud
def close_db_connection(e=None):
    db_connection = g.pop('db_connection', None)
def close_db_connection(e=None):
    db_connection = g.pop('db_connection', None)
    if db_connection and db_connection.open:  # Verifica si la conexión existe y está abierta
        db_connection.close()

