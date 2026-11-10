import pytest

from mitype.commandline import load_text_from_file


def test_missing_file_exits_nonzero(tmp_path):
    """A missing -f file must fail, not exit 0 (success)."""
    missing = tmp_path / "does-not-exist.txt"
    with pytest.raises(SystemExit) as excinfo:
        load_text_from_file(str(missing))
    assert excinfo.value.code != 0


def test_existing_file_loads(tmp_path):
    """Sanity check: an existing file still loads with its basename."""
    sample = tmp_path / "sample.txt"
    sample.write_text("hello world", encoding="utf-8")
    text, text_id = load_text_from_file(str(sample))
    assert text == "hello world"
    assert text_id == "sample.txt"
