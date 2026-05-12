import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_drive_service():
    scopes = ['https://www.googleapis.com/auth/drive.readonly']
    creds_json = os.getenv("GOOGLE_CREDENTIALS")

    if creds_json:
        creds_info = json.loads(creds_json)
        creds = service_account.Credentials.from_service_account_info(creds_info, scopes=scopes)
    
    elif os.path.exists('credentials.json'):
        creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=scopes)
    
    else:
        raise FileNotFoundError("Google credentials not found in Environment Variables or local file.")

    return build('drive', 'v3', credentials=creds)

def search_drive(query_string: str, order_by: str = "modifiedTime desc"):
    service = get_drive_service()
    results = service.files().list(
        q=query_string,
        orderBy=order_by,
        spaces='drive',
        fields='files(id, name, mimeType, webViewLink, modifiedTime)',
    ).execute()
    return results.get('files', [])