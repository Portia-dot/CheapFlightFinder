import os
import random

from dotenv import load_dotenv
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


load_dotenv()
google_sheet_id = os.getenv("GOOGLE_SHEET_ID")

class DataManager:
    def __init__(self):
        self.scope = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = Credentials.from_service_account_file('flight.json', scopes=self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet_id = google_sheet_id
        self.sheet = self.client.open_by_key(self.sheet_id)

    #Get Request
    def get_data(self):
        values_list = self.sheet.sheet1.get_values()
        headers = values_list[0]
        rows = values_list[1:]
        df = pd.DataFrame(rows, columns=headers)
        return df
    #  Put Request
    def update_data(self,dataframe, column_name):
        dataframe[column_name] = dataframe[column_name]
        value_to_write = [dataframe.columns.tolist()] + dataframe.values.tolist()
        worksheet = self.sheet.sheet1
        worksheet.clear()
        worksheet.update(values=value_to_write)
