from flask import Blueprint, request, jsonify
from ..utils import db
from datetime import datetime

contacto_bp = Blueprint('contacto', __name__)

@contacto_bp.route('/', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()

    required = ['nombre', 'correo', 'mensaje']
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    nuevo_contacto = Contacto(
        nombre=data['nombre'],
        correo=data['correo'],
        mensaje=data['mensaje'],
        fecha_envio=datetime.utcnow(),
        leido=False
    )

    try:
        db.session.add(nuevo_contacto)
        db.session.commit()
        
        return jsonify({"mensaje": "Mensaje enviado correctamente. ¡Gracias por contactarnos!"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al guardar el mensaje"}), 500