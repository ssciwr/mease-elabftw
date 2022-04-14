from .metadata import get_metadata
from .linked_items import get_linked_items
from .util import get_experiment, convert_weight
import json
from datetime import datetime
from copy import deepcopy
from pynwb import NWBFile, validate, NWBHDF5IO
from pynwb.file import Subject
from tempfile import TemporaryFile
import os

# from .logger import logger as logger
import logging

logger = logging.getLogger("mease-elabftw")


def dict_to_string(dict):
    """
    Custom conversion method for dict to string.
    This adds a bullet point and line break to the dict.


    :param dict: A dict used to store metadata.
    :type dict: dict
    :return: The dict as a string with added * for seperation
    :rtype: str
    """
    str = ""
    for key, value in dict.items():
        str += f"  * {key}: {value}\n"
    return str


def get_raw_nwb_metadata(experiment_id):
    """
    Collect metadata information from the given experiment id.
    Ensure data is stored under the correct keys.

    No conversion will take place in this function.

    Warning: this function should not be used manually, for user workflow see: ``get_nwb_metadata``

    :param experiment_id: The experiment id given by the user.
    :type experiment_id: int
    :return: Nested dictionary with all required metadata.
    :rtype: dict
    """
    logger.info(f"Begin data collection of experiment id: {experiment_id}")

    experiment = get_experiment(experiment_id)
    expmetadata = get_metadata(experiment_id)
    linked_items = get_linked_items(experiment_id)

    metadata = {
        "NWBFile": dict(),
        "Subject": dict(),
        "Ecephys": dict(),
        "Other": dict(),
    }
    metadata["NWBFile"]["session_description"] = experiment["title"]
    metadata["NWBFile"]["identifier"] = experiment["elabid"]
    metadata["NWBFile"]["session_start_time"] = experiment["datetime"]

    metadata["NWBFile"]["experimenter"] = [experiment["fullname"]]
    metadata["NWBFile"][
        "institution"
    ] = "Heidelberg University, Physiology and Pathophysiology"
    metadata["NWBFile"]["lab"] = "Medical Biophysics, Groh/Mease"
    for item in linked_items:
        category = item["category"]
        if category == "virus":
            virus = metadata["NWBFile"].get("virus", "")
            virus += f"{item['title']}:\n{dict_to_string(item['data_dict'])}"
            metadata["NWBFile"]["virus"] = virus
        elif category == "mouse":
            f = json.loads(item.get("metadata", "{}")).get("extra_fields")
            for key, value in f.items():

                metadata["Subject"][key.split(".")[1]] = value["value"]
        elif category == "silicon probe":
            metadata["Other"]["SiliconProbe"] = dict()
            f = json.loads(item.get("metadata", "{}")).get("extra_fields")
            for key, value in f.items():
                val = value["value"]
                if value["type"] == "number":
                    val = float(val)
                metadata["Other"]["SiliconProbe"][key] = val
        elif category == "OptogeneticStimulationSite":
            metadata["Other"]["OptogeneticStimulationSite"] = dict()
            f = json.loads(item.get("metadata", "{}")).get("extra_fields")
            for key, value in f.items():
                val = value["value"]
                if value["type"] == "number":
                    val = float(val)
                metadata["Other"]["OptogeneticStimulationSite"][key.split(".")[1]] = val

    logger.debug(f"Report final metadata: \n" + dict_to_string(metadata))
    return metadata


def get_nwb_metadata(experiment_id):
    metadata = get_raw_nwb_metadata(experiment_id)

    metadata["Subject"]["weight"] = convert_weight(metadata["Subject"]["weight"])

    return metadata


def create_pynwb(experiment_id=None, nwb_metadata=None):

    if nwb_metadata is None:
        nwb_metadata = get_nwb_metadata(experiment_id)

    if experiment_id is None and nwb_metadata is None:
        raise Exception("At least one of experiment_id and nwb_metadata must be given.")

    pynwb_metadata = deepcopy(nwb_metadata)

    # session_start_time needs to be converted to datatime for pynwb
    # This conversion loggs a warning, as no timezone is specified. It assumes local time, which is fine for now.
    pynwb_metadata["NWBFile"]["session_start_time"] = datetime.fromisoformat(
        nwb_metadata["NWBFile"]["session_start_time"]
    )

    logger.info(
        f"Session start time will be converted from string to datetime. \n From "
        + str(nwb_metadata["NWBFile"]["session_start_time"])
        + " to "
        + str(datetime.fromisoformat(nwb_metadata["NWBFile"]["session_start_time"]))
        + ")"
    )

    # Subject date of birth needs to be converted to datetime.
    pynwb_metadata["Subject"]["date_of_birth"] = datetime.fromisoformat(
        nwb_metadata["Subject"]["date_of_birth"]
    )
    logger.info(
        f"mouse date of birth  will be converted from string to datetime. \n From "
        + str(nwb_metadata["Subject"]["date_of_birth"])
        + " to "
        + str(datetime.fromisoformat(nwb_metadata["Subject"]["date_of_birth"]))
        + ")"
    )

    # Subject weight needs to be a string
    pynwb_metadata["Subject"]["weight"] = str(nwb_metadata["Subject"]["weight"]) + " kg"

    # Write pywnb and subject object.

    nwbfile_dict = pynwb_metadata.get("NWBFile")
    subject_dict = pynwb_metadata.get("Subject")

    pynwbfile = NWBFile(**nwbfile_dict)
    subject = Subject(**subject_dict)
    pynwbfile.subject = subject

    return pynwbfile


def validate_pynwb_data(pynwbfile):

    # Make temporary nwb file for validation.
    file = TemporaryFile(suffix=".nwb")
    io = NWBHDF5IO(file, mode="w")
    io.write(pynwbfile)
    # This validate function behaves a bit unintuitively, when everything is fine it returns an empty list,
    # if not it raises an exception or returns a list of warnings.

    if validate(io) != []:
        validation_bool = False
        message = f"nwbfile could not be validated, raised errors are {validate(io)}"
        logger.error(message)
        raise Exception(message)
    else:
        validation_bool = False

        logger.info(f"Succsesfull  validation of nwb file: \n {pynwbfile}")
    io.close()

    return validation_bool
