from .main_routes import main_bp
from .auth_routes import auth_bp
from app.routes.information_routes import information_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(information_bp, url_prefix='/auth')
