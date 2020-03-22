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
    if len(key) == 1:
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
    if key in ("KEY_BACKSPACE", "\b"):
        return True
    if len(key) == 1:
        return ord(key) == curses.ascii.BS
    return False


def is_null(key):
    """Detect null keys like super key."""
    if len(key) == 1:
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
    if len(key) == 1:
        return ord(key) in range(32, 127)
    return False
