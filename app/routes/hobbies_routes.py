from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from app.models.hobbies import HobbiesModel

hobbies_bp = Blueprint('hobbies', __name__)

@hobbies_bp.route('/hobbies', methods=['GET'])
def hobbies():
    """
    Renderiza la página para registrar los gustos del usuario.
    """
    username = session.get('username')
    if not username:
        # Si no hay un usuario en sesión, redirige al registro
        return redirect(url_for('auth.register'))

    return render_template('hobbies.html')

@hobbies_bp.route('/api/hobbies', methods=['POST'])
def api_hobbies():
    """
    API para registrar los gustos del usuario en la base de datos.
    """
    try:
        username = session.get('username')
        if not username:
            return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

        data = request.get_json()
        pasatiempos = data.get('pasatiempos')
        gustos_musicales = data.get('gustosMusicales')
        peliculas_favoritas = data.get('peliculasFavoritas')

        # Validar campos
        if not pasatiempos or not gustos_musicales or not peliculas_favoritas:
            return jsonify({'success': False, 'message': 'Todos los campos son obligatorios.'}), 400

        # Guardar los gustos en la base de datos y crear el nodo en Neo4j
        result = HobbiesModel.create_hobbies(username, pasatiempos, gustos_musicales, peliculas_favoritas)
        if result['success']:
            # Si se guarda correctamente, redirigir al login
            return jsonify({'success': True, 'message': result['message'], 'redirect': '/auth/login'}), 201
        else:
            return jsonify({'success': False, 'message': result['message']}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error interno del servidor.', 'error': str(e)}), 500
