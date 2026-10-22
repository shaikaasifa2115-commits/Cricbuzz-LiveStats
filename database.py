
import os
import mysql.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_db_config():
    """Read database settings from Streamlit Secrets or local .env."""

    try:
        secrets = st.secrets
        host = secrets.get("MYSQL_HOST", os.getenv("MYSQL_HOST", "localhost"))
        user = secrets.get("MYSQL_USER", os.getenv("MYSQL_USER", "root"))
        password = secrets.get("MYSQL_PASSWORD", os.getenv("MYSQL_PASSWORD"))
        port = int(secrets.get("MYSQL_PORT", os.getenv("MYSQL_PORT", "3306")))
        database = secrets.get(
            "MYSQL_DATABASE",
            os.getenv("MYSQL_DATABASE", "cricbuzz_livestats"),
        )
    except Exception:
        host = os.getenv("MYSQL_HOST", "localhost")
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD")
        port = int(os.getenv("MYSQL_PORT", "3306"))
        database = os.getenv("MYSQL_DATABASE", "cricbuzz_livestats")

    if not password:
        raise ValueError("MYSQL_PASSWORD is missing from environment settings.")

    config = {
        "host": host,
        "user": user,
        "password": password,
        "port": port,
        "database": database,
        "connection_timeout": 15,
    }

    # Enable SSL for remote databases such as Aiven.
    if host not in ("localhost", "127.0.0.1"):
        config["ssl_disabled"] = False

    return config


def get_connection():
    """Connect Python to MySQL and log detailed connection errors."""

    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        print("MySQL connection successful!")
        return connection

    except Exception as error:
        # Do not print passwords or other secret values.
        print(
            f"MySQL connection failed: "
            f"{type(error).__name__}: {error}"
        )
        return None


def save_matches(matches):
    """Insert new matches or update existing matches."""

    if not matches:
        print("No matches to save.")
        return False

    connection = get_connection()

    if connection is None:
        return False

    query = """
        INSERT INTO matches (
            match_id, series_name, match_type, match_description,
            team1, team2, venue, city, match_status, start_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            series_name = VALUES(series_name),
            match_type = VALUES(match_type),
            match_description = VALUES(match_description),
            team1 = VALUES(team1),
            team2 = VALUES(team2),
            venue = VALUES(venue),
            city = VALUES(city),
            match_status = VALUES(match_status),
            start_date = VALUES(start_date)
    """

    cursor = None

    try:
        cursor = connection.cursor()

        values = [
            (
                int(match["match_id"]),
                match.get("series_name"),
                match.get("match_type"),
                match.get("match_description"),
                match.get("team1"),
                match.get("team2"),
                match.get("venue"),
                match.get("city"),
                match.get("match_status"),
                str(match.get("start_date") or ""),
            )
            for match in matches
            if match.get("match_id") is not None
        ]

        if not values:
            print("No valid match IDs found.")
            return False

        cursor.executemany(query, values)
        connection.commit()

        print(f"Successfully saved {len(values)} matches to MySQL.")
        return True

    except (mysql.connector.Error, ValueError, TypeError) as error:
        connection.rollback()
        print("Error saving matches:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()
