from datetime import datetime, timedelta

from flask import Flask, request, jsonify
import httpx
from jwt import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from db import Database
from token_ import token_required

app = Flask(__name__)
db = Database()
app.config['SECRET_KEY'] = 'test'


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if db.get_user(username):
        return jsonify({"error": "Usuario ya existe"}), 400

    password_hash = generate_password_hash(password)
    db.add_user(username, password_hash)
    return jsonify({"message": "Usuario registrado correctamente"}), 201

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