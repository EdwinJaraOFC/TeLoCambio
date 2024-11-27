from app.database import get_db_connection, get_neo4j_connection

class DirectionModel:
    @staticmethod
    def create_direction(username, direccion, departamento, provincia, distrito):
        """
        Crea una nueva entrada en la tabla direccion_Persona y el nodo correspondiente en Neo4j,
        y establece la relación entre el usuario y su dirección.
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

            # Ahora que la dirección ha sido insertada en MySQL, creamos el nodo en Neo4j
            conn_neo4j = get_neo4j_connection()  # Conexión a Neo4j
            query = f"""
            CREATE (d:Direction_Persona {{
                direccion: '{direccion}',
                departamento: '{departamento}',
                provincia: '{provincia}',
                distrito: '{distrito}'
            }})
            """
            conn_neo4j.execute_query(query)  # Ejecutamos la consulta para crear el nodo de dirección en Neo4j

            # Relacionar el nodo de dirección con el nodo de usuario
            relation_query = f"""
            MATCH (u:User), (d:Direction_Persona)
            WHERE u.username = '{username}' AND d.direccion = '{direccion}'
            CREATE (u)-[:HAS_ADDRESS]->(d)
            """
            conn_neo4j.execute_query(relation_query)

            return {'success': True, 'message': 'Dirección registrada y nodo creado exitosamente.'}

        except Exception as e:
            return {'success': False, 'message': 'Error al registrar la dirección.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()
