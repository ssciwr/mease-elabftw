import pytest
import mease_elabftw
import test_ids


def test_get_linked_items():
    items = mease_elabftw.get_linked_items(test_ids.valid_experiment)
    assert len(items) == 4
    assert items[0]["category"] == "dye"
    assert items[0]["title"] == "DiO green"
    d = items[0]["data_dict"]
    assert len(d.items()) == 2
    assert d["origin"] == "ThermoFisher"
    assert d["catalog number"] == "V22886"
    assert items[1]["category"] == "mouse line"
    assert items[1]["title"] == "wild type"
    d = items[1]["data_dict"]
    assert len(d.items()) == 6
    assert items[3]["category"] == "virus"
    assert items[3]["title"] == "AAVretr Flpo"
    d = items[3]["data_dict"]
    assert len(d.items()) == 5
    assert d["Virus in -80 storage"] == "AAVretr EF1a-Flpo"


def test_get_linked_items_no_token(monkeypatch):
    monkeypatch.delenv("ELABFTW_TOKEN")
    with pytest.raises(Exception) as exception_info:
        items = mease_elabftw.get_linked_items(test_ids.valid_experiment)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "The ELABFTW_TOKEN environment variable needs to be set to your eLabFTW access token."
    )


def test_get_linked_items_invalid_token(monkeypatch):
    monkeypatch.setenv("ELABFTW_TOKEN", "abc123")
    with pytest.raises(Exception) as exception_info:
        items = mease_elabftw.get_linked_items(test_ids.valid_experiment)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "Could not connect to https://elabftw.uni-heidelberg.de - do you have a valid token?"
    )


def test_get_linked_items_invalid_id(monkeypatch):
    with pytest.raises(Exception) as exception_info:
        items = mease_elabftw.get_linked_items(test_ids.invalid_experiment)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == f"Experiment with id {test_ids.invalid_experiment} not found - do you have the correct id?"
    )


def test_get_linked_items_no_items():
    items = mease_elabftw.get_linked_items(test_ids.valid_experiment_no_items)
    assert len(items) == 0
