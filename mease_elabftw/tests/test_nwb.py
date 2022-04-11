import pytest
import mease_elabftw
import test_ids
from pathlib import Path
import json
import jsonschema
from pynwb import NWBFile, validate, NWBHDF5IO
from datetime import datetime
from dateutil import tz


def test_get_nwb_metadata():
    data = mease_elabftw.get_nwb_metadata(test_ids.valid_experiment)
    assert len(data.keys()) == 4

    # NWBFile section
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

    # Subject section
    subject = data.get("Subject")
    assert subject["sex"] == "unknown"
    assert subject["weight"] == "2"
    assert subject["genotype"] == "Nt1Cre-ChR2-EYFP"
    assert subject["subject_id"] == "xy1"
    assert subject["description"] == "test mouse"

    # Validate json using nwb schema
    # (remove "Other" section before validating)
    del data["Other"]
    schema_file_path = (
        Path(__file__).parent / "metadata_ecephys.schema.json"
    ).resolve()
    with schema_file_path.open() as schema_file:
        print(data)
        jsonschema.validate(instance=data, schema=json.load(schema_file))


def test_NWB_creation(tmp_path):
    data = mease_elabftw.get_nwb_metadata(test_ids.valid_experiment)
    nwbfile_dict = data.get("NWBFile")
    # pynwb only takes session_start_time as a datetime object.
    nwbfile_dict["session_start_time"] = datetime.fromisoformat(
        nwbfile_dict["session_start_time"]
    )

    nwbfile = NWBFile(**nwbfile_dict)
    # write the nwbfile to the plate, this is necessary for the validation.
    file = tmp_path / "test.nwb"
    io = NWBHDF5IO(file, mode="w")
    io.write(nwbfile)
    # This validate function behaves a bit unintuitively, when everything is fine it returns an empty list,
    # if not it raises an exception or returns a list of warnings.
    if validate(io) != []:
        raise Exception(
            f"nwbfile could not be validated, raised errors are {validate(io)}"
        )
    io.close()

    # a simple assertion of the fied and our previously created dict is not possible as pynwb creates additional fields.
    # Because of this only keys in the original dict are compared. The time series has to be excluded as it is also altered by pynwb.
    for key in nwbfile_dict.keys():
        if key != "session_start_time":
            assert nwbfile.fields[key] == nwbfile_dict[key]
