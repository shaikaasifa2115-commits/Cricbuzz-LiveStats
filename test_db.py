
from database import get_connection


def test_database():
    connection = get_connection()

    if connection is None:
        print("Database connection failed. Check your .env settings.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE(), VERSION()")
        result = cursor.fetchone()

        print("Database connection successful!")
        print("Database:", result[0])
        print("MySQL version:", result[1])

        cursor.close()

    finally:
        connection.close()


if __name__ == "__main__":
    test_database()
