"""Keypress."""

import curses.ascii


def is_escape(key):
    """Detect ESC key.

    This is used to exit the application.

    Args:
        key (str): Individual characters are returned as 1-character
            strings, and special keys such as function keys
            return longer strings containing a key name such as
            KEY_UP or ^G.

    Returns:
        bool: Returns `True` if pressed key is ESC key.
        Returns `False` otherwise.
    """
    if isinstance(key, str) and len(key) == 1:
        return ord(key) == curses.ascii.ESC
    return False


def is_ctrl_c(key):
    """Detect Ctrl+c key combination.

    This is used to exit the application.

    Args:
        key (str): Character to check.

    Returns:
        bool: Returns `True` if Ctrl+c is pressed.
        Returns `False` otherwise.
    """
    return key == "\x03"


def is_ctrl_t(key):
    """Detect Ctrl+t key combination.

    This is used to share results on twitter

    Args:
        key (str): Character to check.
    Returns:
        bool: Return `True` if Ctrl+t is pressed.
        Return `False` otherwise.
    """
    return key == "\x14"


def is_ctrl_backspace(key):
    """Detect Ctrl+backspace key combination.

    Used to delete the last typed word

    Args:
        key (str): Character to check.

    Returns:
        bool: Returns `True` if Ctrl+backspace is pressed.
        Returns `False` otherwise.
    """
    return key == "\x17"


def is_backspace(key):
    """Detect BACKSPACE key.

    Args:
        key (str): Character to check.

    Returns:
        bool: Returns `True` if pressed key is BACKSPACE key.
        Returns `False` otherwise.
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


def is_tab(key):
    """Detect tab key to start mitype again.

    Args:
        key (str): Character to check.

    Returns:
        bool: `True` if tab key or `False` otherwise.
    """
    return key == "\t"


def is_resize(key):
    """Detect if terminal was resized.

    Args:
        key (str): Character to check.

    Returns:
        bool: `True` if resize request or `False` otherwise.
    """
    return key == "KEY_RESIZE"


def is_ignored_key(key):
    """Detect if key press should be ignored.

    Special function keys, page navigation keys must be ignored.

    Args:
        key (str): Character to check.

    Returns:
        bool: Returns `True` if pressed key must be ignored or `False`
        otherwise.
    """
    return isinstance(key, int)


def is_valid_initial_key(key):
    """Detect if the pressed key is a valid key to start timer.

    Args:
        key (str): Character to check.

    Returns:
        bool: `True` if key is a valid text character or `False` otherwise.
    """
    return not (
        is_resize(key)
        or is_null(key)
        or is_enter(key)
        or is_escape(key)
        or is_backspace(key)
        or is_tab(key)
        or is_ignored_key(key)
    )


def is_right_arrow_key(key):
    """Detect right arrow key.

    Args:
        key (str): Character to check.

    Returns:
        bool: `True` if key is a valid text character or `False` otherwise.
    """
    if key == "KEY_RIGHT":
        return True
    return key == curses.KEY_RIGHT


def is_left_arrow_key(key):
    """Detect left arrow key.

    Args:
        key (str): Character to check.

    Returns:
        bool: `True` if key is a valid text character or `False` otherwise.
    """
    if key == "KEY_LEFT":
        return True
    return key == curses.KEY_LEFT
