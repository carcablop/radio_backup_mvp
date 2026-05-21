from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def autenticar_drive():
    """
    Autentica la aplicación con Google Drive desde Visual Studio Code.

    Usa:
    - credentials.json: credenciales descargadas desde Google Cloud
    - token.json: token generado después del primer inicio de sesión

    Retorna:
    - service: cliente de Google Drive API
    """

    creds = None
    credentials_path = Path("credentials.json")
    token_path = Path("token.json")

    if not credentials_path.exists():
        raise FileNotFoundError(
            "No se encontró credentials.json. "
            "Debes ponerlo en la carpeta raíz del proyecto."
        )

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)
    return service