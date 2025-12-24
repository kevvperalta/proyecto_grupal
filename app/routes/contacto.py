from flask import Blueprint, request, jsonify
from ..utils.db import get_db_connection  # ✅ Conexión directa
from datetime import datetime

contacto_bp = Blueprint('contacto', __name__)

@contacto_bp.route('/', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()

    required = ['nombre', 'correo', 'mensaje']
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión a la BD"}), 500
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO Contactos (nombre, correo, mensaje, fecha_envio, leido)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['nombre'],
            data['correo'],
            data['mensaje'],
            datetime.utcnow(),
            False
        ))
        
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Mensaje enviado correctamente. ¡Gracias por contactarnos!"}), 201
    
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": "Error al guardar el mensaje"}), 500