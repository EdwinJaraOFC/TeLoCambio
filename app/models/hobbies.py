from app.database import get_db_connection

class HobbiesModel:
    @staticmethod
    def create_hobbies(username, pasatiempos, gustos_musicales, peliculas_favoritas):
        """
        Crea una nueva entrada en la tabla gustos_Persona asociada al usuario.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Verificar el idPersona del usuario desde la tabla usuarios
                cursor.execute(
                    "SELECT idPersona FROM usuarios WHERE username = %s",
                    (username,)
                )
                result = cursor.fetchone()

                if not result or not result['idPersona']:
                    return {'success': False, 'message': 'Usuario no tiene información personal asociada.'}

                id_persona = result['idPersona']

                # Insertar gustos en la tabla gustos_Persona
                cursor.execute(
                    "INSERT INTO gustos_Persona (idPersona, Pasatiempos, GustosMusicales, PeliculasFavoritas) "
                    "VALUES (%s, %s, %s, %s)",
                    (id_persona, pasatiempos, gustos_musicales, peliculas_favoritas)
                )
                conn.commit()
                return {'success': True, 'message': 'Gustos registrados exitosamente.'}
        except Exception as e:
            return {'success': False, 'message': 'Error al registrar los gustos.', 'error': str(e)}
        finally:
            conn.close()
