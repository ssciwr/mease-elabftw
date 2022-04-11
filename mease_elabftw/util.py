import elabapy
import os
from requests.exceptions import HTTPError

url = "https://elabftw.uni-heidelberg.de"


def handle_http_error(http_error, experiment_id=None):
    """
    Unified error hanlding, for http and wrong id errors.

    :param http_error: Error object.
    :type http_error: HTTPError
    :param experiment_id: The experiment number given by the user for which an error was raised. , defaults to None
    :type experiment_id: int, optional
    """
    if http_error.response.status_code == 400:
        raise RuntimeError(f"Could not connect to {url} - do you have a valid token?")
    elif experiment_id is not None and http_error.response.status_code == 403:
        raise RuntimeError(
            f"Experiment with id {experiment_id} not found - do you have the correct id?"
        )
    else:
        raise http_error


def get_manager():
    """
    Verify that a token is given and creates an elabapy Manager object.

    :raises RuntimeError: Error when no token is in the env variables.
    :return: The manager object to collect the data.
    :rtype: elabapy.Manager
    """
    token = os.environ.get("ELABFTW_TOKEN")
    if token is None:
        raise RuntimeError(
            "The ELABFTW_TOKEN environment variable needs to be set to your eLabFTW access token."
        )
    return elabapy.Manager(endpoint=url + "/api/v1/", token=token)


def get_experiment(experiment_id):
    """
    Get the experiment corresponding to the given id through the elabapy Manager.

    :param experiment_id: user defined experiment id.
    :type experiment_id: int
    :return: Experiment Data
    :rtype: dict
    """
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
    """
    Get all experiments accesible with the current token.

    :return: All experiments
    :rtype: list of dict
    """
    manager = get_manager()
    try:
        # note: offset is ignored, so for now just setting limit to a large value and making a single request
        return manager.get_all_experiments({"limit": 999, "offset": 0})
    except HTTPError as e:
        handle_http_error(e)
