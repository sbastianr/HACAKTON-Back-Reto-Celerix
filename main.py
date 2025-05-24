from flask import Flask, request, jsonify
import requests
import httpx

app = Flask(__name__)

@app.route('/consultar-procesos-by-nombre-razonsocial', methods=['GET'])
def consultar_procesos():
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


@app.route('/consultar-procesos-byC-nombre-razonsocial', methods=['GET'])
def consultar_procesos():
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