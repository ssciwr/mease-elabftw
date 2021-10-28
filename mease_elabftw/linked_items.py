from .util import get_experiment, get_item
from .parsing import html_to_dict


def get_linked_items(experiment_id):
    links = get_experiment(experiment_id).get("links", [])
    items = []
    for link in links:
        item = get_item(link["itemid"])
        item["data_dict"] = html_to_dict(item.get("body", ""))
        items.append(item)
    return items
