"""Calculations"""

from __future__ import division

import math

from mitype import timer


def change_index(string1, string2):
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
    if len(string1) == 0:
        return 0
    length = min(len(string1), len(string2))
    for i in range(length):
        if string1[i] != string2[i]:
            return i
    return length


def get_wpm(txt, start_time):
    """Calculate typing speed in WPM.

    Args:
        txt (list): List of words from sample text.
        start_time (float): The time when user starts typing
        the sample text.

    Returns:
        string: Speed in WPM upto 2 decimal places.
    """
    time_taken = 60 * len(txt) / timer.get_time_elasped(start_time)
    return "{0:.2f}".format(time_taken)


def count_lines(string, win_width):
    """Count number of lines required for displaying text.

    Args:
        string (string): String containing sample text.
        win_width (int): Width of terminal.

    Returns:
        integer: The number of lines required to display sample text
    """
    return int(math.ceil(len(string) / win_width))


def get_spc_count(i, ogtext):
    count = 0
    # count number of spaces after the ith word in ogtext
    while ogtext[i] == " ":
        i += 1
        count += 1

    return count
