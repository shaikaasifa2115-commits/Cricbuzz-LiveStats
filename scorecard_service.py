
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")


def get_scorecard(match_id):
    """Fetch a scorecard from the Cricbuzz API."""

    if not API_KEY or not API_HOST:
        print("Error: Check API settings in .env.")
        return None

    url = f"https://{API_HOST}/mcenter/v1/{match_id}/scard"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST,
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            print("Unexpected API response.")
            return None

        return data

    except requests.exceptions.RequestException as error:
        print("Scorecard API request failed:", error)
        return None

    except ValueError as error:
        print("Invalid JSON response:", error)
        return None


def display_scorecard(data):
    """Print innings summaries, batting, and bowling tables."""

    if not data:
        print("No scorecard data available.")
        return

    print("\nMATCH STATUS:", data.get("status", "Unavailable"))

    innings_list = data.get("scorecard", [])

    if not isinstance(innings_list, list) or not innings_list:
        print("No innings scorecard is available.")
        return

    for number, innings in enumerate(innings_list, start=1):
        if not isinstance(innings, dict):
            continue

        team = innings.get("batteamname", "Unknown team")
        runs = innings.get("score", 0)
        wickets = innings.get("wickets", 0)
        overs = innings.get("overs", 0)
        run_rate = innings.get("runrate", 0)

        print(f"\n{'=' * 55}")
        print(f"INNINGS {number}: {team}")
        print(f"Score: {runs}/{wickets} in {overs} overs")
        print(f"Run rate: {run_rate}")
        print("=" * 55)

        batsmen = innings.get("batsman", [])

        if batsmen:
            print("\nBATTING")
            print(
                f"{'Player':<22} {'R':>4} {'B':>4} "
                f"{'4s':>4} {'6s':>4} {'SR':>7}"
            )

            for player in batsmen:
                name = player.get("name", "Unknown")
                print(
                    f"{name[:21]:<22} "
                    f"{player.get('runs', 0):>4} "
                    f"{player.get('balls', 0):>4} "
                    f"{player.get('fours', 0):>4} "
                    f"{player.get('sixes', 0):>4} "
                    f"{player.get('strkrate', 0):>7}"
                )

        bowlers = innings.get("bowler", [])

        if bowlers:
            print("\nBOWLING")
            print(
                f"{'Player':<22} {'O':>5} {'M':>3} "
                f"{'R':>4} {'W':>3} {'Econ':>7}"
            )

            for player in bowlers:
                name = player.get("name", "Unknown")
                print(
                    f"{name[:21]:<22} "
                    f"{player.get('overs', 0):>5} "
                    f"{player.get('maidens', 0):>3} "
                    f"{player.get('runs', 0):>4} "
                    f"{player.get('wickets', 0):>3} "
                    f"{player.get('economy', 0):>7}"
                )

        extras = innings.get("extras", {})

        if isinstance(extras, dict):
            print("\nExtras:", extras.get("total", 0))


if __name__ == "__main__":
    match_id = input("Enter a match ID: ").strip()

    if match_id.isdigit():
        scorecard_data = get_scorecard(match_id)
        display_scorecard(scorecard_data)
    else:
        print("Please enter a numeric match ID.")
