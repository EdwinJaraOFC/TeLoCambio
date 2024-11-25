import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

class Config:
    # Configuración de la aplicación
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

    # Configuración de la base de datos MySQL
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
    MYSQL_DB = os.getenv('MYSQL_DB', 'database')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))

    # Configuración de la base de datos Neo4j
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

    @staticmethod
    def validate():
        required_vars = [
            'SECRET_KEY', 'MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DB', 'MYSQL_PORT',
            'NEO4J_URI', 'NEO4J_USER', 'NEO4J_PASSWORD'
        ]
        for var in required_vars:
            if not getattr(Config, var, None):
                raise ValueError(f"La variable de entorno {var} no está configurada.")
