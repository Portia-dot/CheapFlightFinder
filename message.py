from dotenv import load_dotenv
import requests
import os
from twilio.rest import Client
load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
account_token = os.getenv("TWILIO_ACCOUNT_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
my_phone = os.getenv("MY_PHONE_NUMBER")

class Message:
    def __init__(self):
        self.client = Client(account_sid, account_token)

    def send(self, message):
        msg = self.client.messages.create(
            body=message,
            from_='+14452922187',
            to='+13062612371'
        )

        print(message.sid)