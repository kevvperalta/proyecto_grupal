from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not all(k in data for k in ['nombre', 'correo', 'password']):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión"}), 500

    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Usuarios WHERE correo = %s", (data['correo'],))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Correo ya registrado"}), 409

    hashed_pw = generate_password_hash(data['password'])
    
    cursor.execute(
        "INSERT INTO Usuarios (nombre, correo, password_hash) VALUES (%s, %s, %s)",
        (data['nombre'], data['correo'], hashed_pw)
    )
    conn.commit()
    conn.close()
    
    return jsonify({"mensaje": "Registro exitoso"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not all(k in data for k in ['correo', 'password']):
        return jsonify({"error": "Faltan campos"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de conexión"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuarios WHERE correo = %s", (data['correo'],))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario or not check_password_hash(usuario['password_hash'], data['password']):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = create_access_token(identity=usuario['id_usuario'])
    return jsonify({"token": token, "mensaje": "Inicio de sesión exitoso"}), 200