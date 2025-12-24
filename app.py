import os
import mysql.connector
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps
from dotenv import load_dotenv

load_dotenv()


# CONFIGURACIÓN

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-temporal')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-clave-temporal')

# Configuración de MySQL para Railway
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'ssl_disabled': True  # Railway MySQL no requiere SSL
}


# FUNCIONES DE AYUDA

def get_db_connection():
    """Conectar a la base de datos MySQL"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error conectando a la BD: {e}")
        return None

def token_required(f):
    """Decorador para proteger rutas con JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Obtener token del header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token de acceso requerido'}), 401
        
        try:
            # Decodificar el token
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated


# RUTAS HTML (FRONTEND)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/registro')
def registro_page():
    return render_template('registro.html')

@app.route('/catalogo')
def catalogo_page():
    return render_template('catalogo.html')

@app.route('/busqueda')
def busqueda_page():
    return render_template('busqueda.html')

@app.route('/contacto')
def contacto_page():
    return render_template('contacto.html')

@app.route('/alquiler')
def alquiler_page():
    return render_template('alquiler.html')

@app.route('/compra')
def compra_page():
    return render_template('compra.html')

@app.route('/libro')
def libro_page():
    return render_template('libro.html')


# RUTAS API - AUTENTICACIÓN

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Registrar nuevo usuario"""
    data = request.get_json()
    
    required_fields = ['nombre', 'correo', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Verificar si el correo ya existe
        cursor.execute("SELECT id_usuario FROM Usuarios WHERE correo = %s", (data['correo'],))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'El correo ya está registrado'}), 409
        
        # Hashear contraseña
        hashed_password = generate_password_hash(data['password'])
        
        # Insertar nuevo usuario
        cursor.execute("""
            INSERT INTO Usuarios (nombre, correo, password, fecha_registro)
            VALUES (%s, %s, %s, NOW())
        """, (data['nombre'], data['correo'], hashed_password))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': f'Error en el registro: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Iniciar sesión y generar token JWT"""
    data = request.get_json()
    
    if not all(k in data for k in ['correo', 'password']):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Buscar usuario
        cursor.execute("""
            SELECT id_usuario, nombre, correo, password 
            FROM Usuarios 
            WHERE correo = %s
        """, (data['correo'],))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
        
        # Verificar contraseña
        if not check_password_hash(user['password'], data['password']):
            return jsonify({'error': 'Credenciales incorrectas'}), 401
        
        # Generar token JWT
        token_payload = {
            'user_id': user['id_usuario'],
            'nombre': user['nombre'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(token_payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'mensaje': 'Inicio de sesión exitoso',
            'token': token,
            'user': {
                'id': user['id_usuario'],
                'nombre': user['nombre'],
                'correo': user['correo']
            }
        }), 200
        
    except Exception as e:
        conn.close()
        return jsonify({'error': f'Error en el inicio de sesión: {str(e)}'}), 500


# RUTAS API - LIBROS

@app.route('/api/libros', methods=['GET'])
def get_libros():
    """Obtener todos los libros"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT id_libro, titulo, autor, descripcion, anio_publicacion, 
                   precio, imagen_url, stock_compra, stock_alquiler
            FROM Libros
            ORDER BY titulo
        """)
        
        libros = cursor.fetchall()
        conn.close()
        
        # Convertir decimal a float para JSON
        for libro in libros:
            libro['precio'] = float(libro['precio'])
        
        return jsonify(libros), 200
        
    except Exception as e:
        conn.close()
        return jsonify({'error': f'Error al obtener libros: {str(e)}'}), 500

@app.route('/api/libros/<int:id_libro>', methods=['GET'])
def get_libro(id_libro):
    """Obtener un libro por ID"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT id_libro, titulo, autor, descripcion, anio_publicacion, 
                   precio, imagen_url, stock_compra, stock_alquiler
            FROM Libros
            WHERE id_libro = %s
        """, (id_libro,))
        
        libro = cursor.fetchone()
        conn.close()
        
        if not libro:
            return jsonify({'error': 'Libro no encontrado'}), 404
        
        libro['precio'] = float(libro['precio'])
        return jsonify(libro), 200
        
    except Exception as e:
        conn.close()
        return jsonify({'error': f'Error al obtener libro: {str(e)}'}), 500


# RUTAS API - COMPRAS

@app.route('/api/compras', methods=['POST'])
@token_required
def crear_compra(current_user_id):
    """Crear una nueva compra"""
    data = request.get_json()
    
    required_fields = ['id_libro', 'direccion_envio', 'metodo_pago']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Verificar libro y stock
        cursor.execute("""
            SELECT id_libro, titulo, precio, stock_compra 
            FROM Libros 
            WHERE id_libro = %s
        """, (data['id_libro'],))
        
        libro = cursor.fetchone()
        if not libro:
            conn.close()
            return jsonify({'error': 'Libro no encontrado'}), 404
        
        if libro['stock_compra'] <= 0:
            conn.close()
            return jsonify({'error': 'No hay stock disponible para compra'}), 400
        
        # Insertar compra
        cursor.execute("""
            INSERT INTO Compras (id_usuario, id_libro, precio_pagado, direccion_envio, 
                                 metodo_pago, estado, fecha_compra)
            VALUES (%s, %s, %s, %s, %s, 'pendiente', NOW())
        """, (current_user_id, data['id_libro'], libro['precio'], 
              data['direccion_envio'], data['metodo_pago']))
        
        # Reducir stock
        cursor.execute("""
            UPDATE Libros 
            SET stock_compra = stock_compra - 1 
            WHERE id_libro = %s
        """, (data['id_libro'],))
        
        conn.commit()
        compra_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'mensaje': 'Compra registrada exitosamente',
            'compra_id': compra_id,
            'libro': libro['titulo'],
            'precio': float(libro['precio'])
        }), 201
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': f'Error al crear compra: {str(e)}'}), 500

@app.route('/api/compras/mis-compras', methods=['GET'])
@token_required
def obtener_mis_compras(current_user_id):
    """Obtener compras del usuario actual"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT c.id_compra, c.id_libro, l.titulo, c.fecha_compra, 
                   c.precio_pagado, c.estado, c.metodo_pago, c.direccion_envio
            FROM Compras c
            LEFT JOIN Libros l ON c.id_libro = l.id_libro
            WHERE c.id_usuario = %s
            ORDER BY c.fecha_compra DESC
        """, (current_user_id,))
        
        compras = cursor.fetchall()
        conn.close()
        
        # Convertir fechas y precios
        for compra in compras:
            if compra['fecha_compra']:
                compra['fecha_compra'] = compra['fecha_compra'].isoformat()
            if compra['precio_pagado']:
                compra['precio_pagado'] = float(compra['precio_pagado'])
        
        return jsonify(compras), 200
        
    except Exception as e:
        conn.close()
        return jsonify({'error': f'Error al obtener compras: {str(e)}'}), 500


# RUTAS API - ALQUILERES

@app.route('/api/alquileres', methods=['POST'])
@token_required
def crear_alquiler(current_user_id):
    """Crear un nuevo alquiler"""
    data = request.get_json()
    
    required_fields = ['id_libro', 'dias_alquiler']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    # Validar días de alquiler
    dias = int(data['dias_alquiler'])
    if dias < 1 or dias > 30:
        return jsonify({'error': 'Los días de alquiler deben estar entre 1 y 30'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Verificar libro y stock
        cursor.execute("""
            SELECT id_libro, titulo, stock_alquiler 
            FROM Libros 
            WHERE id_libro = %s
        """, (data['id_libro'],))
        
        libro = cursor.fetchone()
        if not libro:
            conn.close()
            return jsonify({'error': 'Libro no encontrado'}), 404
        
        if libro['stock_alquiler'] <= 0:
            conn.close()
            return jsonify({'error': 'No hay stock disponible para alquiler'}), 400
        
        # Calcular fechas
        fecha_inicio = datetime.now()
        fecha_devolucion = fecha_inicio + timedelta(days=dias)
        
        # Insertar alquiler
        cursor.execute("""
            INSERT INTO Alquileres (id_usuario, id_libro, dias_alquiler, 
                                    fecha_inicio, fecha_devolucion, estado)
            VALUES (%s, %s, %s, %s, %s, 'activo')
        """, (current_user_id, data['id_libro'], dias, 
              fecha_inicio, fecha_devolucion))
        
        # Reducir stock
        cursor.execute("""
            UPDATE Libros 
            SET stock_alquiler = stock_alquiler - 1 
            WHERE id_libro = %s
        """, (data['id_libro'],))
        
        conn.commit()
        alquiler_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'mensaje': 'Alquiler registrado exitosamente',
            'alquiler_id': alquiler_id,
            'libro': libro['titulo'],
            'dias_alquiler': dias,
            'fecha_devolucion': fecha_devolucion.isoformat()
        }), 201
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': f'Error al crear alquiler: {str(e)}'}), 500

@app.route('/api/alquileres/mis-alquileres', methods=['GET'])
@token_required
def obtener_mis_alquileres(current_user_id):
    """Obtener alquileres del usuario actual"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT a.id_alquiler, a.id_libro, l.titulo, a.dias_alquiler, 
                   a.fecha_inicio, a.fecha_devolucion, a.estado
            FROM Alquileres a
            LEFT JOIN Libros l ON a.id_libro = l.id_libro
            WHERE a.id_usuario = %s
            ORDER BY a.fecha_inicio DESC
        """, (current_user_id,))
        
        alquileres = cursor.fetchall()
        conn.close()
        
        # Convertir fechas
        for alquiler in alquileres:
            if alquiler['fecha_inicio']:
                alquiler['fecha_inicio'] = alquiler['fecha_inicio'].isoformat()
            if alquiler['fecha_devolucion']:
                alquiler['fecha_devolucion'] = alquiler['fecha_devolucion'].isoformat()
        
        return jsonify(alquileres), 200
        
    except Exception as e:
        conn.close()
        return jsonify({'error': f'Error al obtener alquileres: {str(e)}'}), 500


# RUTAS API - CONTACTO

@app.route('/api/contacto', methods=['POST'])
def enviar_contacto():
    """Enviar mensaje de contacto"""
    data = request.get_json()
    
    required_fields = ['nombre', 'correo', 'mensaje']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO Contactos (nombre, correo, mensaje, fecha_envio, leido)
            VALUES (%s, %s, %s, NOW(), FALSE)
        """, (data['nombre'], data['correo'], data['mensaje']))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'mensaje': 'Mensaje enviado correctamente. ¡Gracias por contactarnos!'
        }), 201
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': f'Error al enviar mensaje: {str(e)}'}), 500


# RUTAS DE PRUEBA

@app.route('/api/test', methods=['GET'])
def test_api():
    """Ruta de prueba para verificar que el API funciona"""
    return jsonify({
        'mensaje': 'API funcionando correctamente',
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/test-db', methods=['GET'])
def test_db():
    """Ruta de prueba para verificar conexión a BD"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT COUNT(*) as total FROM Libros")
        result = cursor.fetchone()
        
        cursor.execute("SELECT COUNT(*) as total FROM Usuarios")
        usuarios = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            'status': 'BD conectada correctamente',
            'total_libros': result['total'],
            'total_usuarios': usuarios['total']
        }), 200
        
    except Exception as e:
        conn.close()
        return jsonify({'error': f'Error en consulta BD: {str(e)}'}), 500


# CONFIGURACIÓN DE STATIC FILES

@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir archivos estáticos"""
    return app.send_static_file(filename)


# INICIAR APLICACIÓN

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)