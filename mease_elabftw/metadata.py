import json
from .util import get_experiment
import logging

logger = logging.getLogger("mease-elabftw")


def get_metadata(experiment_id):
    """
    Get the experiment metadata corresponding to the given id through the elabapy Manager.

    :param experiment_id: User defined experiment id
    :type experiment_id: int
    :return: Experiment metadata
    :rtype: dict
    """
    experiment = get_experiment(experiment_id)
    logger.info(f"Getting metadata from {experiment_id}")
    metadata = json.loads(experiment.get("metadata", "{}")).get("extra_fields")
    logger.debug(f"Collected metadata: : \n \t {json.dumps(metadata, indent = 4)}")

    if not metadata:
        message = f"Experiment with id {experiment_id} doesn't contain any metadata."
        logger.error(message)

        raise RuntimeError(message)
    return metadata
