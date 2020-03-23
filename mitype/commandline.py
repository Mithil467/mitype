"""
Start of app.
Parses command line arguments.
Decides and fills text accordingly.
"""

import argparse
import os
import random
import sys

import mitype

import mitype.database


def parse_arguments():
    """Parse command line arguments"""
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
        help="ID to retreive corresponding text",
    )

    parser.add_argument(
        "-d",
        "--difficulty",
        metavar="N",
        default=2,
        type=int,
        help="Choose difficulty within range 1-5",
    )

    opt = parser.parse_args()
    return opt


def display_version():
    """Display version"""

    print("Mitype %s" % mitype.__version__)


def load_file(file_path):
    """Load file contents"""

    if not os.path.isfile(file_path):
        print("Cannot open file -", file_path)
        sys.exit(0)

    text = open(file_path).read()

    return text


def load_from_database(text_id):
    """Load given text from database referring given id"""

    number_of_entries = 6000

    if text_id not in range(1, number_of_entries + 1):
        print("ID is out of range. Please make sure ID is in range [1,6000]")
        sys.exit(0)

    text = mitype.database.search(text_id)

    return text


def load_based_on_difficulty(difficulty_level = random.randrange(1,6)):
    """Load text of given difficulty from database"""

    max_level = 5

    if difficulty_level not in range(1, max_level + 1):
        print("Select a difficulty level in range [1,5]")
        sys.exit(0)

    # Each difficulty section has 1200 texts each
    upper_limit = difficulty_level * 1200
    lower_limit = upper_limit - 1200

    text_id = random.randrange(lower_limit, upper_limit + 1)
    text = mitype.database.search(text_id)

    return text

def main():
    """The main methor for parsing command line arguments
    and returning text"""
    opt = parse_arguments()

    if opt.version:
        display_version()
        sys.exit(0)

    if opt.file:
        text = load_file(opt.file)

    elif opt.id:
        text = load_from_database(opt.id)

    elif opt.difficulty:
        text = load_based_on_difficulty(opt.difficulty)

    else:
        text = load_based_on_difficulty()

    return text
