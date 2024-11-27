import pymysql
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db_connection
from app.database import get_neo4j_connection  # Usamos la conexión a Neo4j

class UserModel(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def create_user(username, password):
        """Crea un nuevo usuario en MySQL y en Neo4j"""
        if not username or not password:
            return {'success': False, 'message': 'El nombre de usuario y la contraseña son obligatorios.'}

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Verificar si el nombre de usuario ya existe
                cursor.execute("SELECT COUNT(*) AS count FROM usuarios WHERE username = %s", (username,))
                user_count = cursor.fetchone()['count']
                if user_count > 0:
                    return {'success': False, 'message': 'El nombre de usuario ya existe.'}

                # Hashear la contraseña
                hashed_password = generate_password_hash(password)

                # Insertar el nuevo usuario en MySQL
                cursor.execute(
                    "INSERT INTO usuarios (username, password) VALUES (%s, %s)",
                    (username, hashed_password)
                )
                conn.commit()

                # Obtener el id del usuario recién insertado
                cursor.execute("SELECT idUsuario FROM usuarios WHERE username = %s", (username,))
                user = cursor.fetchone()
                user_id = user['idUsuario']

                # Crear el nodo de usuario en Neo4j
                UserModel.create_user_node_in_neo4j(user_id, username)  # Llamada para crear el nodo en Neo4j

            return {'success': True, 'message': 'Usuario y nodo creado exitosamente.'}
        except pymysql.MySQLError as e:
            print(f"Error en la base de datos MySQL: {str(e)}")
            return {'success': False, 'message': 'Error en la base de datos MySQL.', 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def create_user_node_in_neo4j(user_id, username):
        """Crea un nodo de Usuario en Neo4j"""
        conn = get_neo4j_connection()  # Conexión a Neo4j
        try:
            query = """
            CREATE (u:User {id: $user_id, username: $username})
            """
            parameters = {'user_id': user_id, 'username': username}
            # Ejecutar la consulta para crear el nodo en Neo4j
            conn.execute_query(query, parameters)
            print(f"Nodo de usuario con id {user_id} y username {username} creado en Neo4j.")
        except Exception as e:
            print(f"Error al crear el nodo de usuario en Neo4j: {e}")
        finally:
            conn.close()

    @staticmethod
    def get_user_by_username(username):
        """Busca un usuario por nombre de usuario"""
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
                user = cursor.fetchone()
                if user:
                    return UserModel(user['idUsuario'], user['username'], user['password'])
        except Exception as e:
            print(f"Error al buscar el usuario: {e}")
            return None
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def get_user_by_id(id):
        """Busca un usuario por ID"""
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE idUsuario = %s", (id,))
                user = cursor.fetchone()
                if user:
                    return UserModel(user['idUsuario'], user['username'], user['password'])
        except Exception as e:
            print(f"Error al buscar el usuario por ID: {e}")
            return None
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def authenticate_user(username, password):
        """Valida las credenciales del usuario"""
        user = UserModel.get_user_by_username(username)
        if not user:
            return {'success': False, 'message': 'Usuario no encontrado.'}

        # Verificar la contraseña
        if not check_password_hash(user.password, password):
            return {'success': False, 'message': 'Contraseña incorrecta.'}

        return {'success': True, 'message': 'Inicio de sesión exitoso.', 'user': user}
