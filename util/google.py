from google.oauth2 import id_token
from google.auth.transport import requests

def verificar_token_google(token):
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request())

        return {
            "id": id_info.get("sub"),
            "correo": id_info.get("email"),
            "nombre": id_info.get("name"),
        }

    except ValueError:
        # El token es inválido
        return None
