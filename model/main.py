import datetime

from flask import Flask, request, jsonify
import httpx
import jwt

from model.db import Database
from util.google import verificar_token_google

app = Flask(__name__)
db = Database()
SECRET_KEY = "test"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user_info = verificar_token_google(data.get("token"))
    if user_info:

        nombre = user_info.get("nombre")
        correo = user_info.get("correo")
        cedula = user_info.get("id")

    if db.get_or_create_user(nombre, correo, cedula):
        return jsonify({"error": "Usuario ya existe"}), 400

    # Generar JWT propio para la sesión
    payload = {
        "user_id": user_info.get("id"),
        "nombre": user_info.get("nombre"),
        "correo": user_info.get("correo"),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # Expira en 2 horas
    }
    token_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({"message": "Usuario registrado correctamente", "token": token_jwt}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    token = data.get("token")

    user_info = verificar_token_google(token)
    if not user_info:
        return jsonify({"error": "Token inválido"}), 401

    correo = user_info.get("correo")
    usuario = db.get_user_by_email(correo)

    if not usuario:
        return jsonify({"error": "Usuario no registrado"}), 404

    # Generar JWT propio para la sesión
    payload = {
        "user_id": usuario['USU_ID_USUARIO'],
        "nombre": usuario['USU_NOMBRE'],
        "correo": usuario['USU_CORREO'],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # Expira en 2 horas
    }
    token_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({"message": "Login exitoso", "token": token_jwt})


@app.route('/consultar-procesos-by-nombre-razonsocial', methods=['GET'])
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