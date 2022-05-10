import pytest
import mease_elabftw
import test_ids


def test_list_experiments():
    lines = mease_elabftw.list_experiments()
    assert len(lines) > 10


def test_list_experiments_with_owner():
    lines = mease_elabftw.list_experiments("Liam")
    assert len(lines) == 3
    assert (
        lines[1]
        == "163: test fake experiment without json metadata (Liam Keegan, 2021-10-07)"
    )


def test_list_experiments_no_token(monkeypatch):
    monkeypatch.delenv("ELABFTW_TOKEN")
    with pytest.raises(Exception) as exception_info:
        lines = mease_elabftw.list_experiments("Liam")
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "The ELABFTW_TOKEN environment variable needs to be set to your eLabFTW access token."
    )


def test_list_experiments_invalid_token(monkeypatch):
    monkeypatch.setenv("ELABFTW_TOKEN", "abc123")
    with pytest.raises(Exception) as exception_info:
        lines = mease_elabftw.list_experiments("Liam")
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "Could not connect to https://elabftw.uni-heidelberg.de - do you have a valid token?"
    )


def test_upload_file():
    # For now skip this test, as there is no way to delete the uploaded file again using the API
    return
    with open("test.txt", "w") as file:
        file.write("Test file to upload")
    upload_id = mease_elabftw.upload_file(test_ids.valid_experiment, "test.txt")
    assert upload_id > 0


def test_upload_file_invalid_id():
    with open("test.txt", "w") as file:
        file.write("Test file to upload")
    with pytest.raises(Exception) as exception_info:
        upload_id = mease_elabftw.upload_file(test_ids.invalid_experiment, "test.txt")
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == f"Experiment with id {test_ids.invalid_experiment} not found - do you have the correct id?"
    )
