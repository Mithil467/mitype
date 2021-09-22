"""Deals with fetching texts from database."""

import os
import sqlite3


def database_file_absolute_path():
    """Get full path of directory where source files are stored.

    This is required for later fetching entry from data.db which is
    stored in same directory as app.

    Returns:
        str: The path of directory of source file.
    """
    database_filename = "data.db"
    database_directory_absolute_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        database_directory_absolute_path,
        database_filename,
    )


def fetch_text_from_id(serial_id):
    """Fetch row from data.db database.

    Args:
        serial_id (int): The unique ID of database entry.

    Returns:
        str: The text corresponding to the entry_id.
    """
    database_file = database_file_absolute_path()
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # For details related to the database schema check CONTRIBUTING.md
    cursor.execute("SELECT txt FROM data where id=?", (serial_id,))
    text = cursor.fetchone()[0]
    connection.close()

    return text
