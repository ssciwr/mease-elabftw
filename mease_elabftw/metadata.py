import elabapy
import json
import os
from requests.exceptions import HTTPError


def get(experiment_id):
    token = os.environ.get("ELABFTW_TOKEN")
    manager = elabapy.Manager(
        endpoint="https://elabftw.uni-heidelberg.de/api/v1/", token=token
    )
    experiment = manager.get_experiment(experiment_id)
    return json.loads(experiment["metadata"])
