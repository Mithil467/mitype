"""Handle with user history."""

import csv
import os
import time
from datetime import date


def history_file_absolute_path():
    """Get full path of history file.

    This is required for later reading or modifying records from history file.

    Returns:
        str: The path of history file.
    """
    history_filename = ".mitype_history.csv"
    history_path = os.path.join(os.path.expanduser("~"), history_filename)

    return history_path


def show_history(number_of_records):
    """Print records from history

    Defaults to -1 if argument value not provided on command line.

    Args:
        number_of_records (int): Number of last records to print.
    """
    history_file_path = history_file_absolute_path()

    if not os.path.exists(history_file_path):
        print("0 records found")
        return

    file = open(history_file_path)

    history_reader = csv.reader(file)
    next(history_reader)

    data = list(history_reader)
    total_records = len(data)

    if number_of_records <= -1 or number_of_records >= total_records:
        number_of_records = total_records

    print("Last", number_of_records, "records:")

    print("ID\tWPM\tDATE\t\tTIME")

    start_count = 0
    if number_of_records < total_records and number_of_records != -1:
        start_count = total_records - number_of_records
    for i in range(start_count, total_records):
        formatted_row_data = "\t".join(str for str in data[i])
        print(formatted_row_data)


def save_history(text_id, current_speed_wpm, accuracy):
    """Save test stats to history file.

    Args:
        text_id (int): Row identifier of database text loaded.
        current_speed_wpm (float): Speed result from test.
        accuracy (string): Accuracy result from test.
    """
    history_path = history_file_absolute_path()

    if not os.path.isfile(history_path):
        row = ["ID", "WPM", "DATE", "TIME", "ACCURACY"]
        history = open(history_path, "ab")
        csv_history = csv.writer(history)
        csv_history.writerow(row)
        history.close()

    history = open(history_path, "ab")
    csv_history = csv.writer(history)

    current_time = time.strftime("%H:%M:%S", time.localtime())

    test_data = [
        text_id,
        current_speed_wpm,
        date.today(),
        current_time,
        accuracy,
    ]
    csv_history.writerow(test_data)

    history.close()
