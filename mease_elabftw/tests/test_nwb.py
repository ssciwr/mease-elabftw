import pytest
import mease_elabftw
import test_ids
from pathlib import Path
import json
import jsonschema


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
    ecephys = data.get("Ecephys")
    assert len(ecephys["ElectrodeGroup"]) == 1
    electrode_group = ecephys["ElectrodeGroup"][0]
    assert electrode_group["name"] == "H3"
    assert electrode_group["location"] == "S1"
    # validate json using nwb schema
    schema_file_path = (
        Path(__file__).parent / "metadata_ecephys.schema.json"
    ).resolve()
    with schema_file_path.open() as schema_file:
        print(data)
        jsonschema.validate(instance=data, schema=json.load(schema_file))
