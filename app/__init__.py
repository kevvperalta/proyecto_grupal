# app/__init__.py - VERSIÓN COMPLETA Y CORREGIDA
from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)

# Configuración EXACTA para que busque templates y static en la raíz del proyecto
# (donde están tus carpetas templates/ y static/)
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # Sube un nivel a la raíz
app.template_folder = os.path.join(BASE_DIR, 'templates')
app.static_folder = os.path.join(BASE_DIR, 'static')

CORS(app)

# Configurar JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'clave-secreta-temporal')
JWTManager(app)

# ============================================
# RUTAS PARA PÁGINAS HTML (FRONTEND)
# ============================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/busqueda')
def busqueda():
    return render_template('busqueda.html')

@app.route('/alquiler')
def alquiler():
    return render_template('alquiler.html')

@app.route('/compra')
def compra():
    return render_template('compra.html')

@app.route('/libro')
def libro():
    return render_template('libro.html')

# Ruta de prueba para confirmar que el servidor responde
@app.route('/test')
def test():
    return "¡El servidor funciona! Prueba /login, /catalogo, /api/libros, etc."

# Ruta de prueba para la base de datos
@app.route('/test-db')
def test_db():
    try:
        from .utils.db import get_db_connection
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as total FROM Libros")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return f" Base de datos funcionando. Libros en BD: {result['total']}"
        else:
            return " No se pudo conectar a la base de datos"
    except Exception as e:
        return f" Error en base de datos: {str(e)}"

# Ruta para ver variables de entorno (solo muestra, no contraseñas)
@app.route('/test-env')
def test_env():
    import os
    env_vars = ['DB_HOST', 'DB_USER', 'DB_NAME', 'DB_PORT']
    results = []
    for var in env_vars:
        if var in os.environ:
            results.append(f"{var}: {os.environ[var]}")
        else:
            results.append(f"{var}: NO DEFINIDA")
    
    # Verificar JWT
    if 'JWT_SECRET_KEY' in os.environ:
        results.append("JWT_SECRET_KEY: DEFINIDA (oculta por seguridad)")
    else:
        results.append("JWT_SECRET_KEY: NO DEFINIDA")
    
    return "<br>".join(results)

# ============================================
# REGISTRAR BLUEPRINTS (API/BACKEND)
# ============================================

# Importar Blueprints
from .routes.auth import auth_bp
from .routes.libros import libros_bp
from .routes.alquileres import alquileres_bp
from .routes.compras import compras_bp
from .routes.contacto import contacto_bp

# Registrar Blueprints con prefijo /api
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(libros_bp, url_prefix='/api/libros')
app.register_blueprint(alquileres_bp, url_prefix='/api/alquileres')
app.register_blueprint(compras_bp, url_prefix='/api/compras')
app.register_blueprint(contacto_bp, url_prefix='/api/contacto')

# ============================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)