from flask import Flask
from flask_login import LoginManager
from .database import close_db_connection, close_neo4j_connection
from .config.config import Config
from .routes import register_blueprints
from .models.user import UserModel  # Importar el modelo de usuario para Flask-Login

# Crear una instancia de LoginManager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)  # Crear la aplicación Flask
    app.config.from_object(Config)  # Cargar configuración desde la clase Config
    Config.validate()  # Validar que todas las variables de entorno necesarias están configuradas

    # Registrar todos los blueprints
    register_blueprints(app)

    # Configurar el cierre automático de la conexión de MySQL y Neo4j
    app.teardown_appcontext(close_db_connection)  # Cerrar la conexión de MySQL
    app.teardown_appcontext(close_neo4j_connection)  # Cerrar la conexión de Neo4j

    # Inicializar Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Vista para redirigir si no está autenticado
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
    login_manager.login_message_category = "info"  # Clase de alerta de Bootstrap

    return app

@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario desde el ID"""
    return UserModel.get_user_by_id(user_id)
