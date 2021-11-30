from .metadata import get_metadata
from .linked_items import get_linked_items
from .util import get_experiment
import json


def get_nwb_metadata(experiment_id):
    experiment = get_experiment(experiment_id)
    metadata = get_metadata(experiment_id)
    linked_items = get_linked_items(experiment_id)
    metadata = {"NWBFile": dict(), "Subject": dict(), "Ecephys": dict()}
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
            virus += f"{item['title']}:\n"
            for key, value in item["data_dict"].items():
                virus += f"  * {key}: {value}\n"
            metadata["NWBFile"]["virus"] = virus
    return metadata
