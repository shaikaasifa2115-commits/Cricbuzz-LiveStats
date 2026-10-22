
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_db_config():
    """Use Aiven on Streamlit Cloud and local MySQL on your computer."""
    try:
        import streamlit as st

        if "mysql" in st.secrets:
            mysql_secrets = st.secrets["mysql"]

            return {
                "host": mysql_secrets["host"],
                "port": int(mysql_secrets["port"]),
                "user": mysql_secrets["user"],
                "password": mysql_secrets["password"],
                "database": "cricbuzz_livestats",
                "ssl_ca": mysql_secrets["ssl_ca"],
            }
    except (ImportError, FileNotFoundError):
        pass

    return {
        "host": "localhost",
        "user": "root",
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": "cricbuzz_livestats",
    }


DB_CONFIG = get_db_config()


def get_connection():
    """Connect Python to the MySQL database."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as error:
        print("MySQL connection error:", error)
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
            match_id,
            series_name,
            match_type,
            match_description,
            team1,
            team2,
            venue,
            city,
            match_status,
            start_date
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
