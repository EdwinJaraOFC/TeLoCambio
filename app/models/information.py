from app.database import get_db_connection

class InformationModel:
    @staticmethod
    def create_information(username, dni, nombre, fecha_nacimiento, correo):
        """
        Crea una nueva entrada en la tabla informacion_persona y actualiza el idPersona del usuario.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Insertar información personal en la tabla informacion_persona
                cursor.execute(
                    "INSERT INTO informacion_Persona (DNI, Nombre, FechaNacimiento, DireccionCorreo) "
                    "VALUES (%s, %s, %s, %s)",
                    (dni, nombre, fecha_nacimiento, correo)
                )
                # Obtener el idPersona generado
                id_persona = cursor.lastrowid

                # Actualizar el idPersona en la tabla usuarios usando el username
                cursor.execute(
                    "UPDATE usuarios SET idPersona = %s WHERE username = %s",
                    (id_persona, username)
                )
                conn.commit()
                return {'success': True, 'message': 'Información registrada exitosamente.'}
        except Exception as e:
            return {'success': False, 'message': 'Error al registrar la información.', 'error': str(e)}
        finally:
            conn.close()

