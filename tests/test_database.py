import pytest
from app import create_app
from app.database import get_db_connection

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

def test_db_connection(app):
    with app.app_context():
        conn = get_db_connection()
        assert conn.open, "Error: No se pudo establecer la conexión a la base de datos"