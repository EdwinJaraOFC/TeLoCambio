from app.database import get_db_connection

class UserDirectionModel:
    @staticmethod
    def get_user_direction_by_username(username):
        """
        Recupera la dirección asociada al usuario dado el username.
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
                    return {'success': False, 'message': 'Usuario no tiene dirección asociada.'}

                id_persona = result['idPersona']

                # Recuperar los datos de direccion_Persona
                cursor.execute(
                    "SELECT Direccion, Departamento, Provincia, Distrito FROM direccion_Persona WHERE idPersona = %s",
                    (id_persona,)
                )
                user_direction = cursor.fetchone()

                return {'success': True, 'data': user_direction} if user_direction else {'success': False, 'message': 'No se encontraron datos de dirección para el usuario.'}
        except Exception as e:
            return {'success': False, 'message': 'Error al recuperar la dirección.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def update_user_direction_by_username(username, direccion, departamento, provincia, distrito):
        """
        Actualiza la dirección del usuario.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT idPersona FROM usuarios WHERE username = %s", (username,)
                )
                result = cursor.fetchone()

                if not result or not result['idPersona']:
                    return {'success': False, 'message': 'Usuario no encontrado.'}

                id_persona = result['idPersona']

                cursor.execute(
                    "UPDATE direccion_Persona SET Direccion = %s, Departamento = %s, Provincia = %s, Distrito = %s WHERE idPersona = %s",
                    (direccion, departamento, provincia, distrito, id_persona)
                )
                conn.commit()
                return {'success': True, 'message': 'Dirección actualizada correctamente.'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            if conn and conn.open:
                conn.close()