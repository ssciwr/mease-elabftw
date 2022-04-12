from .metadata import get_metadata
from .linked_items import get_linked_items
from .util import get_experiment
import json
from datetime import datetime
import re


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


def get_nwb_metadata(experiment_id):
    """
    Collect metadata information from the given experiment id.
    Ensure data is stored under the correct keys.

    Note for special cases:
    - session_start_time will be converted to datetime.datetime object.
    - subject.date_of_birth will be converted to datetime.datetime object.
    - subject.weight will be converted into string with unit attached.



    :param experiment_id: The experiment id given by the user.
    :type experiment_id: int
    :return: Nested dictionary with all required metadata.
    :rtype: dict
    """

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
    # Session start time needs to be converted to datatime for pynwb.
    # This conversion loggs a warning, as no timezone is specified. It assumes local time, which is fine for now.
    metadata["NWBFile"]["session_start_time"] = datetime.fromisoformat(
        experiment["datetime"]
    )
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
                print(key, value["value"])
                # Date of birth needs to be converted to datetime.
                if key.split(".")[1] == "date_of_birth":
                    metadata["Subject"][key.split(".")[1]] = datetime.fromisoformat(
                        value["value"]
                    )
                # Mouse weight must always be given in g and is automatically converted to kg for pynwb.
                elif key.split(".")[1] == "weight":
                    weight_str = value["value"].lower()

                    # Check if letters are present in string:
                    if (
                        weight_str.islower()
                    ):  # Not sure how to test this as I can't put a letter in the mouse file.

                        weight_str, unit_str = re.split(
                            r"([a-z])", weight_str, 1, flags=re.I
                        )
                        weight_str = weight_str.strip()
                        unit_str = unit_str.strip()
                        if unit_str == "g" or unit_str == "kg":
                            weight_str = weight_str + " " + unit_str

                        else:
                            # add this to loggs
                            weight_str = weight_str + " g"

                    # if no letters are present strip white space and add " g" for grams.
                    else:
                        weight_str = weight_str.strip()
                        weight_str = weight_str + " g"

                    metadata["Subject"][key.split(".")[1]] = weight_str

                else:
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
    return metadata
