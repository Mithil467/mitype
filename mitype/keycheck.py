"""Keypress."""

import curses.ascii
import sys


def is_escape(key):
    """Detect ESC key.

    This is used to exit the application.

    Args:
        key (string): Individual characters are returned as 1-character
            strings, and special keys such as function keys
            return longer strings containing a key name such as
            KEY_UP or ^G.

    Returns:
        bool: Returns true if pressed key is ESC key.
            Returns false otherwise.
    """
    if isinstance(key, str) and len(key) == 1:
        return ord(key) == curses.ascii.ESC
    return False


def is_ignored(key):
    if sys.version_info[0] < 3:
        return key.startswith("KEY") or (len(key) > 1 and key.startswith("k"))
    else:
        return isinstance(key, int)


def is_backspace(key):
    """Detect BACKSPACE key.

    This is used to exit the application.

    Args:
        key (string): Individual characters are returned as 1-character
            strings, and special keys such as function keys
            return longer strings containing a key name such as
            KEY_UP or ^G.

    Returns:
        bool: Returns true if pressed key is BACKSPACE key.
            Returns false otherwise.
    """
    if key in ("KEY_BACKSPACE", "\b", "\x7f"):
        return True
    return key in (curses.KEY_BACKSPACE, curses.KEY_DC)


def is_null(key):
    """Detect null keys like super key.

    Args:
        key (str): Character to check.

    Returns:
        bool: `True` if "null" key or `False` otherwise.
    """
    if isinstance(key, str) and len(key) == 1:
        return ord(key) == 0
    return key == ""


def is_enter(key):
    """Detect enter key.

    Args:
        key (str): Character to check.

    Returns:
        bool: `True` if line feed or `False` otherwise.
    """
    return key == "\n"


def is_resize(key):
    """Detect is terminal was resized.

    Args:
        key (str): Character to check.

    Returns:
        bool: `True` if resize request or `False` otherwise.
    """
    return key == "KEY_RESIZE"


def is_valid_initial_key(key):
    """Detect if the pressed key is a valid key to start timer.

    Args:
        key (str): Character to check.

    Returns:
        bool: `True` if key is a valid text character or `False` otherwise.
    """
    if (
        is_resize(key)
        or is_null(key)
        or is_enter(key)
        or is_escape(key)
        or is_backspace(key)
        or is_ignored(key)
    ):
        return False
    return True
