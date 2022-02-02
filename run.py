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
    if WORKSHEET.find(date):
        return True
    else:
        print("That was not a valid date, please try again.\n")
        return False


def last_30_day_data(date):
    """
    This function grabs the values from the last 30 days of each KPI
    from the worksheet and calculates their averages.
    """
    # This function was set up with the help of the gspread documentation.
    date_cell = WORKSHEET.find(date)
    date_cell_row = date_cell.row
    range_start = str(date_cell_row-30)
    range_end = str(date_cell_row-1)

    final_values = []
    for let in ["B", "C", "D", "E", "F"]:
        column_values = []
        for row in WORKSHEET.range(f"{let}{range_start}:{let}{range_end}"):
            column_values.append(row.value)
        final_values.append(column_values)
    return final_values


def check_30_day_data(values):
    """
    This function will check how many of the 30 values are empty and
    subsquently give a string to the user if they were sloppy
    entering values during the last 30 days.
    """
    all_empty_values_list = []
    for column in values:
        column_empty_values = []
        for value in column:
            if value == "":
                column_empty_values.append(value)
        all_empty_values_list.append(column_empty_values)

    for each_list in all_empty_values_list:
        if len(each_list) > 0:
            print(
                "It seems like you have missed to enter some values "
                "on recent dates. Please enter data consistently in the future "
                "in order to not distort the following calculations.\n"
            )
            break
        else:
            print("Good job, you have entered data for the last 30 days!\n")
            break


def get_30_day_averages(values):
    """
    This function will calculate the averages for the last 30
    days for each KPI.
    """
    list_with_sums = []
    for each_list in values:
        int_list = [int(num) for num in each_list if num != ""]
        list_with_sums.append(sum(int_list))

    list_with_lens = []
    for each_list in values:
        no_empty_strings_list = []
        for item in each_list:
            if item != "":
                no_empty_strings_list.append(item)
        list_with_lens.append(len(no_empty_strings_list))

    averages = (
        [num1/num2 for num1, num2 in zip(list_with_sums, list_with_lens)]
    )
    return averages


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
    # Thanks to my colleague Daniel to give me the idea to
    # use a while loop in this particular way
    while len(prompts) != len(kpi_list):
        kpi_input = input(prompts[i])
        if validate_kpi(kpi_input):
            kpi_list.append(kpi_input)
            i += 1
    print("Thanks for entering valid data!\n")
    return kpi_list


def validate_kpi(kpi):
    """
    This function validates that the given values are integers
    larger than or equal to 0.
    """
    # This stackoverflow page helped me with
    # the validation process (for positive integer):
    # https://stackoverflow.com/questions/26198131/check-if-input-is-positive-integer
    try:
        kpi_input = int(kpi)
        if kpi_input < 0:
            print("Your input must be a positive, whole number!\n")
            return False
    except ValueError:
        print("You can only enter whole numbers!\n")
        return False
    return True


def update_worksheet(kpis, date):
    """
    This function will grab the Google sheet and update it with the
    KPIs that were entered by the user for a given date.
    """
    print("The KPIs worksheet is currently updating...\n")
    date_cell = WORKSHEET.find(date)
    i = 0
    for col in range(1, 6):
        WORKSHEET.update_cell(date_cell.row, date_cell.col+col, kpis[i])
        i += 1
    print("Worksheet successfully updated.\n")


def calculate_current_trends(kpis, averages):
    """
    This function will calculate how the KPIs have developed compared
    to the average of the last 30 days.
    """ 
    trends_list = [(kpi/average)-1 for kpi, average in zip(kpis, averages)]
    return trends_list


def evaluate_trends(trends):
    """
    This function will evaluate the previously calculated trends
    of KPI development and will give the user relevant 
    information about it.
    """
    all_kpis = ["App Opens", "Screen Views", "Ad Views", "Threads Created", "Swipes"]
    min_kpi = min(trends)
    max_kpi = max(trends)
    min_pos = trends.index(min_kpi)
    max_pos = trends.index(max_kpi)

    if min_kpi < 0:
        min_word = "decreasing"
    else:
        min_word = "increaing"
    
    if max_kpi > 0:
        max_word = "increaing"
    else: 
        max_word = "decreaing"

    print(
        f"Compared to the average of the last 30 days, the KPI '{all_kpis[min_pos]}' performed worst, {min_word} by {round((min_kpi)*100)}%\n"
        )
    print(f"The KPI '{all_kpis[max_pos]}' performed best, {max_word} by {round((max_kpi)*100)}%\n")

def main():
    """
    This function will execute all the other functions to run the program.
    """
    chosen_date = get_date()
    unchecked_30_day_kpis = last_30_day_data(chosen_date)
    check_30_day_data(unchecked_30_day_kpis)
    averages = get_30_day_averages(unchecked_30_day_kpis)
    str_kpis = get_kpis(chosen_date)
    int_kpis = [int(kpi) for kpi in str_kpis]
    #update_worksheet(int_kpis, chosen_date)
    trends = calculate_current_trends(int_kpis, averages)
    evaluate_trends(trends)

main()
