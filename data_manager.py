import os
from dotenv import load_dotenv
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from flight_search import FlightSearch




load_dotenv()
google_sheet_id = os.getenv("GOOGLE_SHEET_ID")
flight_search = FlightSearch()

class DataManager:
    def __init__(self):
        self.scope = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = Credentials.from_service_account_file('flight.json', scopes=self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet_id = google_sheet_id
        self.sheet = self.client.open_by_key(self.sheet_id)
        self.user_details = []
    #Get IATA CODE

    #Get Request-
    def get_data(self, sheet_name = 'Sheet1'):
        worksheet = self.sheet.worksheet(sheet_name)
        values_list = worksheet.get_all_values()
        headers = values_list[0]
        rows = values_list[1:]
        df = pd.DataFrame(rows, columns=headers)
        return df
    #  Put Request
    def update_data(self,dataframe, column_name, sheet_name = 'Sheet1'):
        worksheet = self.sheet.worksheet(sheet_name)
        dataframe[column_name] = dataframe[column_name]
        value_to_write = [dataframe.columns.tolist()] + dataframe.values.tolist()
        worksheet.clear()
        worksheet.update(values=value_to_write)

    def get_iata_code(self, city, dataframe, column_name, index, sheet_name = 'Sheet1'):
        try:
            response = flight_search.get_city_iata(city)
            iataCode = response['data'][0]['iataCode']
            dataframe.at[index, column_name] = iataCode
            self.update_data(dataframe, column_name=column_name , sheet_name= sheet_name)
        except Exception as e:
            print(e)



        except requests.exceptions.RequestException as e:
            print('Handled Expected exception', e)

    def get_users_details(self, user_dataframe):
        unique_users = user_dataframe.drop_duplicates(subset="Email")
        user_data = []
        for index, row in unique_users.iterrows():
            first_name = row['First Name']
            last_name = row['Last Name']
            destinations  = row['Preferred Destinations'].split(",")
            email = row['Email']
            user_data.append([first_name, last_name, destinations, email])
        return user_data

    def get_user_location_iata(self, user_details):
        for users in user_details:
            first_name = users[0]
            last_name = users[1]
            destinations = users[2]
            email = users[3]
            iata_code = []
            for city in destinations:
                try:
                    response = flight_search.get_city_iata(city)
                    if 'data' in response and len(response['data']) > 0:
                        iata = response['data'][0]['iataCode']
                        iata_code.append(iata)
                    else:
                       iata_code.append(None)
                except Exception as e:
                    print(e)
            self.user_details.append([first_name, last_name, destinations, email, iata_code])
        return self.user_details
