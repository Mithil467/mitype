from copy import copy
from unittest.mock import MagicMock


def test_perfect_accuracy(mocked_app):
    win = MagicMock()

    for character in copy(mocked_app.text):
        mocked_app.typing_mode(win, character)
    assert mocked_app.accuracy == 100


def test_error_during_typing(mocked_app):
    win = MagicMock()

    text = 2 * ["z", "KEY_BACKSPACE"] + list(copy(mocked_app.text))
    print("list is ", mocked_app.text)
    for character in copy(text):
        mocked_app.typing_mode(win, character)
    assert mocked_app.accuracy == 98.75


def test_same_character_after_typing(mocked_app):
    win = MagicMock()

    text = list(copy(mocked_app.text)) + list(mocked_app.text[-1] * 10)

    for character in copy(text):
        mocked_app.typing_mode(win, character)
    assert mocked_app.accuracy == 100
