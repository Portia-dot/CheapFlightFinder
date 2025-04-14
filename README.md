# CheapFlightFinder
 
This project helps you find cheap flight deals from London to popular destinations around the world using the Amadeus Flight Offers API. When a flight's price drops below your specified threshold, it sends you an alert via SMS.


- Retrieves city IATA codes using Amadeus API.
- Searches for flight deals departing within a 10-day window.
- Compares results against your predefined lowest acceptable price.
- Sends low-price alerts to your phone via Twilio SMS.






pip install -r requirements.txt
