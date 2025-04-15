#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from message import Message
import time

#
#
data_manager = DataManager()
flight_search = FlightSearch()
message_manager = Message()


all_messages = []
user_messages = []

is_running = True
user_question = input("Enter Y for yourself and U for users: ").lower().strip()
#
sheet_data = data_manager.get_data(sheet_name='prices')
#Single User Logic
while is_running:
    if user_question == 'y':
        is_running = False
        try:
            for index, row in sheet_data.iterrows():
                if row['IATA Code'] == '':
                    city = row['City']
                    time.sleep(5)
                    data_manager.get_iata_code(city, sheet_data, index = index, sheet_name = 'prices', column_name = 'IATA Code')
                else:
                    iataCode = row['IATA Code']
                    maxPrice = row['Lowest Price']
                    time.sleep(10)
                    message = message_manager.get_flight_info(iataCode, maxPrice)
                    if message:
                        all_messages.append(message)
            if all_messages:
                full_message = '\n\n'.join(all_messages)
                print(full_message)
                message_manager.send(full_message)
        except Exception as e:
            print(e)

    #Dealing with User Implementation
    elif user_question == 'n':
        is_running = False
    # #Users Logic
        users = data_manager.get_data(sheet_name='users')
        user_details = data_manager.get_users_details(users)
        result = data_manager.get_user_location_iata(user_details)
        for user in result:
            first_name = user[0]
            last_name = user[1]
            prefered_city = user[2]
            email = user[3]
            iata_code = user[4]

            for city, code  in zip(prefered_city, iata_code):
                if code:
                    iataCode = code
                    message = message_manager.get_flight_info(iataCode)
                    if message:
                        user_messages.append(message)
                    message_manager.send_mail(message, email)
                    print('Message sent')
                else:
                    print(f'No code for {city}')

    else:
        print('Please enter Y for yourself and U for users')
