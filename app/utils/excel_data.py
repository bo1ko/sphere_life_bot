import gspread
import os

from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()


def get_excel_data():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file(os.getenv('SERVICE_ACCOUNT_FILE'), scopes=scopes)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1iAyFDR17mA4jUpr9DOP-vPULMq48N41jDvz7cxOqfIg/edit?gid=0#gid=0')
    data_key_list = ['media', 'qa', 'locations']
    data_dict = {}

    for i in range(3):
        worksheet = spreadsheet.get_worksheet(i)
        data = worksheet.get_all_values()
        data.pop(0)

        data_dict.update({data_key_list[i]: data})

    return data_dict
