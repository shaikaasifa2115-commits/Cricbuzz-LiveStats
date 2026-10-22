
from api_service import get_live_matches
from database import save_matches


def main():
    print("Fetching matches from Cricbuzz API...")

    matches = get_live_matches()

    if matches is None:
        print("Failed to fetch matches.")
        return

    if not matches:
        print("No matches returned by the API.")
        return

    print(f"Retrieved {len(matches)} matches.")
    print("\nSaving matches to MySQL...")

    if save_matches(matches):
        print("Database update completed!")
    else:
        print("Could not save matches to MySQL.")


if __name__ == "__main__":
    main()
