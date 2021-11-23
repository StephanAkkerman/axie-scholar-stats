import threading

# Local files
from scholars import get_stats


def update():

    spreadsheet = "Scholars"
    worksheet = "Scholars"
    get_stats(spreadsheet, worksheet)

    # Do this every 4 hours (minimum)
    # threading.Timer(3600 * 4, update).start()


if __name__ == "__main__":

    # Update the spreadsheet
    update()

    # Every 14th of the month pay the scholars their part
    # Delete every worksheet in Scholar Stats unless last_claim is later than now
