from .util import get_experiments, get_manager, handle_http_error
from datetime import datetime
from requests.exceptions import HTTPError
import os


def list_experiments(owner=""):
    output = []
    experiments = get_experiments()
    for e in experiments:
        fullname = e.get("fullname", "")
        if owner in fullname:
            id = e.get("id", "")
            title = e.get("title", "")
            date = datetime.strptime(e.get("date", ""), "%Y%m%d")
            output.append(f"{id}: {title} ({fullname}, {date:%Y-%m-%d})")
    return output


def upload_file(experiment_id, filename):
    manager = get_manager()
    try:
        with open(os.path.join(os.getcwd(), filename), "r+b") as f:
            status = manager.upload_to_experiment(experiment_id, {"file": f})
        if status.get("result") == "success":
            upload_id = status.get("id")
            print(
                f"Uploaded file {filename} to experiment {experiment_id} with upload id {upload_id}"
            )
            return upload_id
        else:
            raise RuntimeError(
                f"Could not upload file {filename} to experiment {experiment_id}"
            )
    except HTTPError as e:
        handle_http_error(e, experiment_id)
