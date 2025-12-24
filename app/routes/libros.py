from flask import Blueprint, jsonify
from ..utils.db import get_db_connection  # ✅ Importa la función de conexión

libros_bp = Blueprint('libros', __name__)

@libros_bp.route('/', methods=['GET'])
def get_all_libros():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión a la BD"}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_libro, titulo, autor, anio_publicacion, precio, 
               imagen_url, descripcion, stock_compra, stock_alquiler
        FROM Libros
    """)
    libros = cursor.fetchall()
    conn.close()
    
    # Asegurar que el precio sea un float
    for libro in libros:
        libro['precio'] = float(libro['precio'])
    
    return jsonify(libros), 200  # ✅ Devuelve la lista directamente


@libros_bp.route('/<int:id>', methods=['GET'])
def get_libro(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión a la BD"}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_libro, titulo, autor, anio_publicacion, precio, 
               imagen_url, descripcion, stock_compra, stock_alquiler
        FROM Libros 
        WHERE id_libro = %s
    """, (id,))
    libro = cursor.fetchone()
    conn.close()
    
    if not libro:
        return jsonify({"error": "Libro no encontrado"}), 404
    
    libro['precio'] = float(libro['precio'])
    return jsonify(libro), 200