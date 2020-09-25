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


def main():
    """The main method for parsing command line arguments
    and returning text"""
    opt = parse_arguments()
    if opt.version:
        display_version()
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
        help="ID to retreive text from database",
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

    print("Mitype version %s" % mitype.__version__)


def load_text_from_file(file_path):
    """Load file contents"""

    if os.path.isfile(file_path):
        text = open(file_path).read()
        filename = os.path.basename(file_path)
        return (text, filename)

    print("Cannot open file -", file_path)
    sys.exit(0)


def load_from_database(text_id):
    """Load given text from database with given id"""

    row_count = 6000
    if 1 <= text_id <= row_count:
        text = mitype.database.fetch_text_from_id(text_id)
        return (text, text_id)

    print("ID must be in range [1,6000]")
    sys.exit(1)


def load_based_on_difficulty(difficulty_level=random.randrange(1, 6)):
    """Load text of given difficulty from database if parameter is passed.
    Else pick difficulty randomly
    """

    max_level = 5

    if 1 <= difficulty_level <= max_level:
        # Each difficulty section has 6000/5 = 1200 texts each
        upper_limit = difficulty_level * 1200
        lower_limit = upper_limit - 1200 + 1

        text_id = random.randrange(lower_limit, upper_limit + 1)
        text = mitype.database.fetch_text_from_id(text_id)

        return (text, text_id)

    print("Select a difficulty level in range [1,5]")
    sys.exit(2)
