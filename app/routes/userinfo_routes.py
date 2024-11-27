from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.models.userinfo import UserInfoModel

userinfo_bp = Blueprint('userinfo', __name__)

@userinfo_bp.route('/userinfo', methods=['GET'])
def user_info_page():
    """
    Renderiza la página que muestra la información personal del usuario.
    """
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))  # Redirigir si no hay sesión activa

    result = UserInfoModel.get_user_info_by_username(username)
    if result['success']:
        return render_template('userinfo.html', user_info=result['data'])
    else:
        return render_template('userinfo.html', error=result['message'])


@userinfo_bp.route('/api/userinfo', methods=['GET'])
def api_user_info():
    """
    API que devuelve la información personal del usuario en formato JSON.
    """
    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

    result = UserInfoModel.get_user_info_by_username(username)
    if result['success']:
        return jsonify({'success': True, 'data': result['data']}), 200
    else:
        return jsonify({'success': False, 'message': result['message']}), 404

# Ruta para editar la información personal
@userinfo_bp.route('/edit', methods=['POST'])
def api_edit_user_info():
    """
    Actualiza la información personal del usuario por su nombre de usuario.
    """
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))  # Redirigir si no hay sesión activa

    # Obtener los nuevos valores del formulario
    dni = request.form.get('dni')
    nombre = request.form.get('nombre')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    correo_electronico = request.form.get('correo_electronico')

    # Actualizar los datos en la base de datos
    result = UserInfoModel.update_user_info_by_username(username, dni, nombre, fecha_nacimiento, correo_electronico)

    if result['success']:
        # Redirigir de nuevo a la página de información con los nuevos datos
        return redirect(url_for('userinfo.user_info_page'))
    else:
        # Mostrar un mensaje de error si la actualización falla
        return render_template('userinfo.html', error=result['message'])