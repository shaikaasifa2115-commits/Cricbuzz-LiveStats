
import time

from database import get_connection
from scorecard_service import get_scorecard
from player_stats_service import save_player_stats


def get_match_ids():
    """Get all match IDs stored in MySQL."""

    connection = get_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT match_id FROM matches ORDER BY match_id")
        return [row[0] for row in cursor.fetchall()]

    except Exception as error:
        print("Could not load match IDs:", error)
        return None

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def main():
    match_ids = get_match_ids()

    if match_ids is None:
        print("Could not connect to the database.")
        return

    if not match_ids:
        print("No matches found. Run python sync_matches.py first.")
        return

    print(f"Found {len(match_ids)} matches in MySQL.\n")

    successful = 0
    skipped = 0

    for index, match_id in enumerate(match_ids, start=1):
        print(f"[{index}/{len(match_ids)}] Match ID: {match_id}")

        scorecard = get_scorecard(match_id)

        if scorecard is None or not scorecard.get("scorecard"):
            print("No scorecard available. Skipping.\n")
            skipped += 1
            continue

        if save_player_stats(match_id, scorecard):
            successful += 1
        else:
            skipped += 1

        print()

        # Avoid sending requests too rapidly.
        if index < len(match_ids):
            time.sleep(1)

    print("=" * 40)
    print("Player statistics sync finished.")
    print("Successful matches:", successful)
    print("Skipped or failed matches:", skipped)
    print("=" * 40)


if __name__ == "__main__":
    main()
