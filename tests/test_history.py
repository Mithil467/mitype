import pytest

from mitype import history


@pytest.fixture()
def empty_history_file(monkeypatch, tmp_path):
    history_file = tmp_path / ".mitype_history.csv"
    history_file.touch()

    monkeypatch.setattr(history, "history_file_absolute_path", lambda: history_file)


def test_show_history_no_file(monkeypatch, tmp_path):

    history_file = tmp_path / ".mitype_history.csv"

    monkeypatch.setattr(history, "history_file_absolute_path", lambda: history_file)
    history.show_history(10)


def test_show_history_file_empty(empty_history_file):
    history.show_history(10)
