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
JWTManager(app)

# Rutas para tus páginas HTML
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
    return "¡El servidor funciona! Prueba /login, /catalogo, etc."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)