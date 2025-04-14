from dotenv import load_dotenv
import requests
import pandas as pd
load_dotenv()
class DataManager:
    def __init__(self):
        # self.sheety_endpoint = os.environ.get('SHEETY_GET_ENDPOINT')
        # self.sheety_get_endpoint = os.environ.get('SHEETY_GET_ENDPOINT')
        # self.data = self.get_data()
        # self.headers = {
        #     'Content-Type': 'application/json',
        #     'Authorization': 'Basic' + os.environ.get('SHEETY_AUTH')
        #
        # }

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
