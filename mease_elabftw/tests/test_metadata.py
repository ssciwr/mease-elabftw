import pytest
import mease_elabftw

valid_experiment_id = 156
valid_experiment_id_no_metadata = 163
invalid_experiment_id = 9999999999999


def test_get_valid_id():
    data = mease_elabftw.get_metadata(valid_experiment_id)
    assert len(data.keys()) == 2
    start_time = data.get("Session start time")
    assert start_time["type"] == "date"
    assert start_time["value"] == "2021-01-01"
    description = data.get("Session description")
    assert description["type"] == "text"
    assert description["value"] == "description of session"


def test_get_no_token(monkeypatch):
    monkeypatch.delenv("ELABFTW_TOKEN")
    with pytest.raises(Exception) as exception_info:
        data = mease_elabftw.get_metadata(valid_experiment_id)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "The ELABFTW_TOKEN environment variable needs to be set to your eLabFTW access token."
    )


def test_get_invalid_token(monkeypatch):
    monkeypatch.setenv("ELABFTW_TOKEN", "abc123")
    with pytest.raises(Exception) as exception_info:
        data = mease_elabftw.get_metadata(valid_experiment_id)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "Could not connect to https://elabftw.uni-heidelberg.de - do you have a valid token?"
    )


def test_get_invalid_id(monkeypatch):
    with pytest.raises(Exception) as exception_info:
        data = mease_elabftw.get_metadata(invalid_experiment_id)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == f"Experiment with id {invalid_experiment_id} not found - do you have the correct id?"
    )


def test_get_valid_id_no_metadata():
    with pytest.raises(Exception) as exception_info:
        data = mease_elabftw.get_metadata(valid_experiment_id_no_metadata)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == f"Experiment with id {valid_experiment_id_no_metadata} doesn't contain any metadata."
    )
