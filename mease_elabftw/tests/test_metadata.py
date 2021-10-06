import pytest
import mease_elabftw.metadata as elm


def test_get_valid_id():
    data = elm.get(156)
    assert len(data.keys()) == 2
    assert len(data["Custom"].keys()) == 6
    assert len(data["Electrophysiology"].keys()) == 1


def test_get_invalid_id():
    with pytest.raises(Exception) as exception_info:
        data = elm.get(1)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "Experiment with id 1 not found - do you have the correct id?"
    )


def test_get_valid_id_no_metadata():
    with pytest.raises(Exception) as exception_info:
        data = elm.get(145)
    assert exception_info.type == RuntimeError
    assert (
        str(exception_info.value)
        == "Experiment with id 145 doesn't contain any metadata."
    )
