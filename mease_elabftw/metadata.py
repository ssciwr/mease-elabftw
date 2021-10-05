import elabapy
import json
import os
from requests.exceptions import HTTPError


def get_experiment(id):
    token = os.environ.get("ELABFTW_TOKEN")
    print(token)
    manager = elabapy.Manager(
        endpoint="https://elabftw.uni-heidelberg.de/api/v1/", token=token
    )
    return manager.get_experiment(id)
