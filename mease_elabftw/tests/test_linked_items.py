import pytest
import mease_elabftw
import test_ids
import json


def test_get_linked_items():
    items = mease_elabftw.get_linked_items(test_ids.valid_experiment)
    assert len(items) == 5
    # dye
    assert items[0]["category"] == "dye"
    assert items[0]["title"] == "DiO green"
    d = items[0]["data_dict"]
    assert len(d.items()) == 2
    assert d["origin"] == "ThermoFisher"
    assert d["catalog number"] == "V22886"
    # mouse line
    assert items[1]["category"] == "mouse line"
    assert items[1]["title"] == "wild type"
    d = items[1]["data_dict"]
    assert len(d.items()) == 6
    # silicon probe
    assert items[2]["category"] == "silicon probe"
    assert items[2]["title"] == "Untitled"
    print(items[2])
    d = json.loads(items[2].get("metadata", "{}")).get("extra_fields")
    assert d["ElectrodeGroup.name"]["value"] == "H3"
    assert d["ElectrodeGroup.location"]["value"] == "S1"
    # virus
    assert items[4]["category"] == "virus"
    assert items[4]["title"] == "AAVretr Flpo"
    d = items[4]["data_dict"]
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
