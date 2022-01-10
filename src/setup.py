# Standard libraries
import gspread
from main import update

# Login using the .json file
gc = gspread.service_account(filename="authentication.json")

def create_scholars_sheet():
    """Create a new Scholars spreadsheet"""
    try:
        sheet = gc.open("Scholar Stats")
        print("Found existing Scholar Stats spreadsheet")
    except gspread.exceptions.SpreadsheetNotFound:
        sheet= gc.create("Scholars Stats", folder_id)
        print("Creating Scholar Stats spreadsheet")
        
    # Create the worksheets
    try:
        ws = sheet.worksheet("Scholars")
        print("Found existing Scholars worksheet")
    # If it does not exist, make one
    except gspread.exceptions.WorksheetNotFound:
        ws = gc.open("Scholars").add_worksheet(title="Scholars", rows="100", cols="20")
        print("Creating Scholars worksheet")

    # Add the default first row
    ws.update(
        "A1:F1",
        [
            [
                "Scholar Name",
                "Manager",
                "Scholar Share",
                "Address",
            ]
        ],
    )

if __name__ == "__main__":

    # Request the folder id
    folder_id = input(
        "Please paste the folder url that you shared with the bot, e.g. https://drive.google.com/drive/folders/abcdlakfdj:\n"
    )

    # Get everything after the last /
    folder_id = folder_id.split("/")[-1]

    # Create the Scholars spreadsheet + worksheet
    create_scholars_sheet()
    
    print("Please fill in the information in the Scholars worksheet, located in Scholar Stats spreadsheet")

    print("If you filled in the information, please run: python src/main.py to update the Scholar Stats sheet")