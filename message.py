from dotenv import load_dotenv
import os
from twilio.rest import Client
load_dotenv()

from flight_search import FlightSearch
import requests

import smtplib

flight_search = FlightSearch()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
account_token = os.getenv("TWILIO_ACCOUNT_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
my_phone = os.getenv("MY_PHONE_NUMBER")

email = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")

print(email, password)


class Message:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(account_sid, account_token)

    def send(self, message):
        msg = self.client.messages.create(
            body=message,
            from_='+14452922187',
            to='+13062612371'
        )

        print(msg.sid)

    def get_flight_info(self, iata_code, maxPrice = None):
        try:
            if maxPrice:
                result = flight_search.get_flight_offer(destination_location_code=iata_code, max_price=maxPrice)
            else:
                result = flight_search.get_flight_offer(destination_location_code=iata_code, max_price=None)
            if not result:
                print("No flight offer found")
                return None
            print(result)
            fromCity = result['origin']
            toCity = result['destination']
            departureDate = result['departureDate']
            returnDate = result['returnDate']
            price = result['price']
            message = f'{price['total']} Pounds {fromCity} to {toCity}! on {departureDate} to {returnDate}'
            return message
        except requests.exceptions.RequestException as e:
            print('Handled Expected exception',e)

    def send_mail(self, message, user_email):
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email, to_addrs=user_email, msg=f'Subject: Flight Offer!\n\n{message}')

