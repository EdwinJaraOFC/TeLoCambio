from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from app.models.direction import DirectionModel

direction_bp = Blueprint('direction', __name__)

@direction_bp.route('/api/direction', methods=['POST'])
def api_direction():
    """
    API para registrar la dirección del usuario en la base de datos.
    """
    try:
        username = session.get('username')
        if not username:
            return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

        data = request.get_json()
        direccion = data.get('direccion')
        departamento = data.get('departamento')
        provincia = data.get('provincia')
        distrito = data.get('distrito')

        # Validar campos
        if not direccion or not departamento or not provincia or not distrito:
            return jsonify({'success': False, 'message': 'Todos los campos son obligatorios.'}), 400

        # Guardar la dirección en la base de datos y crear el nodo en Neo4j
        result = DirectionModel.create_direction(username, direccion, departamento, provincia, distrito)
        if result['success']:
            # Si se guarda correctamente, redirigir a la página de hobbies o cualquier otra página relevante
            return jsonify({'success': True, 'message': result['message'], 'redirect': '/auth/hobbies'}), 201
        else:
            return jsonify({'success': False, 'message': result['message']}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error interno del servidor.', 'error': str(e)}), 500

@direction_bp.route('/direction', methods=['GET'])
def direction():
    """
    Renderiza la página para registrar la dirección del usuario.
    """
    if not session.get('username'):
        # Si no hay un usuario en sesión, redirige al registro
        return redirect(url_for('auth.register'))
    
    return render_template('direction.html')  # Renderiza la página para registrar la dirección
