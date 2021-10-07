import pytest
import mease_elabftw


def test_list_experiments():
    lines = mease_elabftw.list_experiments()
    assert len(lines) > 10


def test_list_experiments_with_owner():
    lines = mease_elabftw.list_experiments("Liam")
    assert len(lines) == 2
    assert (
        lines[0]
        == "163: test fake experiment without json metadata (Liam Keegan, 2021-10-07)"
    )


def test_list_experiments_no_token(monkeypatch):
    monkeypatch.delenv("ELABFTW_TOKEN")
    with pytest.raises(Exception) as exception_info:
        data = mease_elabftw.list_experiments("Liam")
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "The ELABFTW_TOKEN environment variable needs to be set to your eLabFTW access token."
    )


def test_list_experiments_invalid_token(monkeypatch):
    monkeypatch.setenv("ELABFTW_TOKEN", "abc123")
    with pytest.raises(Exception) as exception_info:
        data = mease_elabftw.list_experiments("Liam")
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "Could not connect to https://elabftw.uni-heidelberg.de - do you have a valid token?"
    )
