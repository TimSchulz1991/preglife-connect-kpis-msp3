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

print("""Welcome to this Python program to save the most recent
Preglife Connect KPIs and to analyse the current trends for you!\n""")
# The setup of the connection between Python and the Google sheet
# was done with the help of the LoveSandwiches project.


def get_date():
    """
    This function is used to get the date from the user
    for which the KPIs should be entered into the sheet.
    """
    while True:
        print(
            "For which date would you like to enter "
            "the KPIs of the Preglife Connect app?\n"
        )
        print(
            "Please enter the date in the following format: "
            "DD/MM/YYYY, e.g. 22/02/2022\n"
        )

        date_input = input("Enter the date here:\n")

        if validate_date(date_input):
            print("Thank you for entering a valid date.\n")
            break
    return date_input


def validate_date(date):
    """
    This function checks if the given date exists
    in the sheet and can be filled with values.
    """
    if WORKSHEET.find(date) is not None:
        return True
    else:
        print("That was not a valid date, please try again.\n")
        return False


def get_kpis(date):
    """
    This function gets all the KPIs from the user and saves them in a list.
    """
    kpi_list = []
    prompts = ["Please enter the number of APP OPENS "
               f"for the chosen date ({date}):\n",
               "Please enter the number of SCREEN VIEWS "
               f"for the chosen date ({date}):\n",
               "Please enter the number of AD VIEWS "
               f"for the chosen date ({date}):\n",
               "Please enter the number of CREATED THREADS "
               f"for the chosen date ({date}):\n",
               "Please enter the number of SWIPES "
               f"for the chosen date ({date}):\n"]
    i = 0
    while len(prompts) != len(kpi_list):
        kpi_input = input(prompts[i])
        if validate_kpi(kpi_input):
            kpi_list.append(kpi_input)
            i += 1
    print("Thanks for entering valid data!")
    return kpi_list


def validate_kpi(kpi):
    """
    This function validates that the given values are integers
    larger than or equal to 0.
    """
    try:
        kpi_input = int(kpi)
        if kpi_input < 0:
            print("Your input must all be positive, whole numbers\n")
            return False
    except ValueError:
        print("You can only enter numbers\n")
        return False
    return True


def main():
    """
    This function will execute all the other functions to run the program.
    """
    chosen_date = get_date()
    get_kpis(chosen_date)


main()
