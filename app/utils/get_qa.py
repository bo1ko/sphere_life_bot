import gspread
import os

from google.oauth2.service_account import Credentials
from dotenv import load_dotenv


load_dotenv()

def get_data():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file(os.getenv('SERVICE_ACCOUNT_FILE'), scopes=scopes)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(os.getenv('SHEET_URL_KEY'))
    worksheet = spreadsheet.sheet1
    data = worksheet.get_all_values()
    data.pop(0)

    return data
