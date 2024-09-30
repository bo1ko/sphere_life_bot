import gspread
import os
import psycopg2
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv


load_dotenv()

def get_data():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file(os.getenv('SERVICE_ACCOUNT_FILE'), scopes=scopes)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(os.getenv('SHEET_URL_KEY'))
    worksheet = spreadsheet.sheet1
    sheet_data = worksheet.get_all_values()
    sheet_data.pop(0)

    return sheet_data


def clear_table(cursor):
    cursor.execute('DELETE FROM my_table')


def save_to_db(sheet_data):
    # Підключаємося до бази даних PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = conn.cursor()
    clear_table(cursor)

    cursor.executemany('''
        INSERT INTO my_table (column1, column2, column3, column4)
        VALUES (%s, %s, %s, %s)
    ''', sheet_data)

    conn.commit()

    cursor.close()
    conn.close()

def save_service_data(sheet_data):
    ...

def save_media_data(sheet_data):
    ...


if __name__ == "__main__":
    data = get_data()

    save_to_db(data)
