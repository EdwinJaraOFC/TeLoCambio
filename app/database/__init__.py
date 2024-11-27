import pymysql
from flask import g
from dotenv import load_dotenv
from app.config.config import Config
from neo4j import GraphDatabase

# Función para obtener la conexión a la base de datos MySQL
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
        raise RuntimeError(f"Error al conectar a la base de datos MySQL: {e}")
    return g.db_connection

def close_db_connection(e=None):
    db_connection = g.pop('db_connection', None)
    if db_connection and db_connection.open:
        db_connection.close()

# Función para obtener la conexión a la base de datos Neo4j
def get_neo4j_connection():
    try:
        if 'neo4j_connection' not in g:
            g.neo4j_connection = GraphDatabase.driver(
                Config.NEO4J_URI, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
            )
    except Exception as e:
        raise RuntimeError(f"Error al conectar a la base de datos Neo4j: {e}")
    return g.neo4j_connection

# Función para cerrar la conexión de Neo4j
def close_neo4j_connection(e=None):
    neo4j_connection = g.pop('neo4j_connection', None)
    if neo4j_connection:
        neo4j_connection.close()
