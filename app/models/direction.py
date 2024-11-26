from app.database import get_db_connection

class DirectionModel:
    @staticmethod
    def create_direction(username, direccion, departamento, provincia, distrito):
        """
        Crea una nueva entrada en la tabla direccion_Persona asociada al usuario.
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

                # Insertar dirección en la tabla direccion_Persona
                cursor.execute(
                    "INSERT INTO direccion_Persona (idPersona, Direccion, Provincia, Departamento, Distrito) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (id_persona, direccion, provincia, departamento, distrito)
                )
                conn.commit()
                return {'success': True, 'message': 'Dirección registrada exitosamente.'}
        except Exception as e:
            return {'success': False, 'message': 'Error al registrar la dirección.', 'error': str(e)}
        finally:
            conn.close()
