import json
from .util import get_experiment


def get_metadata(experiment_id):
    """
    Get the experiment metadata corresponding to the given ID through the elabapy Manager.

    :param experiment_id: user defined experiment ID
    :type experiment_id: int
    :return: experiment metaata
    :rtype: dict
    """
    experiment = get_experiment(experiment_id)
    metadata = json.loads(experiment.get("metadata", "{}")).get("extra_fields")
    if not metadata:
        raise RuntimeError(
            f"Experiment with id {experiment_id} doesn't contain any metadata."
        )
    return metadata
