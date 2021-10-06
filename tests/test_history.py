from mitype import history


def test_show_history_no_file(monkeypatch, tmp_path):

    history_file = tmp_path / ".mitype_history.csv"

    monkeypatch.setattr(history, "history_file_absolute_path", lambda: history_file)
    history.show_history(10)
