# CheapFlightFinder
 
This project helps you find cheap flight deals from London to popular destinations around the world using the Amadeus Flight Offers API. When a flight's price drops below your specified threshold, it sends you an alert via SMS.


- Retrieves city IATA codes using Amadeus API.
- Searches for flight deals departing within a 10-day window.
- Compares results against your predefined lowest acceptable price.
- Sends low-price alerts to your phone via Twilio SMS.



Setup 
Google Sheets API Configuration
We switched from Sheety to Google Sheets API due to request limits and reliability.

Steps:
Go to Google Cloud Console.
Create a new project.
Enable the Google Sheets API.
Create a Service Account and generate a JSON key file.
Share your Google Sheet with the service account email.
Rename the downloaded credentials file to something like flight.json and DO NOT push this to GitHub.


pip install -r requirements.txt
