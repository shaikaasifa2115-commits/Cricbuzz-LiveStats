
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

BASE_URL = f"https://{API_HOST}" if API_HOST else None


def get_live_matches():
    """Fetch live matches from the Cricbuzz API."""

    if not API_KEY or not API_HOST:
        print("Error: Check API settings in your .env file.")
        return None

    url = f"{BASE_URL}/matches/v1/live"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST,
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()

        matches = []

        for match_type in data.get("typeMatches", []):
            category = match_type.get("matchType", "")

            for series in match_type.get("seriesMatches", []):
                wrapper = series.get("seriesAdWrapper", {})

                if not isinstance(wrapper, dict):
                    continue

                for item in wrapper.get("matches", []):
                    info = item.get("matchInfo", {})

                    if not isinstance(info, dict):
                        continue

                    team1 = info.get("team1") or {}
                    team2 = info.get("team2") or {}
                    venue_info = info.get("venueInfo") or {}

                    matches.append({
                        "match_id": info.get("matchId"),
                        "series_name": wrapper.get("seriesName", ""),
                        "match_type": category,
                        "match_description": info.get("matchDesc", ""),
                        "team1": team1.get("teamName", ""),
                        "team2": team2.get("teamName", ""),
                        "venue": venue_info.get("ground", ""),
                        "city": venue_info.get("city", ""),
                        "match_status": info.get("status", ""),
                        "start_date": info.get("startDate", ""),
                    })

        return matches

    except requests.exceptions.RequestException as error:
        print("Cricbuzz API request failed:", error)
        return None
    except (ValueError, TypeError, AttributeError) as error:
        print("Could not process API response:", error)
        return None


if __name__ == "__main__":
    result = get_live_matches()

    if result is None:
        print("Could not retrieve matches.")
    elif not result:
        print("No live matches returned.")
    else:
        print(f"Successfully retrieved {len(result)} matches.\n")

        for match in result[:5]:
            print(
                f"{match['team1']} vs {match['team2']} | "
                f"{match['match_description']} | "
                f"{match['match_status']}"
            )
