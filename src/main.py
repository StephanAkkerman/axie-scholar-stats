import threading
import time

# Local files
from scholars import get_stats


def update():

    spreadsheet = "Scholars"
    worksheet = "Scholars"
    
    # This should fix it getting stuck
    try:
        get_stats(spreadsheet, worksheet)
    except Exception as e:
        print(e)
        time.sleep(60*5)
        print("Restarting...")
        update()
    
    # Do this every 4 hours (minimum)
    threading.Timer(3600 * 4, update).start()


if __name__ == "__main__":

    # Update the spreadsheet
    update()

    # Delete every worksheet in Scholar Stats unless last_claim is later than now
