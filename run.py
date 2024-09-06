import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

# define scope as a contstant variable (capital letters)
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    get sales figures from the user
    """

    # create a 'while' loop to prevent having to relaunch the programme
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be 6 numbers separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        # next use the input method to get our sales data from the terminal
        data_str = input("Enter your data here: ")
    
        # convert the user's string input data to a list 
        # and use the split() method - returns the broken up values as a list -  
        # to remove all the commas
        sales_data = data_str.split(",")

        if validate_data(sales_data): # if statement calls the validate_data() function and if there are no errors, returns True
            print("Data looks good")
            break

    # now return out validated sales_data from the get_sales_data() function
    return sales_data
        

# create a function to handle data validation - we need exactly 6 numbers
# call the validate_data() function in the get_sales_data() function above
def validate_data(values):
    """
    Inside the try, converts all string values to integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        # convert list of string data to integers
        [int(value) for value in values]
        # if the length of the list does not equal 6, show a custom error message
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required. You provided {len(values)}"
            )
        # only catches errors if they are ValueErrors -  an operation receives an argument with an inappropriate value - 
        # and places the input into a variable (e) - shorthand for 'error' - so we can then access details of the error
        
    except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
            return False # if error

    return True # if no error

# create a function to update the sales worksheet
def update_sales_worksheet(data):
    """
    Update sales woeksheet, add new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    # now access the Google Sheet - create a new variable
    sales_worksheet = SHEET.worksheet("sales")
    # add a new row to the worksheet - gspread is helping us here
    sales_worksheet.append_row(data)
    print("Sales worksheet updated!\n")
    

# create a function to calculate the surplus
def calculate_surplus_data(sales_row):
    """
    Compare sales with stock to calculate teh surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock sold out
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1] #access the last entry from our list - the most recent day's stock
    print(stock_row)

# wrap main function calls
def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

print("Welcome to Love Sandwiches Data Automation.")
main()
