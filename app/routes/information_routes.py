from flask import Blueprint, request, jsonify, redirect, url_for, render_template, session
from app.models.information import InformationModel
from datetime import datetime

information_bp = Blueprint('information', __name__)

@information_bp.route('/api/information', methods=['POST'])
def api_information():
    """API para guardar información personal del usuario"""
    try:
        # Obtener el username de la sesión
        username = session.get('username')
        if not username:
            return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

        data = request.get_json()
        dni = data.get('dni')
        nombre = data.get('nombre')
        fecha_nacimiento = data.get('fechaNacimiento')
        correo = data.get('correoElectronico')

        # Validar campos
        if not dni or not nombre or not fecha_nacimiento or not correo:
            return jsonify({'success': False, 'message': 'Faltan campos obligatorios.'}), 400

        # Convertir formato de fecha
        try:
            fecha_nacimiento_formato = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            return jsonify({'success': False, 'message': 'Formato de fecha inválido. Use YYYY-MM-DD.'}), 400

        # Guardar información personal
        result = InformationModel.create_information(username, dni, nombre, fecha_nacimiento_formato, correo)

        if result['success']:
            # Limpiar el username de la sesión después de registrar la información
            return jsonify({'success': True, 'message': 'Información registrada exitosamente.'}), 201
        else:
            return jsonify({'success': False, 'message': result['message']}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error interno del servidor.', 'error': str(e)}), 500

@information_bp.route('/information', methods=['GET'])
def information():
    """Página para registrar información personal"""
    # Verificar que existe un ID temporal en la sesión
    if not session.get('username'):
        return redirect(url_for('auth.register'))  # Redirigir al registro si no hay acceso autorizado

    return render_template('information.html')  # Renderiza la página de información personal