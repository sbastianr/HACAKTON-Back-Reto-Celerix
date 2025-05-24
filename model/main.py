from datetime import datetime, timedelta

from flask import Flask, request, jsonify
import httpx
from jwt import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from db import Database
from token_ import token_required
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
app = Flask(__name__)
db = Database()
app.config['SECRET_KEY'] = 'test'


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    nombre = data.get("nombre")
    correo = data.get("correo")

    if db.get_user_by_email(correo):
        return jsonify({"error": "Usuario ya existe"}), 400

    return jsonify({"message": "Usuario registrado correctamente"}), 201

# Endpoint para login con token de Google
@app.route('/login', methods=['POST'])
def login():
    token = request.json.get('id_token')
    if not token:
        return jsonify({'error': 'Token no proporcionado'}), 400

    try:
        # Verificar token con Google
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request())

        nombre = idinfo.get('name', '')
        email = idinfo.get('email', '')

        # Crear o recuperar usuario
        usuario = get_user_by_email(email)

        # Generar JWT propio
        token_backend = jwt.encode({
            'sub': usuario['id'],
            'nombre': usuario['nombre'],
            'email': usuario['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token_backend})

    except ValueError:
        return jsonify({'error': 'Token inválido'}), 400
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = db.get_user(username)
    if not user or not check_password_hash(user[2], password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = jwt.encode({
        'user_id': user['id_user'],
        'exp': datetime.now() + timedelta(minutes=500)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token, 'message': 'Inicio de sesión exitoso'}), 200

@app.route('/consultar-procesos-by-nombre-razonsocial', methods=['GET'])
@token_required
def consultar_procesos_by_nombre_razonsocial():
    nombre = request.args.get('nombre')
    tipo_persona = request.args.get('tipoPersona')
    solo_activos = request.args.get('SoloActivos')
    codificacion_despacho = request.args.get('codificacionDespacho')
    pagina = request.args.get('pagina', '1').strip()  # eliminamos espacios y saltos de línea

    if not all([nombre, tipo_persona, solo_activos, codificacion_despacho]):
        return jsonify({'error': 'Faltan parámetros obligatorios'}), 400

    url = 'https://consultaprocesos.ramajudicial.gov.co:448/api/v2/Procesos/Consulta/NombreRazonSocial'
    params = {
        "nombre": nombre,
        "tipoPersona": tipo_persona,
        "SoloActivos": solo_activos,
        "codificacionDespacho": codificacion_despacho,
        "pagina": pagina
    }
    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.get(url, params=params)

            if response.status_code == 200:
                return jsonify(response.json()), 200
            else:
                return jsonify({
                    'error': 'Error al consultar el API externa',
                    'status_code': response.status_code,
                    'detalle': response.text
                }), 502

    except httpx.RequestError as e:
        return jsonify({'error': 'Error de conexión', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)