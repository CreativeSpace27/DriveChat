from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

def search_drive(query_string: str, order_by: str = "modifiedTime desc"):
    """Executes a search with optional sorting."""
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    service = build('drive', 'v3', credentials=creds)
    
    results = service.files().list(
        q=query_string,
        orderBy=order_by,  # This is a separate parameter from 'q'
        pageSize=10,       # Limits results for better performance
        spaces='drive',
        fields='files(id, name, mimeType, webViewLink, modifiedTime)',
    ).execute()
    
    return results.get('files', [])