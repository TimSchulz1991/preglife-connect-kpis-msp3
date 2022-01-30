import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("connect_kpis")

#kpis = SHEET.worksheet("kpis")
#data = kpis.get_all_values()
#print(data)

def get_date():
    """
    This function is used to get the date from the user for which the KPIs should be entered into the sheet. 
    """
    while True:
        print("For which date would you like to enter the KPIs or Preglife Connect?")
        print("Please enter the date in the following format: DD/MM/YYYY, e.g. 22/02/2022\n")
        date_input = input("Enter the date here:\n")
        print(date_input)

get_date()
