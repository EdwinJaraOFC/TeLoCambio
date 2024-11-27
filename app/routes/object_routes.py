from flask import Blueprint, jsonify, render_template, session, redirect, url_for, request
from app.models.object import ObjectModel

object_bp = Blueprint('object', __name__)

@object_bp.route('/myobjects', methods=['GET'])
def my_objects():
    """
    Renderiza la página para mostrar los objetos del usuario.
    """
    username = session.get('username')
    if not username:
        # Redirige al login si no hay un usuario en la sesión
        return redirect(url_for('auth.login'))

    result = ObjectModel.get_objects_by_user(username)
    objetos = result['data'] if result['success'] else []

    return render_template('myobjects.html', objetos=objetos)  # Renderiza la página de objetos

@object_bp.route('/availableobjects', methods=['GET'])
def available_objects():
    """
    Renderiza la página para mostrar los objetos disponibles (que no son del usuario).
    """
    username = session.get('username')
    if not username:
        # Redirige al login si no hay un usuario en la sesión
        return redirect(url_for('auth.login'))

    # Obtener objetos disponibles (no del usuario)
    result_available = ObjectModel.get_objects_not_by_user(username)
    objetos = result_available['data'] if result_available['success'] else []

    # Obtener objetos del usuario en estado 'Disponible'
    result_my_objects = ObjectModel.get_objects_by_user(username)
    my_objects = [obj for obj in result_my_objects['data'] if obj['Estado'] == 'Disponible'] if result_my_objects['success'] else []

    return render_template('availableobjects.html', objetos=objetos, my_objects=my_objects)

@object_bp.route('/api/myobjects', methods=['GET'])
def api_get_objects():
    """
    Devuelve los objetos asociados al usuario que está en la sesión.
    """
    username = session.get('username')
    if not username:
        # Redirige al login si no hay un usuario en la sesión
        return redirect(url_for('auth.login'))

    # Recuperar los objetos del usuario
    result = ObjectModel.get_objects_by_user(username)
    if result['success']:
        return jsonify({'success': True, 'data': result['data']})
    else:
        return jsonify({'success': False, 'message': result['message']}), 400

@object_bp.route('/api/objects/<int:object_id>', methods=['DELETE'])
def api_delete_object(object_id):
    """
    Elimina un objeto por su ID.
    """
    print(f"Intentando eliminar el objeto con ID: {object_id}")
    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

    # Llamar al modelo para eliminar el objeto
    result = ObjectModel.delete_object_by_id(object_id)
    if result['success']:
        return jsonify({'success': True, 'message': result['message']}), 200
    else:
        return jsonify({'success': False, 'message': result['message']}), 400

@object_bp.route('/api/objects/not-my-objects', methods=['GET'])
def api_get_objects_not_by_user():
    """
    Devuelve todos los objetos que no están asociados al usuario que está en la sesión.
    """
    username = session.get('username')
    if not username:
        # Redirige al login si no hay un usuario en la sesión
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

    # Recuperar los objetos que no son del usuario en sesión
    result = ObjectModel.get_objects_not_by_user(username)
    if result['success']:
        return jsonify({'success': True, 'data': result['data']}), 200
    else:
        return jsonify({'success': False, 'message': result['message']}), 400