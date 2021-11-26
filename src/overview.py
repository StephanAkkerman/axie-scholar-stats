import gspread
import gspread_dataframe as gd
import pandas as pd

# Local files
from helper import ws_df, add_worksheet, gc, client


def update_sheet(ws_name, df, spreadsheet_name):
    """Updates the specified worksheet, using the data of df"""

    # Open the overview worksheet and make it a df
    try:
        ws = gc.open(spreadsheet_name).worksheet(ws_name)
    except gspread.exceptions.WorksheetNotFound:
        ws = add_worksheet(ws_name, spreadsheet_name)

    old_overview = ws_df(ws)

    # Overwrite whole sheet if it is empty
    if old_overview.empty:
        print("Empty existing dataframe for: " + ws_name)
        gd.set_with_dataframe(ws, df, include_index=True)

    # If that is not the case, get the old info
    else:
        # Last (and only) index of dataframe is today
        today = df.index[-1]

        if today in old_overview.index:
            # Overwrite index of today
            old_overview.loc[today] = df.loc[today]
            updated_overview = old_overview

        # Append dataframe to it
        else:
            updated_overview = old_overview.append(df)

        # Upload it to worksheet
        gd.set_with_dataframe(ws, updated_overview, include_index=True)


def update_overview(
    today, daily_slp, total_slp, lifetime_slp, total_scholar_share, total_average, spreadsheet_name
):
    """Updates the overview worksheet"""

    # SLP price
    SLP = float(client.get_avg_price(symbol="SLPUSDT")["price"])

    total_manager_share = total_slp - total_scholar_share

    # Make df, round $ to 2 decimals
    data = [
        {
            "Date": today,
            "Daily SLP": daily_slp,
            "Daily $": round(daily_slp * SLP, 2),
            "Daily Average SLP": int(total_average),
            "Total SLP": total_slp,
            "Total $": round(total_slp * SLP, 2),
            "Lifetime SLP": lifetime_slp,
            "Lifetime SLP $": round(lifetime_slp * SLP, 2),
            "Manager Share SLP": total_manager_share,
            "Manager Share $": round(total_manager_share * SLP, 2),
            "Scholar Share SLP": total_scholar_share,
            "Scholar Share $": round(total_scholar_share * SLP, 2),
            "SLP Price": str(round(SLP, 3)) + "$",
        }
    ]

    overview = pd.DataFrame(data).set_index("Date")

    update_sheet("Overview", overview, spreadsheet_name)
