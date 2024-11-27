from app.database import get_db_connection
from datetime import datetime

class ExchangeModel:
    @staticmethod
    def get_all_exchanges():
        """Recupera todos los intercambios de la base de datos."""
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Obtener todos los intercambios
                cursor.execute("""
                    SELECT idIntercambio, idPersona1, idObjeto1, idPersona2, idObjeto2, Fecha, Estado 
                    FROM Intercambio
                """)
                intercambios = cursor.fetchall()
                return intercambios
        except Exception as e:
            return {'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    # Otras funciones como eliminar intercambio, etc. pueden ir aquí si se necesitan en el futuro
    @staticmethod
    def get_completed_exchanges():
        """
        Recupera todos los intercambios completados.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM Intercambio WHERE Estado = 'Completado'"
                )
                intercambios = cursor.fetchall()
                return intercambios
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def get_pending_exchanges():
        """
        Recupera todos los intercambios que están en estado 'Pendiente'.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM Intercambio WHERE Estado = 'Pendiente'"
                )
                intercambios = cursor.fetchall()
                return intercambios
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            if conn and conn.open:
                conn.close()

    @staticmethod
    def convert_date_format(date_str):
        """
        Convierte una fecha al formato aaaa-mm-dd.
        """
        try:
            # Intentar convertir la fecha al formato correcto
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")  # Suponemos que el formato ingresado es dd-mm-aaaa
            return date_obj.strftime("%Y-%m-%d")  # Convertimos a aaaa-mm-dd
        except ValueError:
            return None  # Retorna None si la fecha no tiene el formato esperado
        
    @staticmethod
    def create_exchange(id_persona1, id_objeto1, id_persona2, id_objeto2, fecha, estado):
        """
        Crea un intercambio con el estado proporcionado.
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Intercambio (idPersona1, idObjeto1, idPersona2, idObjeto2, Fecha, Estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_persona1, id_objeto1, id_persona2, id_objeto2, fecha, estado))
            conn.commit()
            return {'success': True}
        except Exception as e:
            print(f"Error al crear el intercambio: {e}")
            return {'success': False, 'error': str(e)}
        finally:
            if conn and conn.open:
                conn.close()