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

# Ruta para manejar el formulario de agregar objeto
@object_bp.route('/api/add-object', methods=['POST'])
def api_add_object():
    """API para agregar un nuevo objeto."""
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))  # Redirigir si no hay sesión activa

    # Obtener los datos del formulario
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    url_imagen = request.form['url_imagen']
    url_video = request.form.get('url_video')  # URL Video es opcional

    # Crear el nuevo objeto en la base de datos
    result = ObjectModel.add_object(username, nombre, descripcion, url_imagen, url_video)

    if result['success']:
        # Redirigir a la página de objetos disponibles
        return redirect(url_for('object.my_objects'))
    else:
        # Mostrar error si algo falla
        return render_template('addobjects.html', error=result['message'])

# Ruta para agregar un objeto (mostrar formulario)
@object_bp.route('/add-object', methods=['GET'])
def add_object_page():
    """Página para agregar un nuevo objeto."""
    return render_template('addobjects.html')

# Ruta para editar un objeto
@object_bp.route('/api/edit/<int:idObjeto>', methods=['GET', 'POST'])
def api_edit_object(idObjeto):
    if request.method == 'GET':
        # Obtener el objeto con el idObjeto
        result = ObjectModel.get_object_by_id(idObjeto)
        
        if not result['success']:
            return redirect(url_for('object.my_objects'))  # Si no se encuentra el objeto, redirigir
        
        # Pasa los datos del objeto al formulario de edición
        return render_template('edit_object.html', objeto=result['data'])
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        url_imagen = request.form['url_imagen']
        url_video = request.form['url_video']
        
        # Actualizar el objeto
        result = ObjectModel.update_object(idObjeto, nombre, descripcion, url_imagen, url_video)
        
        if result['success']:
            return redirect(url_for('object.my_objects'))  # Redirigir después de editar
        else:
            return render_template('edit_object.html', error=result['message'], objeto=request.form)