import gspread
from google.oauth2.service_account import Credentials
import time
import sys

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
# The setup of the connection between Python and the Google sheet
# was done with the help of the LoveSandwiches project.


def delay_print(s):
    """
    This function prints the text letter by letter.
    """
    # This function's code was completely copied from 
    # https://stackoverflow.com/questions/9246076/how-to-print-one-character-at-a-time-on-one-line
    # time.sleep was also used more throughout the code
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.035)
    print()


delay_print("""Welcome to this Python program, which captures the most recent
Preglife Connect KPIs and analyzes the current trends for you!\n""")


def get_date():
    """
    This function is used to get the date from the user
    for which the KPIs should be entered into the sheet.
    """
    while True:
        time.sleep(1)
        print(
            "For which date would you like to enter "
            "the KPIs of the Preglife Connect app?\n"
        )
        time.sleep(2)
        print(
            "Please enter the date in the following format: "
            "DD/MM/YYYY, e.g. 22/02/2022\n"
        )
        time.sleep(2)
        date_input = input("Enter the date here:\n")

        if validate_date(date_input):
            delay_print("Thank you for entering a valid date.\n")
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
        delay_print("That was not a valid date, please try again.\n")
        return False


def last_30_day_data(date):
    """
    This function grabs the values from the last 30 days of each KPI
    from the worksheet.
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
    is_all_empty = []
    for val in values[0]:
        if val == "":
            is_all_empty.append(val)
    if len(is_all_empty) == 30:
        delay_print(
            "You did not enter any values in the last 30 days. "
            "You need to enter values for an earlier date first.\n"
            )
        main()
        return False

    if "" in values[0]:
        delay_print(
            "It seems like you have missed to enter some values "
            "on recent dates. Please enter data consistently in the "
            "future in order to not distort the following calculations.\n"
        )
    else:
        delay_print("Good job, you have entered data for the last 30 days!\n")
    return True


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
    time.sleep(1)
    # Thanks to my colleague Daniel to give me the idea to
    # use a while loop in this particular way
    while len(prompts) != len(kpi_list):
        kpi_input = input(prompts[i])
        if validate_kpi(kpi_input):
            kpi_list.append(kpi_input)
            i += 1
    delay_print("Thanks for entering valid data!\n")
    time.sleep(1)
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
            raise ValueError()
    except ValueError:
        print("Your input must be a positive, whole number!\n")
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
    delay_print("Worksheet successfully updated.\n")


def calculate_current_trends(kpis, averages):
    """
    This function will calculate how the KPIs have developed compared
    to the average of the last 30 days.
    """
    trends_list = [(kpi/average)-1 for kpi, average in zip(kpis, averages)]
    return trends_list


def evaluate_min_max(trends):
    """
    This function will evaluate the previously calculated trends
    of KPI development and will give the user relevant
    information about the best and worst KPI.
    """
    all_kpis = (
        ["App Opens", "Screen Views", "Ad Views", "Threads Created", "Swipes"]
    )
    min_kpi = min(trends)
    max_kpi = max(trends)
    min_pos = trends.index(min_kpi)
    max_pos = trends.index(max_kpi)

    if min_kpi < 0:
        min_word = "decreasing"
        trend_word_min = "worst"
    else:
        min_word = "increaing"
        trend_word_min = "'worst'"

    if max_kpi > 0:
        max_word = "increaing"
        trend_word_max = "best"

    else:
        max_word = "decreaing"
        trend_word_max = "'best'"

    delay_print(
        f"Compared to the average of the last 30 days, the KPI "
        f"'{all_kpis[min_pos]}' performed {trend_word_min}, "
        f"{min_word} by {round((min_kpi)*100)}%\n"
        )
    time.sleep(1)
    delay_print(
        f"Compared to the average of the last 30 days, the KPI "
        f"'{all_kpis[max_pos]}' performed {trend_word_max}, "
        f"{max_word} by {round((max_kpi)*100)}%\n"
        )


def evaluate_all_kpis(values):
    """
    This function will evaluate the previously calculated trends
    of KPI development and will give the user relevant
    information about how many KPIs were improved, if any.
    """
    positive_values = [val for val in values if val > 0]
    if len(positive_values) == 5:
        delay_print(
            "Great job, all 5 KPIs improved "
            "compared to last month's average.\n"
            )
    elif len(positive_values) >= 3:
        delay_print(
            "Very good, more than half of the 5 KPIs improved "
            "compared to last month's average.\n"
            )
    elif len(positive_values) >= 1:
        delay_print(
            "Not so bad, you increased at least some KPIs "
            "compared to last month's average.\n"
            )
    else:
        delay_print(
            "Keep on fighting, no KPIs improved "
            "compared to last month's average, but you can turn it around!\n"
            )


def main():
    """
    This function will execute all the other functions to run the program.
    """
    chosen_date = get_date()
    unchecked_30_day_kpis = last_30_day_data(chosen_date)
    valid = check_30_day_data(unchecked_30_day_kpis)
    # Thanks to my colleague Daniel, who helped me to figure out how torun the following 
    # code only if 'valid' was true, effectively checking that the program has
    # user data from at least 1 of the last 30 days to work with.
    if valid:
        averages = get_30_day_averages(unchecked_30_day_kpis)
        str_kpis = get_kpis(chosen_date)
        int_kpis = [int(kpi) for kpi in str_kpis]
        update_worksheet(int_kpis, chosen_date)
        trends = calculate_current_trends(int_kpis, averages)
        evaluate_min_max(trends)
        evaluate_all_kpis(trends)
        time.sleep(1)
        delay_print("Thank you for entering the KPI data. See you tomorrow :)")


main()
