# calendar_utils.py
import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import google.auth

# Carga las variables de entorno (asegúrate de tener GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET)
from dotenv import load_dotenv
load_dotenv()

# Define los permisos que solicitarás (scopes)
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
# Asegúrate de tener 'client_secret.json' o configurar las variables de entorno
CLIENT_SECRETS_FILE = os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "client_secret.json")

def get_calendar_flow(redirect_uri):
    """Inicia el flujo OAuth2."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    return flow

def build_calendar_service(credentials_info):
    """Construye el servicio de Google Calendar."""
    creds = Credentials.from_authorized_user_info(credentials_info, SCOPES)
    # Si las credenciales han expirado, las refresca
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Aquí deberías guardar las credenciales actualizadas en tu DB
    
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_calendar_event(service, summary, description, start_time, end_time):
    """Crea un evento en el calendario principal del usuario."""
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(), # Formato: '2025-05-28T09:00:00-05:00'
            'timeZone': 'America/Bogota',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Bogota',
        },
    }
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Evento creado: {event.get("htmlLink")}')
        return event.get("htmlLink")
    except Exception as e:
        print(f"Error al crear evento: {e}")
        return None
