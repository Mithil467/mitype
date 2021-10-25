from unittest.mock import MagicMock

import pytest

from mitype import app, commandline, history
from mitype.database import fetch_text_from_id


@pytest.fixture()
def empty_history_file(monkeypatch, tmp_path):
    history_file = tmp_path / ".mitype_history.csv"
    history_file.touch()

    monkeypatch.setattr(history, "history_file_absolute_path", lambda: history_file)


@pytest.fixture()
def header_only_history_file(monkeypatch, tmp_path):
    history_file = tmp_path / ".mitype_history.csv"

    with history_file.open("w+") as fd:
        fd.write("ID,WPM,DATE,TIME,ACCURACY\n")

    monkeypatch.setattr(history, "history_file_absolute_path", lambda: history_file)


@pytest.fixture()
def history_file(monkeypatch, tmp_path):
    history_file = tmp_path / ".mitype_history.csv"
    monkeypatch.setattr(history, "history_file_absolute_path", lambda: history_file)

    for i in range(100):
        history.save_history(i, 65.3, 89)


@pytest.fixture()
def mocked_curses(monkeypatch):
    monkeypatch.setattr(app, "curses", MagicMock())


@pytest.fixture()
def mocked_app(mocked_curses, monkeypatch):
    text_id = 1758
    text = fetch_text_from_id(text_id)

    monkeypatch.setattr(app, "resolve_commandline_arguments", lambda: (text, text_id))

    myapp = app.App()
    myapp.Color = MagicMock()
    myapp.window_width = 274
    myapp.window_height = 75

    return myapp
