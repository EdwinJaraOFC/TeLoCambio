from app.database import get_db_connection

class ObjectModel:
    @staticmethod
    def get_objects_by_user(username):
        """
        Recupera todos los objetos asociados al usuario que está en la sesión.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Obtener el idPersona del usuario usando el username
                cursor.execute(
                    "SELECT idPersona FROM usuarios WHERE username = %s",
                    (username,)
                )
                result = cursor.fetchone()

                if not result or not result['idPersona']:
                    return {'success': False, 'message': 'Usuario no tiene información personal asociada.'}

                id_persona = result['idPersona']

                # Recuperar los objetos asociados a idPersona
                cursor.execute(
                    "SELECT * FROM objeto WHERE idPersona = %s AND Estado = 'Disponible'",
                    (id_persona,)
                )
                objects = cursor.fetchall()
                return {'success': True, 'data': objects}
        except Exception as e:
            return {'success': False, 'message': 'Error al recuperar los objetos.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def delete_object_by_id(object_id):
        """
        Elimina un único objeto según su ID.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Verificar si el objeto existe
                cursor.execute(
                    "SELECT COUNT(*) AS count FROM objeto WHERE idObjeto = %s",
                    (object_id,)
                )
                result = cursor.fetchone()

                if not result or result['count'] == 0:
                    return {'success': False, 'message': 'El objeto no existe.'}

                # Eliminar el objeto por su ID
                cursor.execute(
                    "DELETE FROM objeto WHERE idObjeto = %s",
                    (object_id,)
                )
                conn.commit()
                return {'success': True, 'message': 'Objeto eliminado exitosamente.'}
        except Exception as e:
            return {'success': False, 'message': 'Error al eliminar el objeto.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def get_objects_not_by_user(username):
        """
        Recupera todos los objetos que no están asociados al usuario que está en la sesión.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Obtener el idPersona del usuario usando el username
                cursor.execute(
                    "SELECT idPersona FROM usuarios WHERE username = %s",
                    (username,)
                )
                result = cursor.fetchone()

                if not result or not result['idPersona']:
                    return {'success': False, 'message': 'Usuario no tiene información personal asociada.'}

                id_persona = result['idPersona']

                # Recuperar los objetos que no están asociados al idPersona
                cursor.execute(
                    "SELECT * FROM objeto WHERE idPersona != %s AND Estado = 'Disponible'",
                    (id_persona,)
                )
                objects = cursor.fetchall()
                return {'success': True, 'data': objects}
        except Exception as e:
            return {'success': False, 'message': 'Error al recuperar los objetos.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def add_object(username, nombre, descripcion, url_imagen, url_video):
        """
        Agrega un nuevo objeto a la base de datos.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Obtener el idPersona del usuario
                cursor.execute(
                    "SELECT idPersona FROM usuarios WHERE username = %s",
                    (username,)
                )
                result = cursor.fetchone()

                if not result or not result['idPersona']:
                    return {'success': False, 'message': 'Usuario no encontrado.'}

                id_persona = result['idPersona']

                # Insertar el nuevo objeto en la base de datos
                cursor.execute(
                    "INSERT INTO objeto (Nombre, Descripcion, URL_Imagen, URL_Video, idPersona) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (nombre, descripcion, url_imagen, url_video, id_persona)
                )
                conn.commit()
                return {'success': True, 'message': 'Objeto agregado correctamente.'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    # Actualizar un objeto
    @staticmethod
    def update_object(idObjeto, nombre, descripcion, url_imagen, url_video):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE objeto
                    SET Nombre = %s, Descripcion = %s, URL_Imagen = %s, URL_Video = %s
                    WHERE idObjeto = %s
                """, (nombre, descripcion, url_imagen, url_video, idObjeto))
                conn.commit()
                return {'success': True, 'message': 'Objeto actualizado correctamente'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def get_object_by_id(id_objeto):
        """
        Recupera un objeto específico de la base de datos por su ID.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM objeto WHERE idObjeto = %s", (id_objeto,)
                )
                result = cursor.fetchone()

                if result:
                    return {'success': True, 'data': result}
                else:
                    return {'success': False, 'message': 'Objeto no encontrado.'}
        except Exception as e:
            return {'success': False, 'message': 'Error al obtener el objeto.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()