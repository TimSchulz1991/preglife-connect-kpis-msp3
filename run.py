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
WORKSHEET = SHEET.worksheet("kpis")

#kpis = SHEET.worksheet("kpis")
#data = kpis.get_all_values()
#print(data)

print("Welcome to this Python program to save the most recent Preglife Connect KPIs\nand to analyse the current trends for you!\n")

def get_date():
    """
    This function is used to get the date from the user for which the KPIs should be entered into the sheet. 
    """
    while True:
        print("For which date would you like to enter the KPIs of the Preglife Connect app?")
        print("Please enter the date in the following format: DD/MM/YYYY, e.g. 22/02/2022\n")
        date_input = input("Enter the date here:\n")
        
        if validate_date(date_input):
            print("Thank you for entering a valid date.\n")
            break
        
    return date_input

def validate_date(date):
    """
    This function checks if the given date exists in the sheet and can be filled with values.
    """
    if WORKSHEET.find(date) is not None:
        return True
    else: 
        print("That was not a valid date, please try again.\n")
        return False

def get_kpis():
    date = get_date()
    kpi_list = []
    promts = [f"Please enter the number of APP OPENS for {date}:\n","Please enter the number of SCREEN VIEWS:\n",
    "Please enter the number of AD VIEWS:\n","Please enter the number of CREATED THREADS:\n",
    "Please enter the number of SWIPES:\n"]
    for i in range(len(promts)):
        kpi_input = input(promts[i])
        kpi_list.append(kpi_input)
    print(kpi_list)


def main():
    get_date()
    #get_kpis()

main()
