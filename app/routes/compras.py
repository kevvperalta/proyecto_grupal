from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.db import get_db_connection  # ← Usa esta conexión
from datetime import datetime

compras_bp = Blueprint('compras', __name__)

@compras_bp.route('/', methods=['POST'])
@jwt_required()
def crear_compra():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    required_fields = ['id_libro', 'direccion_envio', 'metodo_pago']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión a la BD"}), 500

    cursor = conn.cursor(dictionary=True)

    # Verificar si el libro existe y tiene stock
    cursor.execute("SELECT * FROM Libros WHERE id_libro = %s", (data['id_libro'],))
    libro = cursor.fetchone()
    if not libro:
        conn.close()
        return jsonify({"error": "Libro no encontrado"}), 404

    if libro['stock_compra'] <= 0:
        conn.close()
        return jsonify({"error": "No hay stock disponible"}), 400

    try:
        # Insertar compra
        cursor.execute("""
            INSERT INTO Compras 
            (id_usuario, id_libro, precio_pagado, direccion_envio, metodo_pago, estado, fecha_compra)
            VALUES (%s, %s, %s, %s, %s, 'pendiente', %s)
        """, (
            current_user_id,
            data['id_libro'],
            libro['precio'],
            data['direccion_envio'],
            data['metodo_pago'],
            datetime.utcnow()
        ))

        # Reducir stock
        cursor.execute("UPDATE Libros SET stock_compra = stock_compra - 1 WHERE id_libro = %s", (data['id_libro'],))

        conn.commit()
        compra_id = cursor.lastrowid

        conn.close()

        return jsonify({
            "mensaje": "Compra registrada exitosamente",
            "compra_id": compra_id,
            "libro": libro['titulo'],
            "precio": float(libro['precio'])
        }), 201

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": str(e)}), 500


@compras_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_mis_compras():
    current_user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id_compra, c.id_libro, l.titulo as titulo_libro, c.fecha_compra, 
               c.precio_pagado, c.estado, c.metodo_pago, c.direccion_envio
        FROM Compras c
        LEFT JOIN Libros l ON c.id_libro = l.id_libro
        WHERE c.id_usuario = %s
    """, (current_user_id,))
    
    compras = cursor.fetchall()
    conn.close()

    return jsonify([{
        "id_compra": c['id_compra'],
        "libro_id": c['id_libro'],
        "titulo_libro": c['titulo_libro'] or "Libro eliminado",
        "fecha_compra": c['fecha_compra'].isoformat(),
        "precio_pagado": float(c['precio_pagado']),
        "estado": c['estado'],
        "metodo_pago": c['metodo_pago'],
        "direccion_envio": c['direccion_envio']
    } for c in compras]), 200