
import os
import requests
from dotenv import load_dotenv

# Load API credentials from .env
load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")


def test_cricbuzz_api():
    """Test the Cricbuzz API and inspect its response structure."""

    if not API_KEY or not API_HOST:
        print("ERROR: Check RAPIDAPI_KEY and RAPIDAPI_HOST in .env")
        return

    url = f"https://{API_HOST}/matches/v1/live"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST,
    }

    try:
        print("Connecting to Cricbuzz API...")

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        print("HTTP status:", response.status_code)

        if not response.ok:
            print("API request failed.")
            print("Response:", response.text[:500])
            return

        data = response.json()

        print("\nAPI connection successful!")
        print("Response type:", type(data).__name__)

        if not isinstance(data, dict):
            print("Unexpected response format.")
            return

        # Display top-level response fields
        print("\nTop-level keys:", list(data.keys()))

        # Inspect match types
        type_matches = data.get("typeMatches", [])

        print("Number of match types:", len(type_matches))

        for match_type in type_matches[:3]:
            if not isinstance(match_type, dict):
                continue

            print("\nMatch type:", match_type.get("matchType"))

            series_matches = match_type.get("seriesMatches", [])

            print("Number of series groups:", len(series_matches))

            # Inspect a maximum of two series groups
            for series in series_matches[:2]:
                if isinstance(series, dict):
                    print("Series group keys:", list(series.keys()))

                    # Inspect the nested match structure
                    series_wrapper = series.get("seriesAdWrapper", {})

                    if isinstance(series_wrapper, dict):
                        print(
                            "Series name:",
                            series_wrapper.get("seriesName")
                        )

                        matches = series_wrapper.get("matches", [])
                        print("Matches in series:", len(matches))

                        for item in matches[:2]:
                            if isinstance(item, dict):
                                match_info = item.get("matchInfo", {})

                                if isinstance(match_info, dict):
                                    print(
                                        "Match:",
                                        match_info.get("matchDesc"),
                                        "| Status:",
                                        match_info.get("status")
                                    )

        print("\nAPI inspection completed.")

    except requests.exceptions.Timeout:
        print("ERROR: The API request timed out.")

    except requests.exceptions.RequestException as error:
        print("ERROR: Network or API request failed:", error)

    except ValueError:
        print("ERROR: The API response was not valid JSON.")


if __name__ == "__main__":
    test_cricbuzz_api()
