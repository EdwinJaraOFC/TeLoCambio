from app.database import get_db_connection, get_neo4j_connection

class HobbiesModel:
    @staticmethod
    def create_hobbies(username, pasatiempos, gustos_musicales, peliculas_favoritas):
        """
        Crea una nueva entrada en la tabla gustos_Persona, crea un nodo en Neo4j y
        establece la relación con el usuario.
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

                # Insertar los gustos en la tabla gustos_Persona
                cursor.execute(
                    "INSERT INTO gustos_Persona (idPersona, Pasatiempos, GustosMusicales, PeliculasFavoritas) "
                    "VALUES (%s, %s, %s, %s)",
                    (id_persona, pasatiempos, gustos_musicales, peliculas_favoritas)
                )
                conn.commit()

            # Ahora que la información de los gustos ha sido insertada en MySQL, creamos el nodo en Neo4j
            conn_neo4j = get_neo4j_connection()  # Conexión a Neo4j
            query = f"""
            CREATE (g:Gustos_Persona {{
                pasatiempos: '{pasatiempos}',
                gustos_musicales: '{gustos_musicales}',
                peliculas_favoritas: '{peliculas_favoritas}'
            }})
            """
            conn_neo4j.execute_query(query)  # Ejecutamos la consulta para crear el nodo de gustos en Neo4j

            # Relacionar el nodo de gustos con el nodo de usuario
            relation_query = f"""
            MATCH (u:User), (g:Gustos_Persona)
            WHERE u.username = '{username}' AND g.pasatiempos = '{pasatiempos}' 
            CREATE (u)-[:HAS_GUSTOS]->(g)
            """
            conn_neo4j.execute_query(relation_query)

            return {'success': True, 'message': 'Gustos registrados y nodo creado exitosamente.'}

        except Exception as e:
            return {'success': False, 'message': 'Error al registrar los gustos.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()
