from .main_routes import main_bp
from .auth_routes import auth_bp
from .information_routes import information_bp
from .direction_routes import direction_bp
from .hobbies_routes import hobbies_bp
from .object_routes import object_bp
from .userinfo_routes import userinfo_bp
from app.routes.userdirection_routes import userdirection_bp
from app.routes.userhobbies_routes import userhobbies_bp
from .exchanges_routes import exchanges_bp  # Importamos el blueprint de intercambios

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(information_bp, url_prefix='/auth')
    app.register_blueprint(direction_bp, url_prefix='/auth')
    app.register_blueprint(hobbies_bp, url_prefix='/auth')
    app.register_blueprint(object_bp, url_prefix='/objects')  # Registra el blueprint de objetos
    app.register_blueprint(userinfo_bp, url_prefix='/userinfo')
    app.register_blueprint(userdirection_bp, url_prefix='/userdirection')
    app.register_blueprint(userhobbies_bp, url_prefix='/userhobbies')  # Nuevo prefijo '/userhobbies'
    app.register_blueprint(exchanges_bp, url_prefix='/exchanges')
