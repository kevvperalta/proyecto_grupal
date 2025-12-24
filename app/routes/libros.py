from flask import Blueprint, jsonify
from ..utils import db

libros_bp = Blueprint('libros', __name__)

@libros_bp.route('/', methods=['GET'])
def get_all_libros():
    libros = Libro.query.all()
    
    return jsonify([{
        "id_libro": l.id_libro,
        "titulo": l.titulo,
        "autor": l.autor,
        "anio_publicacion": l.anio_publicacion,
        "precio": float(l.precio),
        "imagen_url": l.imagen_url,
        "descripcion": l.descripcion,
        "stock_compra": l.stock_compra,
        "stock_alquiler": l.stock_alquiler
    } for l in libros]), 200


@libros_bp.route('/<int:id>', methods=['GET'])
def get_libro(id):
    libro = Libro.query.get_or_404(id)
    
    return jsonify({
        "id_libro": libro.id_libro,
        "titulo": libro.titulo,
        "autor": libro.autor,
        "anio_publicacion": libro.anio_publicacion,
        "precio": float(libro.precio),
        "imagen_url": libro.imagen_url,
        "descripcion": libro.descripcion,
        "stock_compra": libro.stock_compra,
        "stock_alquiler": libro.stock_alquiler
    }), 200