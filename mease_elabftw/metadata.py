import elabapy
import json
import os
from requests.exceptions import HTTPError


def get(experiment_id):
    url = "https://elabftw.uni-heidelberg.de"
    token = os.environ.get("ELABFTW_TOKEN")
    if token is None:
        raise RuntimeError(
            "The ELABFTW_TOKEN environment variable needs to be set to your eLabFTW access token."
        )
    manager = elabapy.Manager(endpoint=url + "/api/v1/", token=token)
    try:
        experiment = manager.get_experiment(experiment_id)
    except HTTPError as e:
        if e.response.status_code == 400:
            raise RuntimeError(
                f"Could not connect to {url} - do you have a valid token?"
            )
        elif e.response.status_code == 403:
            raise RuntimeError(
                f"Experiment with id {experiment_id} not found - do you have the correct id?"
            )
        else:
            raise e
    metadata = experiment["metadata"]
    if metadata is None:
        raise RuntimeError(
            f"Experiment with id {experiment_id} doesn't contain any metadata."
        )
    return json.loads(metadata)
