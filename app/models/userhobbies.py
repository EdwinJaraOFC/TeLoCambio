from app.database import get_db_connection

class UserHobbiesModel:
    @staticmethod
    def get_user_hobbies_by_username(username):
        """
        Recupera los pasatiempos, gustos musicales y películas favoritas del usuario dado su username.
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
                    return {'success': False, 'message': 'Usuario no tiene hobbies asociados.'}

                id_persona = result['idPersona']

                # Recuperar los datos de hobbies del usuario
                cursor.execute(
                    "SELECT Pasatiempos, GustosMusicales, PeliculasFavoritas FROM gustos_Persona WHERE idPersona = %s",
                    (id_persona,)
                )
                user_hobbies = cursor.fetchone()

                return {'success': True, 'data': user_hobbies} if user_hobbies else {'success': False, 'message': 'No se encontraron datos de hobbies para el usuario.'}
        except Exception as e:
            return {'success': False, 'message': 'Error al recuperar los hobbies.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def update_user_hobbies_by_username(username, pasatiempos, gustos_musicales, peliculas_favoritas):
        """
        Actualiza los pasatiempos, gustos musicales y películas favoritas del usuario por su nombre de usuario.
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

                # Actualizar los hobbies del usuario en la base de datos
                cursor.execute(
                    "UPDATE gustos_Persona SET Pasatiempos = %s, GustosMusicales = %s, PeliculasFavoritas = %s WHERE idPersona = %s",
                    (pasatiempos, gustos_musicales, peliculas_favoritas, id_persona)
                )
                conn.commit()
                return {'success': True, 'message': 'Gustos actualizados correctamente.'}
        except Exception as e:
            return {'success': False, 'message': 'Error al actualizar los gustos.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()
