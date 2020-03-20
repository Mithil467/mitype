import os
import random
import sqlite3


def directory_path():
    """Get full path of directory where source files are stored.
    This is required for later fetching entry from data.db which is
    stored in same directory as app.

    Returns:
        string: The path of directory of source file.
    """
    path = os.path.abspath(__file__)
    last_index = 0
    slash_character1 = "\\"
    slash_character2 = "/"
    for idx, character in enumerate(path):
        if character in (slash_character1, slash_character2):
            last_index = idx
    return path[0 : last_index + 1]


def search(entry_id):
    """Fetch row from data.db database.

    Args:
        entry_id (int): The unique ID of database entry.

    Returns:
        list: The text corresponding to the entry_id.
    """
    path_str = directory_path() + "data.db"
    conn = sqlite3.connect(path_str)
    cur = conn.cursor()
    cur.execute("SELECT txt FROM data where id=?", (entry_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def generate():
    """Generate a random integer [1, number of database entries].
    This function later calls the 'search' function by passing the
    generated integer as 'entry_id'.
    """
    number_of_text_entries = 6000
    string = search(random.randrange(1, number_of_text_entries + 1))
    return string[0][0]
