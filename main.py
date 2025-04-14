#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import time

import requests

from data_manager import DataManager
from flight_search import FlightSearch
from message import Message

#
#
data_manager = DataManager()
flight_search = FlightSearch()
message_manager = Message()

all_messages = []
#
sheet_data = data_manager.get_data()
try:
    for index, row in sheet_data.iterrows():
        if row['IATA Code'] == '':
            city = row['City']
            time.sleep(5)
            try:
                response = flight_search.get_city_iata(city)
                iataCode = response['data'][0]['iataCode']
                sheet_data.at[index, 'IATA Code'] = iataCode
                data_manager.update_data(sheet_data, column_name = 'IATA Code')
            except Exception as e:
                print(e)
        else:
            iataCode = row['IATA Code']
            maxPrice = row['Lowest Price']
            time.sleep(10)
            try:
                result = flight_search.get_flight_offer(destination_location_code=iataCode, max_price=maxPrice)
                if not result:
                    print('No flight offer found')
                    continue
                fromCity = result['origin']
                toCity = result['destination']
                departureDate = result['departureDate']
                returnDate = result['returnDate']
                price = result['price']

                message = f'{price['total']} Pounds {fromCity} to {toCity}! on {departureDate} to {returnDate}'
                all_messages.append(message)
            except requests.exceptions.RequestException as e:
                print('Handled Expected exception',e)
    # if all_messages:
    #     full_message = '\n\n'.join(all_messages)
    #     message_manager.send(full_message)
except Exception as e:
    print(e)


token = flight_search.amadeus_token_call()
print(token)