# app/routes/exchanges_routes.py

from flask import Blueprint, render_template, jsonify, flash, request, redirect, url_for
from app.models.exchanges import ExchangeModel
from datetime import datetime

# Crear el blueprint para intercambios
exchanges_bp = Blueprint('exchange', __name__)

# Ruta API: obtiene los intercambios como JSON
@exchanges_bp.route('/api/all', methods=['GET'])
def api_get_all_exchanges():
    """Recupera todos los intercambios como JSON."""
    try:
        intercambios = ExchangeModel.get_all_exchanges()  # Obtener todos los intercambios
        if 'error' in intercambios:
            return jsonify({'error': intercambios['error']}), 500  # Si hubo un error
        return jsonify(intercambios)  # Devolver los intercambios como JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta vista: muestra la página con todos los intercambios
@exchanges_bp.route('/all', methods=['GET'])
def all_exchanges():
    """Muestra todos los intercambios en una página web."""
    try:
        intercambios = ExchangeModel.get_all_exchanges()  # Obtener todos los intercambios
        if 'error' in intercambios:
            return jsonify({'error': intercambios['error']}), 500  # Si hubo un error
        return render_template('all_exchanges.html', intercambios=intercambios)  # Pasar los intercambios a la plantilla
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener intercambios completados (API)
@exchanges_bp.route('/api/completed', methods=['GET'])
def api_get_complete_exchanges():
    # Obtiene los intercambios completados desde el modelo
    result = ExchangeModel.get_completed_exchanges()
    if result.get('success'):
        return jsonify(result['data']), 200
    return jsonify(result), 400

# Ruta para la página de intercambios completados
@exchanges_bp.route('/completed', methods=['GET'])
def complete_exchanges():
    # Obtiene los intercambios completados desde el modelo
    exchanges = ExchangeModel.get_completed_exchanges()
    return render_template('complete_exchanges.html', intercambios=exchanges)

# Ruta para la página de intercambios pendientes
@exchanges_bp.route('/pending-exchanges', methods=['GET'])
def pending_exchanges_page():
    """
    Renderiza la página con la tabla de intercambios pendientes.
    """
    intercambios = ExchangeModel.get_pending_exchanges()  # Obtener los intercambios pendientes desde el modelo
    return render_template('pending_exchanges.html', intercambios=intercambios)

@exchanges_bp.route('/apply-exchange/<int:id_objeto>', methods=['GET', 'POST'])
def apply_exchange(id_objeto):
    """
    Muestra el formulario para aplicar un intercambio y maneja la creación del intercambio.
    """
    if request.method == 'POST':
        # Obtener los datos del formulario
        id_objeto1 = id_objeto  # El objeto que el usuario solicita
        id_objeto2 = request.form['id_objeto2']  # El objeto que el usuario está ofreciendo
        id_persona1 = request.form['id_persona1']  # ID de la persona logueada, ingresado manualmente
        id_persona2 = request.form['id_persona2']  # ID del dueño del objeto solicitado, ingresado manualmente
        fecha = request.form['fecha']  # Fecha de la solicitud, obtenida del formulario
        estado = request.form['estado']  # El estado que se elige para el intercambio

        # Convertir la fecha al formato correcto (aaaa-mm-dd)
        fecha_formateada = ExchangeModel.convert_date_format(fecha)

        # Verificar si la fecha es válida
        if not fecha_formateada:
            flash('Fecha inválida. Por favor ingrese una fecha válida (dd-mm-aaaa).', 'error')
            return redirect(request.url)

        # Crear el intercambio con el estado proporcionado
        result = ExchangeModel.create_exchange(id_persona1, id_objeto1, id_persona2, id_objeto2, fecha_formateada, estado)

        if result['success']:
            flash('Intercambio aplicado con éxito', 'success')
            return redirect(url_for('exchange.all_exchanges'))  # Redirigir a la página de intercambios pendientes
        else:
            flash('Error al aplicar el intercambio', 'error')

    # Si es GET, obtenemos los datos y mostramos el formulario
    return render_template('request_exchange.html', id_objeto=id_objeto)

