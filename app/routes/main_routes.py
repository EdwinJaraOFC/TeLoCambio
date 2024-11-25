from flask import Blueprint, render_template
from datetime import datetime

# Definir el blueprint para las rutas principales
main_bp = Blueprint('main', __name__)

# Ruta principal (Index)
@main_bp.route('/')
def index():
    current_year = datetime.now().year  # Obtiene el año actual
    return render_template('index.html', current_year=current_year) # Renderiza el archivo index.html

# Ruta para Login
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')  # Renderiza el archivo login.html

# Ruta para Register
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')  # Renderiza el archivo register.html
