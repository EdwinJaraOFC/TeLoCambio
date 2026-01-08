# 🔄 TeLoCambio

**TeLoCambio** es una plataforma web para el **intercambio de objetos** entre usuarios.  
Permite registrar, ofrecer y solicitar intercambios, además de incluir:  
- Sistema de **valoraciones** de intercambios.  
- **Notificaciones** sobre solicitudes y actualizaciones

La plataforma combina **bases de datos relacionales y no relacionales**:  
- **MySQL** para datos estructurados.  
- **Neo4j** para gestionar relaciones complejas entre usuarios y objetos.  

También cuenta con una **API RESTful** para la gestión de usuarios y objetos.

---

## 🛠️ Tecnologías utilizadas

- **Backend**: Flask (Python)  
- **Base de datos relacional**: MySQL  
- **Base de datos no relacional**: Neo4j  
- **Autenticación**: Flask-Login  
- **Frontend**: HTML, CSS, Bootstrap  
- **Pruebas**: pytest  

---

## 📋 Requisitos

- Python 3.x  
- MySQL  
- Neo4j  
- pip (para instalar dependencias)  

---

## ⚙️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/EdwinJaraOFC/TeLoCambio.git
cd TeLoCambio
```

### 2. Crear un entorno virtual
```bash
python -m venv venv
source venv/bin/activate   # Linux/MacOS
venv\Scripts\activate      # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar archivo `.env`
Ejemplo de configuración:

```env
# MySQL
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_DB=te_locambio
MYSQL_PORT=3306

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=tu_contraseña

# Flask
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=una_clave_secreta
```

### 5. Crear las bases de datos
- Ejecutar scripts de creación de tablas en **MySQL**.  
- Configurar nodos y relaciones en **Neo4j**.  

### 6. Ejecutar la aplicación
```bash
python run.py
```
Disponible en: [http://127.0.0.1:5000](http://127.0.0.1:5000)  

---

## 🚀 Uso

### Funcionalidades principales
- **Registro de usuario** con datos personales (DNI, nombre, fecha de nacimiento, etc.).  
- **Intercambio de objetos**: ofrecer y solicitar.  
- **Valoraciones** después de completar un intercambio.  
- **Notificaciones** de solicitudes y confirmaciones.  
- **Gestión de inventario**: agregar, editar y eliminar objetos.  

### Rutas principales de la API

**Usuarios**  
- `POST /api/usuarios` → Crear usuario  
- `POST /api/login` → Iniciar sesión  
- `GET /api/usuarios` → Listar usuarios  
- `DELETE /api/usuarios/{idUsuario}` → Eliminar usuario  

**Objetos**  
- `POST /api/objetos` → Registrar objeto  
- `PATCH /api/objetos/{idObjeto}/estado` → Cambiar estado  

**Intercambios**  
- `POST /api/intercambios` → Crear intercambio  
- `PATCH /api/intercambios/{idIntercambio}/confirmar` → Confirmar  

**Valoraciones**  
- `POST /api/valoraciones` → Registrar valoración  

**Notificaciones**  
- `POST /api/notificaciones` → Registrar notificación  

---

## 📂 Estructura del proyecto
```plaintext
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
```

---

## ✅ Pruebas automáticas
Este proyecto incluye pruebas con **unittest** y **pytest**.  
Ejecuta las pruebas con:  

```bash
pytest tests/test_api.py
```

---

## 🤝 Contribuciones
Las contribuciones son bienvenidas.  
Abre un **issue** o envía un **pull request** con tus mejoras.  

---

## 📄 Licencia
Este proyecto está bajo la **Licencia MIT**.  
Consulta el archivo `LICENSE` para más detalles.  
