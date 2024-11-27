from .main_routes import main_bp
from .auth_routes import auth_bp
from app.routes.information_routes import information_bp
from .direction_routes import direction_bp
from .hobbies_routes import hobbies_bp
from .object_routes import object_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(information_bp, url_prefix='/auth')
    app.register_blueprint(direction_bp, url_prefix='/auth')
    app.register_blueprint(hobbies_bp, url_prefix='/auth')
    app.register_blueprint(object_bp, url_prefix='/objects')  # Registra el blueprint de objetos
