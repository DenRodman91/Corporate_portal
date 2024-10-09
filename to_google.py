import pandas as pd
import gspread
import os
from gspread_dataframe import set_with_dataframe
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

def to_google(book_id, sheet_name, df):
# Загружаем в гугл-листы
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    SAMPLE_SPREADSHEET_ID = book_id
    creds = None
    if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)


    try:
        gc = gspread.authorize(creds)
        # Открываем нужную таблицу
        spreadsheet = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
        # Записываем DataFrame в Google Таблицу
        worksheet = spreadsheet.worksheet(sheet_name)
        # set_with_dataframe(worksheet, df)
        headers = worksheet.row_values(1)
        worksheet.append_row(headers)
        worksheet.append_rows(df.values.tolist(), value_input_option='USER_ENTERED')
        print('Таблица успешно записана в Google Sheets!')
    except HttpError as err:
        print(err)