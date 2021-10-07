import pytest
import mease_elabftw
import test_ids


def test_get_metadata():
    data = mease_elabftw.get_metadata(test_ids.valid_experiment)
    assert len(data.keys()) == 9
    start_time = data.get("ElectrodeGroup name")
    assert start_time["value"] == "ElectrodeGroup"
    description = data.get("Ecephys Device name")
    assert description["value"] == "Device_ecephys"


def test_get_metadata_no_token(monkeypatch):
    monkeypatch.delenv("ELABFTW_TOKEN")
    with pytest.raises(Exception) as exception_info:
        data = mease_elabftw.get_metadata(test_ids.valid_experiment)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "The ELABFTW_TOKEN environment variable needs to be set to your eLabFTW access token."
    )


def test_get_metadata_invalid_token(monkeypatch):
    monkeypatch.setenv("ELABFTW_TOKEN", "abc123")
    with pytest.raises(Exception) as exception_info:
        data = mease_elabftw.get_metadata(test_ids.valid_experiment)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "Could not connect to https://elabftw.uni-heidelberg.de - do you have a valid token?"
    )


def test_get_metadata_invalid_id(monkeypatch):
    with pytest.raises(Exception) as exception_info:
        data = mease_elabftw.get_metadata(test_ids.invalid_experiment)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == f"Experiment with id {test_ids.invalid_experiment} not found - do you have the correct id?"
    )


def test_get_metadata_no_metadata():
    with pytest.raises(Exception) as exception_info:
        data = mease_elabftw.get_metadata(test_ids.valid_experiment_no_metadata)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == f"Experiment with id {test_ids.valid_experiment_no_metadata} doesn't contain any metadata."
    )
