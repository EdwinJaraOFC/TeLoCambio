from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.models.userhobbies import UserHobbiesModel

# Crear el blueprint para las rutas de hobbies del usuario
userhobbies_bp = Blueprint('userhobbies', __name__)

# Ruta para la página que muestra los hobbies del usuario
@userhobbies_bp.route('/userhobbies', methods=['GET'])
def user_hobbies_page():
    """
    Renderiza la página que muestra los hobbies del usuario.
    """
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))  # Redirigir si no hay sesión activa

    # Recuperar los hobbies del usuario desde el modelo
    result = UserHobbiesModel.get_user_hobbies_by_username(username)
    
    # Si se encontró la información, mostrarla en la plantilla
    if result['success']:
        return render_template('userhobbies.html', user_hobbies=result['data'])
    else:
        # Si no se encontró información, mostrar el mensaje de error
        return render_template('userhobbies.html', error=result['message'])


# Ruta para la API que devuelve los hobbies del usuario en formato JSON
@userhobbies_bp.route('/api/userhobbies', methods=['GET'])
def api_user_hobbies():
    """
    API que devuelve los hobbies del usuario en formato JSON.
    """
    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

    # Recuperar los hobbies del usuario desde el modelo
    result = UserHobbiesModel.get_user_hobbies_by_username(username)
    
    # Si se encontraron los datos, devolverlos en formato JSON
    if result['success']:
        return jsonify({'success': True, 'data': result['data']}), 200
    else:
        return jsonify({'success': False, 'message': result['message']}), 404

# Ruta para editar los gustos
@userhobbies_bp.route('/edit', methods=['POST'])
def api_edit_user_hobbies():
    """
    Actualiza los gustos y hobbies del usuario por su nombre de usuario.
    """
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))  # Redirigir si no hay sesión activa

    # Obtener los nuevos valores del formulario
    pasatiempos = request.form.get('pasatiempos')
    gustos_musicales = request.form.get('gustos_musicales')
    peliculas_favoritas = request.form.get('peliculas_favoritas')

    # Actualizar los datos en la base de datos
    result = UserHobbiesModel.update_user_hobbies_by_username(username, pasatiempos, gustos_musicales, peliculas_favoritas)

    if result['success']:
        # Redirigir de nuevo a la página de hobbies con los nuevos datos
        return redirect(url_for('userhobbies.user_hobbies_page'))
    else:
        # Mostrar un mensaje de error si la actualización falla
        return render_template('userhobbies.html', error=result['message'])