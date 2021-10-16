# Imports
# > Standard library
import requests
import datetime
import threading

# 3rd party dependencies
import pandas as pd
import gspread
import gspread_dataframe as gd

# Local files
from helper import ws_df, add_worksheet, gc
from winrate import get_winrate
from overview import update_overview, update_sheet


def get_stats(spreadsheet_name):
    """ Iterates over dictionary of scholars, set in scholar_info.py """

    # Set locals
    daily_slp = 0
    total_slp = 0
    total_scholar_share = 0
    total_average = 0
    new_update = False

    today = datetime.datetime.today().strftime("%Y-%m-%d")
    yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )

    # Add date to scholar_dict
    scholar_dict = {"Date": today}

    scholar_info = get_scholars(spreadsheet_name)

    # Get all addresses and join together as a string seperated by commas
    together = ",".join(scholar_info["Address"].tolist())

    # Call all addresses at once and retreive json
    response = requests.get(
        "https://game-api.axie.technology/api/v1/" + together
    ).json()

    # Iterate over returned dict
    for address, wallet_data in response.items():
        # Address is the ronin address
        # Data is dictionary that is returned from API.

        # Name is the name of the Ronin account
        scholar_name = wallet_data.get("name")

        # Convert to datetime
        updated_on = datetime.datetime.utcfromtimestamp(
            wallet_data["cache_last_updated"] / 1000
        ).strftime("%m-%d, %H:%M")
        last_claim = datetime.datetime.utcfromtimestamp(
            wallet_data["last_claim"]
        ).strftime("%m-%d")

        # Get all the important info
        data = [
            {
                "Date": today,
                "In Game SLP": wallet_data["in_game_slp"],
                "Ronin SLP": wallet_data["ronin_slp"],
                "Total SLP": wallet_data["total_slp"],
                "Rank": wallet_data["rank"],
                "MMR": wallet_data["mmr"],
                "Last Claim": last_claim,
                "Next Claim": datetime.datetime.utcfromtimestamp(
                    wallet_data["next_claim"]
                ).strftime("%m-%d"),
                "Updated On": updated_on,
            }
        ]

        # Make a df and set today's date as index
        df = pd.DataFrame(data).set_index("Date")

        # Open a specific worksheet, worksheet for every account
        try:
            ws = gc.open(spreadsheet_name).worksheet(scholar_name)

        # If it does not exist, make one
        except gspread.exceptions.WorksheetNotFound:
            ws = add_worksheet(scholar_name, spreadsheet_name)

        # Get the existing worksheet as dataframe
        existing = ws_df(ws)

        # Read the scholar split, using account address
        split = scholar_info.loc[scholar_info["Address"] == address]["Split"].tolist()[
            0
        ]

        # If last existing == same updated on do nothing
        if not existing.empty:
            if existing.tail(1)["Updated On"].tolist()[0] == updated_on:
                print("No updates available for: " + scholar_name)
                daily_slp += existing.tail(1)["SLP Today"].tolist()[0]
                scholar_dict[scholar_name] = existing.tail(1)["SLP Today"].tolist()[0]
                total_slp += existing.tail(1)["Total SLP"].tolist()[0]
                # Read their split %
                total_scholar_share += existing.tail(1)["Total SLP"].tolist()[0] * split
                total_average += existing["SLP Today"].mean() / len(scholar_info)
                continue

        new_update = True

        # Add win data of today
        df = pd.concat([df, get_winrate(address)], axis=1)

        # Calculate difference in days between last existing row and today
        last_date = datetime.datetime.strptime(
            existing.tail(1).index.values[0], "%Y-%m-%d"
        )
        day_diff = (datetime.datetime.now() - last_date).days

        # Set SLP difference to today
        slp_diff = df.loc[today]["In Game SLP"]

        # Calculate difference between last row and today
        if day_diff > 0:
            old_slp = existing.tail(1)["In Game SLP"]

            # Get average if there is a new date
            if old_slp < slp_diff:
                slp_diff = (df.loc[today]["In Game SLP"] - old_slp) / day_diff

            # Fill up dates that have nothing with slp_diff
            # NOT YET IMPLEMENTED

        # Update SLP today, cannot be negative
        df["SLP Today"] = slp_diff

        # Overwrite if the index of today exists
        if today in existing.index:
            # Overwrite index of today
            existing.loc[today] = df.loc[today]
            combined = existing

        # Append dataframe to it
        else:
            combined = existing.append(df)

        # Update locals, for overview
        daily_slp += slp_diff
        scholar_dict[scholar_name] = slp_diff

        total_slp += df.loc[today]["Total SLP"]
        total_scholar_share += df.loc[today]["Total SLP"] * split

        # Update "Daily Average" for today
        if existing.empty:
            # Calculate days passed since last claim, needs year for some reason
            this_year = str(datetime.datetime.today().year)
            days_passed = (
                datetime.datetime.strptime(today, "%Y-%m-%d")
                - datetime.datetime.strptime(this_year + "-" + last_claim, "%Y-%m-%d")
            ).days
            average_slp = slp_diff / days_passed

        # Use old data
        else:
            # Calculate Average
            average_slp = combined["SLP Today"].mean()

        combined.loc[today, "Daily Average"] = average_slp

        # Add average for overview
        total_average += average_slp / len(scholar_info)

        # Upload it to worksheet
        gd.set_with_dataframe(ws, combined, include_index=True)
        print("Updated: " + scholar_name)

    # Update the overview
    if new_update:
        update_overview(
            today,
            daily_slp,
            total_slp,
            total_scholar_share,
            total_average,
            spreadsheet_name,
        )
        update_sheet(
            "Scholar Overview",
            pd.DataFrame([scholar_dict]).set_index("Date"),
            spreadsheet_name,
        )

    # Do this every 4 hours (minimum)
    threading.Timer(3600 * 4, get_stats, args=[spreadsheet_name]).start()


def get_scholars(spreadsheet_name):
    """ Simple function to read the "Scholars" worksheet and return the dataframe """

    ws = gc.open(spreadsheet_name).worksheet("Scholars")
    scholar_info = (
        gd.get_as_dataframe(ws).dropna(axis=0, how="all").dropna(axis=1, how="all")
    )

    # Replace ronin: with 0x for API
    scholar_info["Address"] = scholar_info["Address"].str.replace("ronin:", "0x")

    return scholar_info
