"""
Start of app.

Parses command line arguments and decides and fills text accordingly.
"""

import argparse
import os
import random
import sys
import csv
import ctypes

import mitype
import mitype.database


def main():
    """Parse CLI arguments and return practice text.

    Returns:
        str: Text content to have user attempt to type.
    """
    opt = parse_arguments()
    if opt.version:
        display_version()
        sys.exit(0)

    elif opt.history:
        show_history(opt.history)
        sys.exit(0)

    elif opt.file:
        text = load_text_from_file(opt.file)

    elif opt.id:
        text = load_from_database(opt.id)

    elif opt.difficulty:
        text = load_based_on_difficulty(opt.difficulty)

    else:
        text = load_based_on_difficulty()

    return text


def parse_arguments():
    """Parse command line arguments.

    Returns:
        str: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Process mitype command line arguments"
    )

    parser.add_argument(
        "-V",
        "--version",
        default=False,
        action="store_true",
        help="Show mitype version",
    )

    parser.add_argument(
        "-f",
        "--file",
        metavar="FILENAME",
        default=None,
        type=str,
        help="File to use text from as sample text",
    )

    parser.add_argument(
        "-i",
        "--id",
        metavar="id",
        default=None,
        type=int,
        help="ID to retrieve text from database",
    )

    parser.add_argument(
        "-d",
        "--difficulty",
        metavar="N",
        default=2,
        type=int,
        help="Choose difficulty within range 1-5",
    )

    parser.add_argument(
        "-H",
        "--history",
        nargs='?',
        default=0,
        const=-1,
        help="Show mitype score history",
    )

    opt = parser.parse_args()
    return opt


def display_version():
    """Display version."""
    print("Mitype version %s" % mitype.__version__)


def load_text_from_file(file_path):
    """Load file contents.

    Args:
        file_path (string): Full path to text to load.

    Returns:
        (str, str): Tuple of text content followed by file path.
    """
    if os.path.isfile(file_path):
        text = open(file_path).read()
        filename = os.path.basename(file_path)
        return text, filename

    print("Cannot open file -", file_path)
    sys.exit(0)


def load_from_database(text_id):
    """Load given text from database with given id.

    Args:
        text_id (int): Row identifier of database text to load.

    Returns:
        (str, int): Tuple of text content followed by DB row identifier.
    """
    row_count = 6000
    if 1 <= text_id <= row_count:
        text = mitype.database.fetch_text_from_id(text_id)
        return text, text_id

    print("ID must be in range [1,6000]")
    sys.exit(1)


def load_based_on_difficulty(difficulty_level=random.randrange(1, 6)):
    """
    Load text of given difficulty from database if parameter is passed.

    Defaults to random difficulty level when none is provided.

    Args:
        difficulty_level (int): difficulty leven in a range of 1 - 5

    Returns:
        (str, int): Tuple of text content followed by DB row identifier.
    """
    max_level = 5

    if 1 <= difficulty_level <= max_level:
        # Each difficulty section has 6000/5 = 1200 texts each
        upper_limit = difficulty_level * 1200
        lower_limit = upper_limit - 1200 + 1

        text_id = random.randrange(lower_limit, upper_limit + 1)
        text = mitype.database.fetch_text_from_id(text_id)

        return text, text_id

    print("Select a difficulty level in range [1,5]")
    sys.exit(2)


def show_history(N):
    N = int(N)
    history_file = 'mitype_history.csv'
    history_path = os.path.join(os.path.expanduser('~'), history_file)
    try:
        with open(history_path, 'r') as file:
            history_reader = csv.reader(file)
            next(history_reader)

            data = list(history_reader)
            no_of_records = len(data)

            if N >= len(data) or N == -1:
                print(f"\nLast {no_of_records} records: ")
                print("ID\tWPM\tDATE\t\tTIME")

                for i in range(no_of_records):
                    print(data[i][0] + '\t' + data[i][1] + '\t' + data[i][2] + '\t' + data[i][3])

                print()
            else:
                print(f"\nLast {N} records: ")
                print("ID\tWPM\tDATE\t\tTIME")
                for i in range(no_of_records-N, no_of_records):
                    print(data[i][0] + '\t' + data[i][1] + '\t' + data[i][2] + '\t' + data[i][3])

                print()

    
    except FileNotFoundError:
        
        print("No records found!")
        print("Take the test atleast once before viewing history.")
