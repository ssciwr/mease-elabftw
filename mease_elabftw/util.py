import elabapy
import os
from requests.exceptions import HTTPError

url = "https://elabftw.uni-heidelberg.de"


def handle_http_error(http_error, experiment_id):
    if http_error.response.status_code == 400:
        raise RuntimeError(f"Could not connect to {url} - do you have a valid token?")
    elif http_error.response.status_code == 403:
        raise RuntimeError(
            f"Experiment with id {experiment_id} not found - do you have the correct id?"
        )
    else:
        raise http_error


def get_manager():
    token = os.environ.get("ELABFTW_TOKEN")
    if token is None:
        raise RuntimeError(
            "The ELABFTW_TOKEN environment variable needs to be set to your eLabFTW access token."
        )
    return elabapy.Manager(endpoint=url + "/api/v1/", token=token)


def get_experiment(experiment_id):
    manager = get_manager()
    try:
        return manager.get_experiment(experiment_id)
    except HTTPError as e:
        handle_http_error(e, experiment_id)


def get_item(item_id):
    manager = get_manager()
    try:
        return manager.get_item(item_id)
    except HTTPError as e:
        handle_http_error(e, item_id)


def get_experiments():
    manager = get_manager()
    try:
        # note: offset is ignored, so for now just setting limit to a large value and making a single request
        return manager.get_all_experiments({"limit": 999, "offset": 0})
    except HTTPError as e:
        if e.response.status_code == 400:
            raise RuntimeError(
                f"Could not connect to {url} - do you have a valid token?"
            )
        else:
            raise e
