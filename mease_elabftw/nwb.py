from .metadata import get_metadata
from .linked_items import get_linked_items
from .util import get_experiment, convert_weight, convert_datetime
import json
from datetime import datetime
from copy import deepcopy
from pynwb import NWBFile, validate, NWBHDF5IO
from pynwb.file import Subject
from tempfile import NamedTemporaryFile
import os
import platform

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
    """
    Collects metadata based on the experiment id and converts the weight to a float.
    This is needed for further export to nwb_converter.

    This function also validates, that all metadata is nwb compatible.


    :param experiment_id:  The experiment id given by the user.

    :return: Final nwb metadata to be passed on.
    :rtype: dict
    """
    metadata = get_raw_nwb_metadata(experiment_id)

    # nwb_converter unfortunately needs the weight to be a float in kg.
    metadata["Subject"]["weight"] = convert_weight(metadata["Subject"]["weight"])

    if validate_pynwb_data(metadata):
        return metadata

    else:
        raise Exception("Could not validate nwb file.")


def create_pynwb(nwb_metadata):
    """
    Transformes the nwb_metadata dict into a pynwb NWBFile.
    For this all dates must be converted to datetime and the weight back into a string.
    This is used for the validation function.


    :param nwb_metadata:  The dictionary that is due to be exported to ``nwb_converter``
    :type nwb_metadata: dict
    :return: The pynwb.NWBFile object.
    :rtype: pynwb.NWBFile
    """

    pynwb_metadata = deepcopy(nwb_metadata)

    # session_start_time needs to be converted to datatime for pynwb
    # This conversion loggs a warning, as no timezone is specified. It assumes local time, which is fine for now.
    pynwb_metadata["NWBFile"]["session_start_time"] = convert_datetime(
        pynwb_metadata["NWBFile"], "session_start_time"
    )

    # Subject date of birth needs to be converted to datetime.
    pynwb_metadata["Subject"]["date_of_birth"] = convert_datetime(
        pynwb_metadata["Subject"], "date_of_birth"
    )

    # Subject weight needs to be a string
    if pynwb_metadata["Subject"]["weight"] != "":
        pynwb_metadata["Subject"]["weight"] = (
            str(nwb_metadata["Subject"]["weight"]) + " kg"
        )

    # Write pywnb and subject object.

    nwbfile_dict = pynwb_metadata.get("NWBFile")
    subject_dict = pynwb_metadata.get("Subject")

    pynwbfile = NWBFile(**nwbfile_dict)
    subject = Subject(**subject_dict)
    pynwbfile.subject = subject

    return pynwbfile


def validate_pynwb_data(nwb_metadata):
    """
    Generates and validates the ``nwb_metadata`` with the ``pynwb`` validation tool.
    This ensures, that only valid nwb data gets passed to the nwb_converter.


    :param nwb_metadata: The dictionary that is due to be exported to ``nwb_converter``
    :type nwb_metadata: dict
    :return: A bool wether or not the validation was successful.
    :rtype: bool
    """

    pynwbfile = create_pynwb(nwb_metadata)

    # Make temporary nwb file for validation.
    if platform.system() == "Windows":
        file = NamedTemporaryFile(mode="w", suffix=".nwb", delete=False)
    else:
        file = NamedTemporaryFile(mode="w", suffix=".nwb")

    io = NWBHDF5IO(file.name, mode="w")
    io.write(pynwbfile)
    # This validate function behaves a bit intuitively, when everything is fine it returns an empty list,
    # if not it raises an exception or returns a list of warnings.

    if validate(io) != []:
        validation_bool = False
        message = f"nwbfile could not be validated, raised errors are {validate(io)}"
        logger.error(message)
        raise Exception(message)
    else:
        validation_bool = True

        logger.info(f"Successful  validation of nwb file: \n {pynwbfile}")
    io.close()

    return validation_bool


def get_sample_nwb_metadata(experiment_id):
    """
    Returns sample NWB metadata for testing purposes without needing an ElabFTW token.

    :param experiment_id: Ignored - this function always returns the same sample metadata

    :return: Sample NWB metadata
    :rtype: dict
    """

    # Output of get_nwb_metadata(156) with a valid elabftw token.
    # Note: this needs to be updated when this output changes.
    return {
        "NWBFile": {
            "session_description": "test fake experiment with json metadata",
            "identifier": "20211001-8b6f100d66f4312d539c52620f79d6a503c1e2d1",
            "session_start_time": "2021-10-01 11:13:47",
            "experimenter": ["Liam Keegan"],
            "institution": "Heidelberg University, Physiology and Pathophysiology",
            "lab": "Medical Biophysics, Groh/Mease",
            "virus": "AAVretr ChR2-tdTomato:\n  * Virus in -80 storage: AAVrg-CAG-hChR2-tdTomato (AAV Retrograde)\n  * Origin: Addgene\n  * Comments: retrograde\n  * Expression Quality: \n  * product number: \nAAVretr Flpo:\n  * Virus in -80 storage: AAVretr EF1a-Flpo\n  * Origin: Addgene\n  * Comments: retrograde Flip\n  * Expression Quality: \n  * product number: 55637-AAVrg\n",
        },
        "Subject": {
            "sex": "unknown",
            "weight": 0.002,
            "genotype": "Nt1Cre-ChR2-EYFP",
            "subject_id": "xy1",
            "description": "test mouse",
            "date_of_birth": "2000-01-01",
        },
        "Ecephys": {},
        "Other": {
            "OptogeneticStimulationSite": {
                "device": "the device",
                "location": "S1: primary somatosensory cortex",
                "description": "laser stimulation",
                "excitation_lambda": "473",
            },
            "SiliconProbe": {
                "Probe identifier:": "1234356",
                "ElectrodeGroup.name": "H5",
                "ElectrodeGroup.description": "a test H5 probe",
            },
        },
    }
