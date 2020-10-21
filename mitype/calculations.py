"""Calculations."""

from __future__ import division

import math

from mitype import timer


def first_index_at_which_strings_differ(string1, string2):
    """Return index at which there is a change in strings.

    This is used to determine the index up to which text must be dimmed and
    after which must be coloured red (indicating mismatch).

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
    return length


def speed_in_wpm(text, start_time):
    """Calculate typing speed in WPM.

    Args:
        text (list): List of words from sample text.
        start_time (float): The time when user starts typing
            the sample text.

    Returns:
        string: Speed in WPM up to 2 decimal places.
    """
    time_taken = timer.get_elapsed_minutes_since_first_keypress(start_time)
    wpm = 60 * len(text) / time_taken

    return "{0:.2f}".format(wpm)


def number_of_lines_to_fit_text_in_window(string, window_width):
    """Count number of lines required for displaying text.

    Args:
        string (string): String containing sample text.
        window_width (int): Width of terminal.

    Returns:
        integer: The number of lines required to display sample text
    """
    return int(math.ceil(len(string) / window_width))


def get_space_count_after_ith_word(index, text):
    """Return number of spaces after a given word.

    Args:
        index (int): Index of word in text list
        text(string): Text without appending extra spaces

    Returns:
        integer: The number of spaces required after ith word
    """
    count = 0
    while index < len(text) and text[index] == " ":
        index += 1
        count += 1
    return count


def word_wrap(text, width):
    """Wrap text on the screen according to the window width.

    Returns text with extra spaces which makes the string word wrap.

    Args:
        text (string): Text to wrap.
        width (integer): Width to wrap around.

    Returns:
        str: Return altered text.
    """
    # For the end of each line, move backwards until you find a space.
    # When you do, append those many spaces after the single space.
    for x in range(
        1,
        number_of_lines_to_fit_text_in_window(text, width) + 1,
    ):
        if not (x * width >= len(text) or text[x * width - 1] == " "):
            i = x * width - 1
            while text[i] != " ":
                i -= 1
            text = text[:i] + " " * (x * width - i) + text[i + 1 :]
    return text
