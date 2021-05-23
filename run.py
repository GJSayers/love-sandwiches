import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    Get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")
        data_str = input("Enter your data here: ")
        print(f"The data provided is {data_str}")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is vaild!")
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, converst all string values into integers.
    Raises ValueError if strings cannot be converted to int,
    or if ther are not 6 values exactly
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Works out howmany sadwiches are left at the end of the day.
    positive numbers inicate wastage.
    negative numbers indicate extra sanwiches made to order.
    """
    print("Updating surplus figures...")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
        
    return surplus_data
    

def update_surplus_worksheet(surplus_data):
    """
    Update surplus worksheet, add new row with the list data provided.
    """
    print("Updating surplus worksheet...")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(surplus_data)
    print("Surplus worksheet updated successfully.\n")


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    surplus_data = [int(num) for num in new_surplus_data]
    update_surplus_worksheet(surplus_data)

print("Welcome to love sandwiches data automation")
main()
