import os
import json
import gspread
from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

current_working_dir = os.getcwd()

google_secrets = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
google_secrets = json.loads(google_secrets)

credentials = service_account.Credentials.from_service_account_info(google_secrets)
spreadsheet_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

client = gspread.authorize(credentials)
