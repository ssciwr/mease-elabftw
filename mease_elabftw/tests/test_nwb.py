import pytest
import mease_elabftw
import test_ids
from pathlib import Path
import json
import jsonschema

from datetime import datetime
from dateutil import tz
import logging


def test_get_nwb_metadata():

    logger = logging.getLogger("mease-elabftw")
    logger.error("first function")
    data = mease_elabftw.nwb.get_nwb_metadata(test_ids.valid_experiment)

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
    assert subject["weight"] == 0.002
    assert subject["genotype"] == "Nt1Cre-ChR2-EYFP"
    assert subject["subject_id"] == "xy1"
    assert subject["description"] == "test mouse"
    assert subject["date_of_birth"] == "2000-01-01"

    # Convert weight into string for validation
    data["Subject"]["weight"] = str(data["Subject"]["weight"]) + " kg"

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

    mease_elabftw.activate_logger(True)
    mease_elabftw.set_log_level(logging.INFO)
    logger = logging.getLogger("mease-elabftw")

    logger.error("second function")

    nwb_metadata = mease_elabftw.nwb.get_nwb_metadata(test_ids.valid_experiment)

    # get pynwb from id
    pynwb_file_1 = mease_elabftw.nwb.create_pynwb(test_ids.valid_experiment)

    # Get pynwb from nwb_metadata
    pynwb_file_2 = mease_elabftw.nwb.create_pynwb(nwb_metadata=nwb_metadata)

    # assert both methods result in same result.
    nwbfile_dict = nwb_metadata.get("NWBFile")
    subject_dict = nwb_metadata.get("Subject")

    for key in nwbfile_dict.keys():

        if key == "file_creation_date":
            # this will always be different.
            pass
        if key == "subject":
            for subj_keys in subject_dict.keys():
                assert (
                    pynwb_file_1.fields[key].fields[subj_keys]
                    == pynwb_file_2.fields[key].fields[subj_keys]
                )

        else:
            assert pynwb_file_1.fields[key] == pynwb_file_2.fields[key]

    # This might be a solution to transform a pynwb file back to a dict.
    logger.debug({key: pynwb_file_1.fields[key] for key in nwbfile_dict})
    logger.debug({key: pynwb_file_1.subject.fields[key] for key in subject_dict})

    # A simple assertion of the fied and our previously created dict is not possible as pynwb creates additional fields.
    # Because of this only keys in the original dict are compared. The time series has to be excluded as it is also altered by pynwb.
    for key in nwbfile_dict.keys():
        if key == "session_start_time":
            pass  # does not really want to be compared.
            # assert str(pynwb_file_1.fields[key]) == str(datetime.fromisoformat(nwbfile_dict[key]))

        else:
            assert pynwb_file_1.fields[key] == nwbfile_dict[key]

    # Same for the subject

    for key in subject_dict.keys():
        if key == "date_of_birth":
            pass  # does not really want to be compared.
            # assert str(pynwb_file_1.subject.fields[key]) == str(datetime.fromisoformat(subject_dict[key]))

        elif key == "weight":
            assert pynwb_file_1.subject.fields[key] == str(subject_dict[key]) + " kg"

        else:
            assert pynwb_file_1.subject.fields[key] == subject_dict[key]
