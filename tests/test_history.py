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


class TestShowHistory:
    def test_show_history_no_file(self, monkeypatch, tmp_path):

        history_file = tmp_path / ".mitype_history.csv"

        monkeypatch.setattr(history, "history_file_absolute_path", lambda: history_file)
        history.show_history(10)

    def test_show_history_file_empty(self, empty_history_file):
        history.show_history(10)


class TestGetHistoryRecords:
    def test_get_history_no_file(self, monkeypatch, tmp_path):
        history_file = tmp_path / ".mitype_history.csv"

        monkeypatch.setattr(history, "history_file_absolute_path", lambda: history_file)
        assert history.get_history_records(-1) == []

    def test_get_history_empty(self, empty_history_file):
        assert history.get_history_records(-1) == []

    def test_get_history_with_header_only(self, header_only_history_file):
        assert history.get_history_records(-1) == []

    def test_get_history(self, history_file):
        records = history.get_history_records(-1)

        assert len(records) == 100

    def test_get_history_only_some_records(self, history_file):
        records = history.get_history_records(10)

        assert len(records) == 10
