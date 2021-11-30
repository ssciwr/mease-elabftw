from .metadata import get_metadata
from .linked_items import get_linked_items
from .util import get_experiment
import json


def dict_to_string(dict):
    str = ""
    for key, value in dict.items():
        str += f"  * {key}: {value}\n"
    return str


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
            virus += f"{item['title']}:\n{dict_to_string(item['data_dict'])}"
            metadata["NWBFile"]["virus"] = virus
        elif category == "silicon probe":
            f = json.loads(item.get("metadata", "{}")).get("extra_fields")
            metadata["Ecephys"]["ElectrodeGroup"] = {
                "name": f["ElectrodeGroup.name"]["value"],
                "location": f["ElectrodeGroup.location"]["value"],
            }
    return metadata
