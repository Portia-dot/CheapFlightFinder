from dotenv import load_dotenv
import requests
import os
from datetime import date, timedelta
load_dotenv()


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.Amadeus_API = os.getenv("Amadeus_API")
        self.Amadeus_Secret = os.getenv("Amadeus_API_Secret")
        self.Endpoint = os.getenv("ENDPOINT")
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.token = self.amadeus_token_call()


        self.get_city_header = {
            'Authorization': f'Bearer {self.token}'
        }
        self.destinationLocationCode = "LON"

    def amadeus_token_call(self):

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.Amadeus_API,
            'client_secret': self.Amadeus_Secret,
        }
        response = requests.post(f'{self.Endpoint}/security/oauth2/token', headers=self.headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data['access_token']
        return access_token
    #
    def get_city_iata(self, city):

        url = f'{self.Endpoint}/reference-data/locations/cities'
        query_params = {
            'keyword': city,
            'max': '2',
            'include' : 'AIRPORTS'
        }
        response = requests.get(url, headers=self.get_city_header, params=query_params)
        response.raise_for_status()
        data = response.json()
        return data

    def get_flight_offer(self, destination_location_code, max_price):
        """ Method Limitations// Can not be used for custormers """
        url = f'{self.Endpoint}/shopping/flight-dates'
        #60 DAYS date range
        today = date.today() + timedelta(days=1)
        future_date = (date.today() + timedelta(days=10))
        print(today, future_date)

        def make_requests(params):
            data = requests.get(url, headers=self.get_city_header, params=params)
            data.raise_for_status()
            return data.json()

        date_range = f'{today.strftime("%Y-%m-%d")},{future_date.strftime("%Y-%m-%d")}'
        attempts = [
            {'origin': 'LON', 'destination': destination_location_code,'departureDate': date_range, 'maxPrice': max_price},
            {'origin': 'LON', 'destination': destination_location_code, 'departureDate': date_range},
        ]
        for query in attempts:
            try:
                response = make_requests(query)
                if 'data' in response and len(response['data']) > 0:
                    result = response['data'][0]
                    return result
                else:
                    print('No data returned')
                    return None
            except requests.exceptions.HTTPError as e:
                print(f'http error {e}')
                try:
                    error_response = e.response.json()
                    print('Error JSON',error_response)
                except ValueError:
                    print("Response content is not valid JSON:", e.response.text)
                break
            except requests.exceptions.RequestException as e:
                if e.response.status_code == 404:
                    print('Retrying With No Price To See The Lowest Price')
                    continue
                else:
                    print(f'http error {e}')
        return None

