import json
from .util import get_experiment


def get_metadata(experiment_id):
    experiment = get_experiment(experiment_id)
    metadata = json.loads(experiment.get("metadata", "{}"))
    if not metadata:
        raise RuntimeError(
            f"Experiment with id {experiment_id} doesn't contain any metadata."
        )
    return metadata
