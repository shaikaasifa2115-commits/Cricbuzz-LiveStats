
from database import get_connection
from scorecard_service import get_scorecard


def save_player_stats(match_id, scorecard_data):
    """Save players and their batting/bowling stats for one match."""

    if not scorecard_data:
        print("No scorecard data received.")
        return False

    innings_list = scorecard_data.get("scorecard", [])

    if not isinstance(innings_list, list) or not innings_list:
        print("No innings available for this match.")
        return False

    connection = get_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        for innings in innings_list:
            team_name = innings.get("batteamname", "")

            # Save batting players and their statistics.
            for player in innings.get("batsman", []):
                player_id = player.get("id")
                player_name = player.get("name")

                if not player_id or not player_name:
                    continue

                cursor.execute(
                    """
                    INSERT INTO players (
                        player_id, player_name, team_name
                    )
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        player_name = VALUES(player_name),
                        team_name = VALUES(team_name)
                    """,
                    (int(player_id), player_name, team_name),
                )

                cursor.execute(
                    """
                    INSERT INTO player_match_stats (
                        player_id, match_id, runs, balls_faced,
                        strike_rate
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        runs = VALUES(runs),
                        balls_faced = VALUES(balls_faced),
                        strike_rate = VALUES(strike_rate)
                    """,
                    (
                        int(player_id),
                        int(match_id),
                        int(player.get("runs") or 0),
                        int(player.get("balls") or 0),
                        float(player.get("strkrate") or 0),
                    ),
                )

            # Save bowlers and their bowling statistics.
            for player in innings.get("bowler", []):
                player_id = player.get("id")
                player_name = player.get("name")

                if not player_id or not player_name:
                    continue

                cursor.execute(
                    """
                    INSERT INTO players (
                        player_id, player_name, team_name
                    )
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        player_name = VALUES(player_name)
                    """,
                    (int(player_id), player_name, ""),
                )

                cursor.execute(
                    """
                    INSERT INTO player_match_stats (
                        player_id, match_id, wickets,
                        overs_bowled, runs_conceded
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        wickets = VALUES(wickets),
                        overs_bowled = VALUES(overs_bowled),
                        runs_conceded = VALUES(runs_conceded)
                    """,
                    (
                        int(player_id),
                        int(match_id),
                        int(player.get("wickets") or 0),
                        float(player.get("overs") or 0),
                        int(player.get("runs") or 0),
                    ),
                )

        connection.commit()
        print(f"Player statistics saved for match {match_id}.")
        return True

    except Exception as error:
        connection.rollback()
        print("Error saving player statistics:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


if __name__ == "__main__":
    match_id = input("Enter a match ID: ").strip()

    if not match_id.isdigit():
        print("Please enter a numeric match ID.")
    else:
        scorecard = get_scorecard(match_id)

        if scorecard:
            save_player_stats(match_id, scorecard)
