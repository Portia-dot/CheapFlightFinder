import os

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

        values_list = self.sheet.sheet1.row_values(1)
        print(values_list)


        self.file = 'Flights - prices.csv'
        self.data = self.get_data()

    #Get Request
    def get_data(self):
        return pd.read_csv(self.file)
    #  Put Request
    def update_data(self, index, new_data):
        df = pd.read_csv(self.file)
        df.loc[index, 'IATA Code'] = new_data['IATA Code']
        df.to_csv(self.file, index=False)
