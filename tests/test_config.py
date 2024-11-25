import pytest
from app.config.config import Config

def test_config_validation():
    try:
        Config.validate()
    except ValueError as e:
        pytest.fail(f"Fallo en la validación de configuración: {e}")
