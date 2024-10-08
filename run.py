import gspread
from google.oauth2.service_account import Credentials

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
        data_str = input("Enter your data here:\n")
    
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
# refactor the following two functions into one named update_worksheet()
# def update_sales_worksheet(data):
#     """
#     Update sales woeksheet, add new row with the list data provided
#     """
#     print("Updating sales worksheet...\n")
#     # now access the Google Sheet - create a new variable
#     sales_worksheet = SHEET.worksheet("sales")
#     # add a new row to the worksheet - gspread is helping us here
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated!\n")
    
# # create a function to update the surplus worksheet
# def update_surplus_data(surplus_data):
#     """
#     Update the surplus worksheet with the new surplus data.
#     This appends the surplus data to the surplus worksheet.
#     """
#     print("Updating surplus data in the spreadsheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(surplus_data)
#     print("Surplus data updated!\n")

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevent worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated!\n")


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

    surplus_data = [] # a place to put our surplus data
    for stock, sales in zip(stock_row, sales_row): # for loop to calculate data from two different lists
        surplus = int(stock) - sales
        surplus_data.append(surplus) # add to the surplus_data list
    
    return surplus_data

def get_last_5_entries_sales():
    """
    Collects columns of data from the sales worksheet, collecting
    the last 5 entries for eacj sandwich and returns the data as a list of lists
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:]) # slices the last 5 entries from our lists
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column] # coverts values into integers so we can do arithmetic
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data # and pass it back to where the function was called
    # and assign it a variable named stock_data

# this function works as is - the one below works the same but includes the 'data' parameter
# def get_stock_values():
#     """
#     Builds a dictionary with 'sandwich' keys and 'stock' values
#     """
#     stock = SHEET.worksheet("stock").get_all_values() # access the "stock" worksheet
#     keys = stock[0] # assign 1st row to keys
#     values = stock[-1] # assign last row to values
    
#     stock_dict = dict(zip(keys, values)) # use zip() to combine two lists into one object
#     print(stock_dict)

# this also works but has no variable named 'headings
# def get_stock_values(data):
#     """
#     Builds a dictionary with 'sandwich' keys and 'stock' values
#     """
#     keys = data[0] # assign 1st row to keys - the data here is what 
#     #has been passed when calling the function near the botton i.e. stock_values data
#     values = data[-1] # assign last row to values

#     stock_values = dict(zip(keys, values)) # use zip() to combine two lists into one object
#     print(f"Current stock: {stock_values}")
#     return stock_values

# wrap main function calls
def main():
    """
    Run all program functions.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")

    new_surplus_row = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_row, "surplus")

    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    return stock_data


print("Welcome to Love Sandwiches data automation.\n")
stock_data = main()

# student writes function
def get_stock_values(data):
    """
    Print out the calculated stock numbers for each sandwich type.
    """
    headings = SHEET.worksheet("stock").get_all_values()[0]

    # headings = SHEET.worksheet('stock').row_values(1)

    print("Make the following numbers of sandwiches for next market:\n")

    # new_data = {}
    # for heading, stock_num in zip(headings, data):
    #     new_data[heading] = stock_num
    # return new_data
    
    return {heading: data for heading, data in zip(headings, data)}
    
stock_values = get_stock_values(stock_data)
print(stock_values)