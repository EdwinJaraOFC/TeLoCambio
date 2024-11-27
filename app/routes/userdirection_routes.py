from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.models.userdirection import UserDirectionModel

# Crear el blueprint para las rutas de dirección del usuario
userdirection_bp = Blueprint('userdirection', __name__)

# Ruta para la página que muestra la dirección del usuario
@userdirection_bp.route('/userdirection', methods=['GET'])
def user_direction_page():
    """
    Renderiza la página que muestra la dirección del usuario.
    """
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))  # Redirigir si no hay sesión activa

    # Recuperar la dirección del usuario desde el modelo
    result = UserDirectionModel.get_user_direction_by_username(username)
    
    # Si se encontró la dirección, la mostramos en la plantilla
    if result['success']:
        return render_template('userdirection.html', user_direction=result['data'])
    else:
        # Si no se encontró la dirección, mostrar el mensaje de error
        return render_template('userdirection.html', error=result['message'])


# Ruta para la API que devuelve la dirección del usuario en formato JSON
@userdirection_bp.route('/api/userdirection', methods=['GET'])
def api_user_direction():
    """
    API que devuelve la dirección del usuario en formato JSON.
    """
    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

    # Recuperar la dirección del usuario desde el modelo
    result = UserDirectionModel.get_user_direction_by_username(username)
    
    # Si se encontró la dirección, devolverla en formato JSON
    if result['success']:
        return jsonify({'success': True, 'data': result['data']}), 200
    else:
        return jsonify({'success': False, 'message': result['message']}), 404

# Ruta para editar la dirección
@userdirection_bp.route('/edit', methods=['POST'])
def api_edit_user_direction():
    """
    Actualiza la dirección del usuario por su nombre de usuario.
    """
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))  # Redirigir si no hay sesión activa

    # Obtener los nuevos valores del formulario
    direccion = request.form.get('direccion')
    departamento = request.form.get('departamento')
    provincia = request.form.get('provincia')
    distrito = request.form.get('distrito')

    # Actualizar los datos en la base de datos
    result = UserDirectionModel.update_user_direction_by_username(username, direccion, departamento, provincia, distrito)

    if result['success']:
        # Redirigir de nuevo a la página de dirección con los nuevos datos
        return redirect(url_for('userdirection.user_direction_page'))
    else:
        # Mostrar un mensaje de error si la actualización falla
        return render_template('userdirection.html', error=result['message'])