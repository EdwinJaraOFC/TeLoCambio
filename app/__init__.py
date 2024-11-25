from flask import Flask
from .database import close_db_connection
from .config.config import Config
from .routes import register_blueprints

def create_app():
    app = Flask(__name__) # Crear la aplicación Flask
    app.config.from_object(Config) # Cargar configuración desde la clase Config
    Config.validate() # Validar que todas las variables de entorno necesarias están configuradas

    # Registrar todos los blueprints
    register_blueprints(app)

    # Configurar el cierre automático de la conexión
    app.teardown_appcontext(close_db_connection)

    return app