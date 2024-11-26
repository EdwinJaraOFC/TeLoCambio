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

# Ruta dashboard (Autenticada)
@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Página principal para usuarios autenticados"""
    current_year = datetime.now().year  # Obtiene el año actual
    return render_template('dashboard.html', current_year=current_year)  # Renderiza el archivo dashboard.html