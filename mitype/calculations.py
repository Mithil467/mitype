"""Calculations"""

from __future__ import division
import math

from mitype import timer


def first_index_at_which_strings_differ(string1, string2):
    """Return index at which there is a change in strings. This is used
    to determine the index upto which text must be dimmed and after which
    must be coloured red (indicating mismatch).

    Args:
        string1 (string): The string which is a combination of
                            last typed keys in a session.
        string2 (string): The string corresponding to sample text.

    Returns:
        integer: Index at which mismatch occurs for the first time.
    """
    length = min(len(string1), len(string2))

    for index in range(length):
        if string1[index] != string2[index]:
            return index
    # Both strings are
    return length


def speed_in_wpm(text, start_time):
    """Calculate typing speed in WPM.

    Args:
        text (list): List of words from sample text.
        start_time (float): The time when user starts typing
        the sample text.

    Returns:
        string: Speed in WPM upto 2 decimal places.
    """
    time_taken = (
        60 * len(text) / timer.get_elasped_minutes_since_first_keypress(start_time)
    )

    return "{0:.2f}".format(time_taken)


def number_of_lines_to_fit_string_in_window(string, window_width):
    """Count number of lines required for displaying text.

    Args:
        string (string): String containing sample text.
        window_width (int): Width of terminal.

    Returns:
        integer: The number of lines required to display sample text
    """
    return int(math.ceil(len(string) / window_width))


def get_space_count_after_ith_word(index, text):
    """Returns number of spaces after a given word.

    Args:
        i (int): Index of word in text list
        text(string): Text without appending extra spaces

    Returns:
        integer: The number of spaces required after ith word
    """
    count = 0
    while index < len(text) and text[index] == " ":
        index += 1
        count += 1
    return count
