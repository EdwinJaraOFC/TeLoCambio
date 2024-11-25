from flask import Blueprint, render_template
from datetime import datetime
from flask_login import login_required

# Definir el blueprint para las rutas principales
main_bp = Blueprint('main', __name__)

# Ruta principal (Index)
@main_bp.route('/')
def index():
    """Página inicial pública"""
    current_year = datetime.now().year  # Obtiene el año actual
    return render_template('index.html', current_year=current_year)  # Renderiza el archivo index.html

# Ruta Home (Autenticada)
@main_bp.route('/home')
@login_required
def home():
    """Página principal para usuarios autenticados"""
    return render_template('home.html')  # Renderiza el archivo home.html