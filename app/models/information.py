from app.database import get_db_connection, get_neo4j_connection

class InformationModel:
    @staticmethod
    def create_information(username, dni, nombre, fecha_nacimiento, correo, puntuacion_promedio=None):
        """
        Crea una nueva entrada en la tabla informacion_persona y crea el nodo en Neo4j.
        También establece la relación entre el usuario y su información.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Insertar información personal en la tabla informacion_persona
                cursor.execute(
                    "INSERT INTO informacion_Persona (DNI, Nombre, FechaNacimiento, DireccionCorreo, PuntuacionPromedio) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (dni, nombre, fecha_nacimiento, correo, puntuacion_promedio)
                )
                # Obtener el idPersona generado
                id_persona = cursor.lastrowid

                # Actualizar el idPersona en la tabla usuarios usando el username
                cursor.execute(
                    "UPDATE usuarios SET idPersona = %s WHERE username = %s",
                    (id_persona, username)
                )
                conn.commit()

            # Ahora que la información ha sido insertada en MySQL, creamos el nodo en Neo4j
            conn_neo4j = get_neo4j_connection()  # Conexión a Neo4j
            query = f"""
            CREATE (i:Information_Persona {{
                dni: '{dni}',
                nombre: '{nombre}',
                fecha_nacimiento: '{fecha_nacimiento}',
                direccion_correo: '{correo}',
                puntuacion_promedio: {puntuacion_promedio if puntuacion_promedio is not None else 'NULL'}
            }})
            """
            conn_neo4j.execute_query(query)  # Ejecutamos la consulta para crear el nodo de información en Neo4j

            # Relacionar el nodo de información con el nodo de usuario
            relation_query = f"""
            MATCH (u:User), (i:Information_Persona)
            WHERE u.username = '{username}' AND i.dni = '{dni}'
            CREATE (u)-[:HAS_INFORMATION]->(i)
            """
            conn_neo4j.execute_query(relation_query)

            return {'success': True, 'message': 'Información registrada y nodo creado exitosamente.'}

        except Exception as e:
            return {'success': False, 'message': 'Error al registrar la información.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()