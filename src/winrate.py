import requests
import datetime
import pandas as pd


def get_winrate(address):
    """Gets the winrate of a scholar using the battlelog API"""

    try:
        response = requests.get(
            "https://game-api.axie.technology/battlelog/" + address
        ).json()

        df = pd.DataFrame(response[0]["items"])
        df = df[["winner", "created_at", "first_client_id", "second_client_id"]]

        total_wins_data = get_wins(df, address)

        # Get todays data
        today = datetime.datetime.today()
        yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime(
            "%Y-%m-%d %H:%M"
        )
        today_df = df[
            (df["created_at"] > yesterday)
            & (df["created_at"] <= today.strftime("%Y-%m-%d %H:%M"))
        ]

        daily_wins_data = get_wins(today_df, address)

        # Save this in a dict that will be returned
        wins_data = {
            "Date": today.strftime("%Y-%m-%d"),
            "Weekly winrate": [total_wins_data["Winrate"]],
            "Weekly games": total_wins_data["Games_played"],
            "Daily winrate": daily_wins_data["Winrate"],
            "Daily games": daily_wins_data["Games_played"],
        }

    except Exception as e:
        print("Error with getting winrate")

        wins_data = {
            "Date": today.strftime("%Y-%m-%d"),
            "Weekly winrate": "ERROR",
            "Weekly games": "ERROR",
            "Daily winrate": "ERROR",
            "Daily games": "ERROR",
        }

    wins_df = pd.DataFrame(wins_data).set_index("Date")
    return wins_df


def get_wins(df, address):
    """Simple function to get wins"""

    wins = 0
    for index, row in df.iterrows():
        if row["first_client_id"] == address:
            if row["winner"] == 0:
                wins += 1
        else:
            if row["winner"] == 1:
                wins += 1

    return_dict = {
        "Games_played": len(df),
        "Winrate": "Unknown"
        if len(df) == 0
        else str(round(wins / len(df) * 100, 2)) + "%",
    }
    return return_dict
