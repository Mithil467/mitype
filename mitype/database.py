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

    db_file_name = "data.db"

    module_path = os.path.abspath(__file__)

    last_index = 0

    slash_characters = ("/", "\\")

    for idx, character in enumerate(module_path):
        if character in slash_characters:
            last_index = idx

    db_directory_path = module_path[: last_index + 1]

    db_file_path = db_directory_path + db_file_name

    return db_file_path


def search(entry_id):
    """Fetch row from data.db database.

    Args:
        entry_id (int): The unique ID of database entry.

    Returns:
        list: The text corresponding to the entry_id.
    """
    path_str = directory_path()

    conn = sqlite3.connect(path_str)
    cur = conn.cursor()
    cur.execute("SELECT txt FROM data where id=?", (entry_id,))

    rows = cur.fetchall()
    conn.close()

    text = rows[0][0]

    return text
