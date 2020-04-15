"""Keypress"""

import curses.ascii


def is_escape(key):
    """Detect ESC key. This is used to exit the application.

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


def is_backspace(key):
    """Detect BACKSPACE key. This is used to exit the application.

    Args:
        key (string): Individual characters are returned as 1-character
                        strings, and special keys such as function keys
                        return longer strings containing a key name such as
                        KEY_UP or ^G.

    Returns:
        bool: Returns true if pressed key is BACKSPACE key.
                Returns false otherwise."""
    if key in ("KEY_BACKSPACE", "\b", "\x7f"):
        return True
    return key in (curses.KEY_BACKSPACE, curses.KEY_DC)


def is_null(key):
    """Detect null keys like super key."""
    if isinstance(key, str) and len(key) == 1:
        return ord(key) == 0
    return key == ""


def is_enter(key):
    """Detect enter key"""
    return key == "\n"


def is_resize(key):
    """Detect is terminal was resized"""
    return key == "KEY_RESIZE"


def is_valid_initial_key(key):
    """Detect if the pressed key is a valid key to start timer"""
    if (
        is_resize(key)
        or is_null(key)
        or is_enter(key)
        or is_escape(key)
        or is_backspace(key)
    ):
        return False
    return True
