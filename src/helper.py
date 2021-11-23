import gspread
import gspread_dataframe as gd
from binance import Client

# Ready the Binance client, for SLP prices
client = Client()

# Login using the .json file
gc = gspread.service_account(filename="authentication.json")


def ws_df(ws):
    """Gets worksheet from Google Sheets and returns df"""

    # Get existing info of worksheet
    existing = gd.get_as_dataframe(ws)

    # Drop rows and collumns filled with NaN
    existing = existing.dropna(axis=0, how="all").dropna(axis=1, how="all")

    # If it is not empty, set date as index
    if not existing.empty:
        existing.set_index("Date", inplace=True)

    return existing


def add_worksheet(name, spreadsheet_name):
    """Adds a worksheet to spreadsheet"""

    ws = gc.open(spreadsheet_name).add_worksheet(title=name, rows="100", cols="20")
    return ws
