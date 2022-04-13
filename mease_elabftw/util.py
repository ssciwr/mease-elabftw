import elabapy
import os
from requests.exceptions import HTTPError
import re
import numbers
import json
import logging

logger = logging.getLogger("mease-elabftw")

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
        message = f"Could not connect to {url} - do you have a valid token?"
        logger.error(message)
        raise RuntimeError(message)
    elif experiment_id is not None and http_error.response.status_code == 403:
        message = f"Experiment with id {experiment_id} not found - do you have the correct id?"
        logger.error(message)

        raise RuntimeError(message)
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

        message = "The ELABFTW_TOKEN environment variable needs to be set to your eLabFTW access token."
        logger.error(message)

        raise RuntimeError(message)
    return elabapy.Manager(endpoint=url + "/api/v1/", token=token)


def get_experiment(experiment_id):
    """
    Get the experiment corresponding to the given id through the elabapy Manager.

    :param experiment_id: User defined experiment id.
    :type experiment_id: int
    :return: Experiment Data
    :rtype: dict
    """
    manager = get_manager()
    logger.info(f"Getting experiment {experiment_id}")
    try:
        experiment = manager.get_experiment(experiment_id)
        logger.debug(
            f"Collected experiment:  \n \t{json.dumps(experiment, indent = 4)}"
        )

        return experiment
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


def convert_weight(weight_str):
    if isinstance(weight_str, numbers.Number):
        weight_str = str(weight_str)

    weight_str = weight_str.lower()

    # Check if letters are present in string:
    if weight_str.islower():

        weight_str, unit_str, _ = re.split(r"([a-z])", weight_str, 1, flags=re.I)

        weight_str = weight_str.strip()
        unit_str = unit_str.strip()
        if unit_str == "g" or unit_str == "kg":
            weight_str = weight_str + " " + unit_str

        else:
            # add this to loggs
            weight_str = weight_str + " g"

    # if no letters are present strip white space and add " g" for grams.
    else:
        weight_str = weight_str.strip()
        weight_str = weight_str + " g"
    return weight_str
