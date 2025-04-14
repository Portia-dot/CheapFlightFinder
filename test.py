import gspread
from google.oauth2.service_account import Credentials
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('flight.json', scopes = scope)
client = gspread.authorize(creds)

sheet_id = "1-Rk9VOdIlicJX-nXcibb2SfHPRH4aZU7CJv-XVEyoA4"
sheet = client.open_by_key(sheet_id)

values_list = sheet.sheet1.row_values(1)
print(values_list)