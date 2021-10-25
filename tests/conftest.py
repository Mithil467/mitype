import pytest

from mitype import history


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
