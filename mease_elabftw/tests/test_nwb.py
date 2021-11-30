import pytest
import mease_elabftw
import test_ids


def test_get_nwb_metadata():
    data = mease_elabftw.get_nwb_metadata(test_ids.valid_experiment)
    assert len(data.keys()) == 3
    nwbfile = data.get("NWBFile")
    assert len(nwbfile) == 7
    assert nwbfile["session_description"] == "test fake experiment with json metadata"
    assert nwbfile["identifier"] == "20211001-8b6f100d66f4312d539c52620f79d6a503c1e2d1"
    assert nwbfile["session_start_time"] == "2021-10-01 11:13:47"
    assert len(nwbfile["experimenter"]) == 1
    assert nwbfile["experimenter"][0] == "Liam Keegan"
    assert (
        nwbfile["institution"]
        == "Heidelberg University, Physiology and Pathophysiology"
    )
    assert nwbfile["lab"] == "Medical Biophysics, Groh/Mease"
    # virus items
    viri = nwbfile["virus"].split("\n")
    assert len(viri) == 13
    assert viri[0] == "AAVretr ChR2-tdTomato:"
    assert viri[6] == "AAVretr Flpo:"
