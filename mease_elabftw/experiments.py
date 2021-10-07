from .util import get_experiments
from datetime import datetime


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
