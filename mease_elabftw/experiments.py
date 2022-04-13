from .util import get_experiments, get_manager, handle_http_error
from datetime import datetime
from requests.exceptions import HTTPError
import os
import logging

logger = logging.getLogger("mease-elabftw")


def list_experiments(owner=""):
    """
    Filter experiments by owner.

    If no owner is specified, returns all experiments.

    :param owner: Fullname of the experiment author, defaults to ""
    :type owner: str, optional
    :return: id, title, fullname and date of all applicable experiments.
    :rtype: list of str
    """
    output = []
    experiments = get_experiments()
    for e in experiments:
        fullname = e.get("fullname", "")
        if owner in fullname:
            id = e.get("id", "")
            title = e.get("title", "")
            date = datetime.strptime(e.get("date", ""), "%Y%m%d")
            output.append(f"{id}: {title} ({fullname}, {date:%Y-%m-%d})")
    logger.debug(f"Experiment list for {owner}: \n {output}")
    return output


def upload_file(experiment_id, filename):
    """
    Upload a file to the web service under a specific experiment id.

    :param experiment_id: The experiment id given by the user.
    :type experiment_id: int
    :param filename: Filename to store on the server.
    :type filename: str
    :raises RuntimeError: Raise error if upload is not possible.
    :return: The upload id.
    :rtype: int
    """

    manager = get_manager()
    try:
        with open(os.path.join(os.getcwd(), filename), "r+b") as f:
            status = manager.upload_to_experiment(experiment_id, {"file": f})
        if status.get("result") == "success":
            upload_id = status.get("id")
            logger.info(
                f"Uploaded file {filename} to experiment {experiment_id} with upload id {upload_id}"
            )

            return upload_id
        else:
            message = f"Could not upload file {filename} to experiment {experiment_id}"
            logger.error(message + f"\n The upload status is: {status.get('result')}")
            raise RuntimeError(message)
    except HTTPError as e:
        handle_http_error(e, experiment_id)
