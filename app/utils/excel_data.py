import gspread
import os

from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

links = [
    'https://docs.google.com/spreadsheets/d/1bZkViv8VXWzYfaDL8qHXDa6U-oAbWEMl2RGbdNCa5cE/edit?gid=0#gid=0',
    'https://docs.google.com/spreadsheets/d/1o2n1A3-qL9ymLIGKBs7W26HcKfzmxKUs4jAWZICYgVE/edit?gid=0#gid=0',
    'https://docs.google.com/spreadsheets/d/1A--e54LdGYRBs4bxufVN6VgDP1o5KSGuJPbTjJdenRw/edit?gid=0#gid=0',
]

def get_excel_data():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file(os.getenv('SERVICE_ACCOUNT_FILE'), scopes=scopes)
    client = gspread.authorize(credentials)

    data_key_list = ['qa', 'media', 'locations']
    data_dict = {}
    count = 0
    for i in links:
        spreadsheet = client.open_by_url(i)
        worksheet = spreadsheet.get_worksheet(0)
        data = worksheet.get_all_values()
        data.pop(0)
        data_dict[data_key_list[count]] = data
        count += 1
    
    return data_dict
