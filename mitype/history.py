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

    return os.path.join(os.path.expanduser("~"), history_filename)


def get_history_records(number_of_records):
    """Get records from history.

    Defaults to -1 if argument value not provided on command line.

    Args:
        number_of_records (int): Number of last records to print.
    Returns:
        list: A list of records. The len of this list is `number_of_records` or all records
    """
    history_file_path = history_file_absolute_path()

    if not os.path.exists(history_file_path):
        return []

    with open(history_file_path, encoding="utf-8") as file:
        history_reader = csv.reader(file)

        try:
            # Skip csv header
            next(history_reader)
        except StopIteration:
            # No header found on the file, meaning the file is empty
            return []

        data = list(history_reader)
        total_records = len(data)

        if number_of_records <= -1 or number_of_records >= total_records:
            number_of_records = total_records

        start_count = 0
        if number_of_records < total_records and number_of_records != -1:
            start_count = total_records - number_of_records
        return data[start_count:total_records]


def show_history(number_of_records):
    """Show records from history.

    Defaults to -1 if argument value not provided on command line.

    Args:
        number_of_records (int): Number of last records to print.
    """
    records = get_history_records(number_of_records)

    if len(records) == 0:
        print("0 records found")

    print("Last {} records:".format(len(records)))
    print("ID\tWPM\tDATE\t\tTIME\t\tACCURACY")
    for record in records:
        formatted_row_data = "\t".join(record)
        print(formatted_row_data + "%")


def save_history(text_id, current_speed_wpm, accuracy):
    """Save test stats to history file.

    Args:
        text_id (int): Row identifier of database text loaded.
        current_speed_wpm (float): Speed result from test.
        accuracy (str): Accuracy result from test.
    """
    history_path = history_file_absolute_path()

    file_exists = os.path.isfile(history_path)

    with open(history_path, mode="a", newline="", encoding="utf-8") as history:
        csv_history = csv.writer(history)

        if not file_exists:
            row = ["ID", "WPM", "DATE", "TIME", "ACCURACY"]
            csv_history.writerow(row)

        current_time = time.strftime("%H:%M:%S", time.localtime())

        test_data = [
            text_id,
            current_speed_wpm,
            date.today(),
            current_time,
            accuracy,
        ]
        csv_history.writerow(test_data)
