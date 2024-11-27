from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from app.models.user import UserModel

auth_bp = Blueprint('auth', __name__)

# Rutas para la API REST
@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    """API para registrar un nuevo usuario"""
    try:
        data = request.get_json()  # Leer los datos de la solicitud JSON
        username = data.get('username')
        password = data.get('password')

        # Validar datos
        if not username or not password:
            return jsonify({'success': False, 'message': 'Faltan campos obligatorios.'}), 400

        # Crear usuario en MySQL y crear su nodo en Neo4j
        result = UserModel.create_user(username, password)

        if result['success']:
            # Guardar el username en la sesión (si lo deseas)
            session['username'] = username
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'message': 'Error interno del servidor.', 'error': str(e)}), 500

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    """API para iniciar sesión"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validar datos
        if not username or not password:
            return jsonify({'success': False, 'message': 'Faltan campos obligatorios.'}), 400

        # Autenticar usuario
        result = UserModel.authenticate_user(username, password)
        if result['success']:
            user = result['user']
            login_user(user)  # Inicia sesión con Flask-Login
            session['username'] = username
            return jsonify({'success': True, 'message': 'Inicio de sesión exitoso.'}), 200
        else:
            return jsonify(result), 401
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error interno del servidor.', 'error': str(e)}), 500

# Rutas para vistas HTML
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página para registrar un nuevo usuario"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validar datos
        if not username or not password:
            flash('Faltan campos obligatorios.', 'danger')
            return render_template('register.html')

        # Crear usuario
        result = UserModel.create_user(username, password)
        if result['success']:
            flash('Usuario registrado exitosamente. Por favor, inicia sesión.', 'success')
            return redirect(url_for('auth.login'))  # Redirigir al login tras registro exitoso
        else:
            flash(result['message'], 'danger')
            return render_template('register.html')

    return render_template('register.html')  # Renderiza la página de registro

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página para iniciar sesión"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validar datos
        if not username or not password:
            flash('Faltan campos obligatorios.', 'danger')
            return render_template('login.html')

        # Validar credenciales
        result = UserModel.authenticate_user(username, password)
        if result['success']:
            user = result['user']
            login_user(user)  # Inicia sesión con Flask-Login
            flash('Inicio de sesión exitoso.', 'success')

            # Redirigir al `next` si existe
            next_page = request.args.get('next')  # Obtiene el valor de `next`
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))  # Si no hay `next`, redirige al dashboard
        else:
            flash(result['message'], 'danger')
            return render_template('login.html')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Cierra la sesión del usuario"""
    logout_user()  # Cierra la sesión
    session.pop('username', None)  # Limpia el username de la sesión manualmente
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))
