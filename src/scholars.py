# Imports
import math

# > Standard library
import requests
import datetime
import json

# 3rd party dependencies
import pandas as pd
import gspread
import gspread_dataframe as gd

# Local files
from helper import ws_df, add_worksheet, gc
from winrate import get_winrate
from overview import update_overview, update_sheet


def get_stats(spreadsheet_name, worksheet_name):
    """
    Reads the scholars from the Scholars spreadsheet
    Writes the scholars info in Scholar Stats + Manager name
    """

    print(f"Getting scholar stats at {datetime.datetime.now()}")

    today = datetime.datetime.today().strftime("%Y-%m-%d")

    scholar_info = get_scholars(spreadsheet_name, worksheet_name)
    managers = set(scholar_info["Manager"].tolist())

    # Get all addresses and join together as a string seperated by commas
    together = ",".join(scholar_info["Address"].tolist())

    # Call all addresses at once and retreive json
    response = requests.get(
        "https://game-api.axie.technology/api/v1/" + together
    ).json()

    df = pd.DataFrame(response).transpose()

    # Reset index and rename old index as addresses
    df = df.rename_axis("Address").reset_index()

    # Convert to datetime and string
    df["cache_last_updated"] = pd.to_datetime(
        df["cache_last_updated"], unit="ms"
    ).dt.strftime("%m-%d, %H:%M")
    df["last_claim"] = pd.to_datetime(df["last_claim"], unit="s").dt.strftime("%m-%d")
    df["next_claim"] = pd.to_datetime(df["next_claim"], unit="s").dt.strftime("%m-%d")

    df = df.rename(
        columns={
            "cache_last_updated": "Updated On",
            "in_game_slp": "In Game SLP",
            "ronin_slp": "Ronin SLP",
            "total_slp": "Total SLP",
            "rank": "Rank",
            "mmr": "MMR",
            "last_claim": "Last Claim",
            "next_claim": "Next Claim",
        }
    )

    # Add managers to df
    df = pd.merge(
        df, scholar_info[["Manager", "Address"]], left_index=False, right_index=False
    )

    # Add date
    df["Date"] = today

    for manager in managers:
        # Set variables for overview
        daily_slp = 0
        total_slp = 0
        total_scholar_share = 0

        scholar_dict = {}
        scholar_dict["Date"] = today

        # Open the spreadsheet
        try:
            sheet = gc.open(f"Scholar Stats {manager}")

        # If the spreadsheet does not exist, create it in folder specified in authentication.json
        except gspread.exceptions.SpreadsheetNotFound:
            with open("authentication.json") as f:
                data = json.load(f)
            sheet = gc.create(f"Scholar Stats {manager}", data["folder_id"])

        # Get scholars corresponding with this managers
        scholar_names = df.loc[df["Manager"] == manager]["name"].tolist()

        # Update every scholar
        for scholar_name in scholar_names:

            # Get the row from the df
            scholar_df = df.loc[df["name"] == scholar_name]

            # Set local variables
            address = scholar_df["Address"].tolist()[0]
            updated_on = scholar_df["Updated On"].tolist()[0]

            # Remove clutter
            scholar_df = scholar_df[
                [
                    "Date",
                    "In Game SLP",
                    "Ronin SLP",
                    "Total SLP",
                    "Rank",
                    "MMR",
                    "Last Claim",
                    "Next Claim",
                    "Updated On",
                ]
            ].set_index("Date")

            # Open a specific worksheet, worksheet for every account
            try:
                ws = sheet.worksheet(scholar_name)

            # If it does not exist, make one
            except gspread.exceptions.WorksheetNotFound:
                ws = add_worksheet(scholar_name, f"Scholar Stats {manager}")

            # Get the existing worksheet as dataframe
            existing = ws_df(ws)

            # Add win data of today, disabled for now
            # df = pd.concat([df, get_winrate(address)], axis=1)

            # Combine the dataframes
            combined = scholar_df.combine_first(existing)

            # Do calculations
            combined["SLP Today"] = combined["In Game SLP"].diff()

            # SLP Today cannot be negative
            combined.loc[combined["SLP Today"] < 0, "SLP Today"] = 0
            # combined["SLP Today"][combined["SLP Today"] < 0] = 0

            # Catch NaN
            gained = 0 if math.isnan(combined.tail(1)["SLP Today"].tolist()[0]) else combined.tail(1)["SLP Today"].tolist()[0]

            # Calculate average
            try:
                combined.loc[today, "Daily Average"] = combined["SLP Today"].mean().round()
            except AttributeError:
                combined.loc[today, "Daily Average"] = gained

            # Upload it to worksheet
            gd.set_with_dataframe(ws, combined, include_index=True)
            print("Updated: " + scholar_name)

            # Update variables for Overview
            daily_slp += gained

            new_slp = scholar_df["In Game SLP"].tolist()[0]
            total_slp += new_slp

            # Read the scholar split, using account address
            split = scholar_info.loc[scholar_info["Address"] == address][
                "Scholar Share"
            ].tolist()[0]
            total_scholar_share += split * new_slp

            # Save this in the dict
            scholar_dict[scholar_name] = gained

        # Update the overview of this manager
        update_overview(
            today,
            daily_slp,
            total_slp,
            total_scholar_share,
            daily_slp / len(scholar_names),
            f"Scholar Stats {manager}",
        )
        # Scholar Overview shows everyone's daily SLP
        update_sheet(
            "Scholar Overview",
            pd.DataFrame([scholar_dict]).set_index("Date"),
            f"Scholar Stats {manager}",
        )
        print(f"Updated {manager}'s overview")


def get_scholars(spreadsheet_name, worksheet_name):
    """Simple function to read the "Scholars" worksheet and return the dataframe"""

    # Open the worksheet of the specified spreadsheet
    ws = gc.open(spreadsheet_name).worksheet(worksheet_name)
    scholar_info = (
        gd.get_as_dataframe(ws).dropna(axis=0, how="all").dropna(axis=1, how="all")
    )

    # Replace ronin: with 0x for API
    scholar_info["Address"] = scholar_info["Address"].str.replace("ronin:", "0x")

    return scholar_info
