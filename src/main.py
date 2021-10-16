# Local files
from scholars import get_stats

if __name__ == "__main__":

    # Update the spreadsheet
    spreadsheets = ["Scholar Stats", "Scholar Stats Winston"]
    for s in spreadsheets:
        get_stats(s)

    # Every 14th of the month pay the scholars their part

    # After that clear all except the 'Scholars' worksheet, unless there was an error
