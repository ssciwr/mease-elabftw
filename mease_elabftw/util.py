import elabapy
import os
from requests.exceptions import HTTPError
import re
import numbers
import json
import logging
from datetime import datetime


logger = logging.getLogger("mease-elabftw")

url = "https://elabftw.uni-heidelberg.de"


def handle_http_error(http_error, experiment_id=None):
    """
    Unified error handling, for http and wrong id errors.

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
    Get all experiments accessible with the current token.

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
    """
    Takes a weight determines if its in g or kg and converts it into a kg float, so that the nwb_converter accepts it.

    If a unit is given in the string it will be extracted and conversion will happen according to the unit.
    When no unit is given gram will be assumed.


    :param weight_str: the weight as either a number or a string with or without unit.
    :type weight_str: str or int
    :return: unitless weight as a float
    :rtype: float
    """

    if isinstance(weight_str, numbers.Number):
        weight_str = str(weight_str)

    weight_str = weight_str.lower()

    if weight_str == "":
        logger.warning("No weight given.")

    # Check if letters are present in string:
    if weight_str.islower():

        # weight_str, unit_str, second_unit = re.split(r"([a-z])", weight_str, 1, flags=re.I)

        match = re.compile("[^\W\d]").search(weight_str)
        weight_str, unit_str = [
            weight_str[: match.start()],
            weight_str[match.start() :],
        ]

        weight_str = weight_str.strip()
        unit_str = unit_str.strip()
        if unit_str == "g":
            weight = float(weight_str) / 1000

        elif unit_str == "kg":
            weight = float(weight_str)

        else:
            weight = float(weight_str) / 1000
            logger.error(
                f"A unit was found but could not be interpreted. Maybe missing a whitespace: {weight_str} is interpreted as g and was conferted to {weight}"
            )

    # if no letters are present strip white space.
    # if number is greater 1 its assumed to be gram, smaller 1 assumed to be kg
    else:
        weight = float(weight_str)
        if weight > 1:
            weight = weight / 1000

    logger.info(f"Weight was changed from {weight_str} to {round(weight,5)}")

    return round(weight, 5)


def convert_datetime(metadata, date_name):
    """
    For pynwb all dates need to be of type datetime.datetime.

    :param date_str: The date as an isoformat string.
    :type date_str: string
    :param date_name: A description of the current transformation. Only needed for error message and logging.
    :type date_name: string
    :return: The datetime as an datetime.datetime object
    :rtype: datetime-datetime
    """
    date_str = metadata[date_name]
    try:
        converted_time = datetime.fromisoformat(date_str)
    except ValueError as e:
        raise ValueError(
            f'An error occurred in converting "{date_name}" to datetime: "{date_str}" is not a valid isoformat datetime.'
        )

    logger.info(
        f"{date_name} will be converted from string to datetime. \n From "
        + str(date_str)
        + f" to {converted_time})"
    )

    return converted_time
