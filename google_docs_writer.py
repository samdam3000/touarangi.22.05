# google_docs_writer.py

from google.oauth2 import service_account
from googleapiclient.discovery import build

DOCUMENT_ID = "your-google-doc-id-here"  # Replace with your actual doc ID
SCOPES = ['https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Your service account file

def send_strike_to_doc(strike):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    service = build('docs', 'v1', credentials=creds)

    body = {
        'requests': [{
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': format_strike(strike)
            }
        }]
    }

    service.documents().batchUpdate(
        documentId=DOCUMENT_ID, body=body).execute()

def format_strike(strike):
    return (
        f"\n\nSTRIKE ALERT [{strike.get('confirmed_time')} UTC]\n"
        f"Market: {strike.get('market')}\n"
        f"Player: {strike.get('player')}\n"
        f"Confidence: {strike.get('confidence')}%\n"
        f"Odds: {strike.get('odds')}\n"
        f"Reason: {strike.get('reason')}\n"
    )