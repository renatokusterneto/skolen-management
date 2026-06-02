import os
from datetime import datetime
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[4]
load_dotenv(ROOT / ".env")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET = "pendentes"


def _get_service():
    sa_file = ROOT / os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE").lstrip("./")
    creds = service_account.Credentials.from_service_account_file(
        str(sa_file), scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)


def register_post(
    campaign_id: str,
    tipo: str,
    titulo: str,
    data_postagem: str,
    caption: str,
    cloudinary_urls: list[str],
    publicado: bool = False,
) -> None:
    service = _get_service()

    # Converter data para serial numérico do Sheets (imune a formato de célula e locale)
    try:
        dt = datetime.strptime(data_postagem.strip(), "%Y-%m-%d %H:%M")
        sheets_epoch = datetime(1899, 12, 30)
        data_serial = (dt - sheets_epoch).total_seconds() / 86400
    except ValueError:
        data_serial = data_postagem

    row = [[
        campaign_id,
        tipo,
        titulo,
        data_serial,
        caption,
        ",".join(cloudinary_urls),
        publicado,
    ]]
    service.spreadsheets().values().append(
        spreadsheetId=os.getenv("GOOGLE_SHEETS_ID"),
        range=f"{SHEET}!A:G",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": row},
    ).execute()
    print(f"  OK Registrado em '{SHEET}': {titulo} ({data_postagem})")
