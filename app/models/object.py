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