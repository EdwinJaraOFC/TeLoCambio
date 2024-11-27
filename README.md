# TeLoCambio

**TeLoCambio** es una plataforma de intercambio de objetos basada en web que permite a los usuarios registrar, ofrecer y solicitar intercambios de objetos con otros usuarios. El sistema también incluye un sistema de valoraciones para los intercambios realizados y notificaciones sobre el estado de las solicitudes.

Este proyecto utiliza una arquitectura de base de datos relacional (MySQL) y no relacional (Neo4j), lo que permite gestionar tanto datos estructurados como relaciones complejas entre los usuarios y los objetos. El sistema también está respaldado por una API RESTful para la interacción con la base de datos y la gestión de usuarios.

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos Relacional**: MySQL
- **Base de Datos No Relacional**: Neo4j
- **Autenticación**: Flask-Login (para la gestión de sesiones de usuario)
- **Frontend**: HTML, CSS, Bootstrap
- **Pruebas**: unittest, pytest

## Requisitos

Para ejecutar este proyecto, necesitas tener instalados los siguientes programas:

- Python 3.x
- MySQL
- Neo4j
- pip (para instalar las dependencias de Python)

## Instalación

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/EdwinJaraOFC/TeLoCambio.git
cd TeLoCambio
Paso 2: Crear un entorno virtual
Es recomendable crear un entorno virtual para gestionar las dependencias del proyecto.

bash
Copiar código
python -m venv venv
source venv/bin/activate  # Para Linux/MacOS
venv\Scripts\activate  # Para Windows
Paso 3: Instalar las dependencias
Instala las dependencias necesarias usando pip:

bash
Copiar código
pip install -r requirements.txt
Paso 4: Configurar el archivo .env
Crea un archivo .env en la raíz del proyecto para almacenar las configuraciones necesarias para conectar la base de datos y otros servicios. Aquí hay un ejemplo de cómo debería lucir:

makefile
Copiar código
# Configuración de MySQL
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_DB=te_locambio
MYSQL_PORT=3306

# Configuración de Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=tu_contraseña

# Configuración de Flask
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=una_clave_secreta
Paso 5: Crear las bases de datos
Antes de ejecutar la aplicación, asegúrate de tener las bases de datos de MySQL y Neo4j configuradas. Ejecuta los scripts de creación de tablas para MySQL y configura Neo4j para poder conectar los nodos.

Paso 6: Ejecutar la aplicación
Una vez configurado todo, puedes iniciar la aplicación de Flask:

bash
Copiar código
python run.py
La aplicación estará disponible en http://127.0.0.1:5000.

Uso
Funcionalidades principales
Registro de Usuario: Los usuarios pueden registrarse proporcionando un nombre de usuario, contraseña y detalles adicionales (DNI, nombre, fecha de nacimiento, etc.).
Intercambio de Objetos: Los usuarios pueden ofrecer objetos y solicitar intercambios con otros usuarios.
Valoración de Intercambios: Después de completar un intercambio, los usuarios pueden calificarlo.
Notificaciones: Los usuarios reciben notificaciones cuando se realiza una solicitud de intercambio o cuando se completa un intercambio.
Gestión de Objetos: Los usuarios pueden agregar, editar y eliminar objetos de su inventario.
Rutas de la API
Usuarios
POST /api/usuarios: Crear un nuevo usuario.
POST /api/login: Iniciar sesión con un usuario registrado.
GET /api/usuarios: Obtener una lista de todos los usuarios.
DELETE /api/usuarios/{idUsuario}: Eliminar un usuario y sus datos relacionados.
Objetos
POST /api/objetos: Registrar un objeto ofrecido por un usuario.
PATCH /api/objetos/{idObjeto}/estado: Actualizar el estado de un objeto (Disponible, En Proceso, Intercambiado).
Intercambios
POST /api/intercambios: Registrar un intercambio entre dos usuarios.
PATCH /api/intercambios/{idIntercambio}/confirmar: Confirmar un intercambio.
Valoraciones
POST /api/valoraciones: Registrar una valoración sobre un intercambio.
Notificaciones
POST /api/notificaciones: Registrar una notificación de intercambio para un usuario.
Estructura del Proyecto
arduino
Copiar código
TeLoCambio/
├── app/
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── object_routes.py
│   │   ├── exchange_routes.py
│   │   └── user_routes.py
│   ├── models/
│   │   ├── user.py
│   │   ├── object.py
│   │   ├── exchange.py
│   │   └── notification.py
│   ├── database/
│   │   ├── init_relational_db.py
│   │   ├── init_neo4j_db.py
│   ├── templates/
│   ├── static/
│   └── __init__.py
├── config/
│   ├── config.py
├── tests/
│   ├── test_api.py
├── run.py
└── requirements.txt
Pruebas Automáticas
Este proyecto incluye pruebas automáticas utilizando unittest y pytest. Las pruebas están diseñadas para validar las rutas de la API y asegurar que los datos se gestionen correctamente en la base de datos.

Para ejecutar las pruebas:

bash
Copiar código
pytest tests/test_api.py
Contribuciones
Las contribuciones son bienvenidas. Si tienes alguna sugerencia, mejora o corrección, por favor abre un issue o envía un pull request.

Licencia
Este proyecto está bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.

markdown
Copiar código

Este `README.md` incluye toda la información relevante para tu proyecto **TeLoCambio**, organizada de 
