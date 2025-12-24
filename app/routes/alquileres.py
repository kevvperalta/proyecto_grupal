# app/routes/alquileres.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.db import get_db_connection  # ← Conexión directa
from datetime import datetime, timedelta

alquileres_bp = Blueprint('alquileres', __name__)

@alquileres_bp.route('/', methods=['POST'])
@jwt_required()
def crear_alquiler():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    required_fields = ['id_libro', 'dias_alquiler']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    if not isinstance(data['dias_alquiler'], int) or data['dias_alquiler'] < 1 or data['dias_alquiler'] > 30:
        return jsonify({"error": "Los días de alquiler deben estar entre 1 y 30"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión"}), 500

    cursor = conn.cursor(dictionary=True)

    # Verificar libro y stock
    cursor.execute("SELECT * FROM Libros WHERE id_libro = %s", (data['id_libro'],))
    libro = cursor.fetchone()
    if not libro:
        conn.close()
        return jsonify({"error": "Libro no encontrado"}), 404

    if libro['stock_alquiler'] <= 0:
        conn.close()
        return jsonify({"error": "No hay unidades disponibles para alquiler"}), 400

    fecha_inicio = datetime.utcnow()
    fecha_devolucion = fecha_inicio + timedelta(days=data['dias_alquiler'])

    try:
        cursor.execute("""
            INSERT INTO Alquileres 
            (id_usuario, id_libro, dias_alquiler, fecha_inicio, fecha_devolucion, estado)
            VALUES (%s, %s, %s, %s, %s, 'activo')
        """, (
            current_user_id,
            data['id_libro'],
            data['dias_alquiler'],
            fecha_inicio,
            fecha_devolucion
        ))

        # Reducir stock alquiler
        cursor.execute("UPDATE Libros SET stock_alquiler = stock_alquiler - 1 WHERE id_libro = %s", (data['id_libro'],))

        conn.commit()
        alquiler_id = cursor.lastrowid

        conn.close()

        return jsonify({
            "mensaje": "Alquiler registrado exitosamente",
            "alquiler_id": alquiler_id,
            "libro": libro['titulo'],
            "dias": data['dias_alquiler'],
            "fecha_devolucion": fecha_devolucion.isoformat()
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": str(e)}), 500


@alquileres_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_mis_alquileres():
    current_user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id_alquiler, a.id_libro, l.titulo as titulo_libro, 
               a.dias_alquiler, a.fecha_inicio, a.fecha_devolucion, a.estado
        FROM Alquileres a
        LEFT JOIN Libros l ON a.id_libro = l.id_libro
        WHERE a.id_usuario = %s
    """, (current_user_id,))
    
    alquileres = cursor.fetchall()
    conn.close()

    return jsonify([{
        "id_alquiler": a['id_alquiler'],
        "libro_id": a['id_libro'],
        "titulo_libro": a['titulo_libro'] or "Libro eliminado",
        "dias_alquiler": a['dias_alquiler'],
        "fecha_inicio": a['fecha_inicio'].isoformat(),
        "fecha_devolucion": a['fecha_devolucion'].isoformat() if a['fecha_devolucion'] else None,
        "estado": a['estado']
    } for a in alquileres]), 200