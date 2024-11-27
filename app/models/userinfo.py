from app.database import get_db_connection

class UserInfoModel:
    @staticmethod
    def get_user_info_by_username(username):
        """
        Recupera la información personal asociada al usuario dado el username.
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

                # Recuperar los datos de informacion_Persona
                cursor.execute(
                    "SELECT DNI, Nombre, FechaNacimiento, DireccionCorreo, PuntuacionPromedio FROM informacion_Persona WHERE idPersona = %s",
                    (id_persona,)
                )
                user_info = cursor.fetchone()

                return {'success': True, 'data': user_info} if user_info else {'success': False, 'message': 'No se encontraron datos para el usuario.'}
        except Exception as e:
            return {'success': False, 'message': 'Error al recuperar la información personal.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def update_user_info_by_username(username, dni, nombre, fecha_nacimiento, correo_electronico):
        """
        Actualiza la información personal del usuario.
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
                    "UPDATE informacion_Persona SET DNI = %s, Nombre = %s, FechaNacimiento = %s, DireccionCorreo = %s WHERE idPersona = %s",
                    (dni, nombre, fecha_nacimiento, correo_electronico, id_persona)
                )
                conn.commit()
                return {'success': True, 'message': 'Información actualizada correctamente.'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            if conn and conn.open:
                conn.close()