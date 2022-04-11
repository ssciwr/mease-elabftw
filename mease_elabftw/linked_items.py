from .util import get_experiment, get_item
from .parsing import html_to_dict


def get_linked_items(experiment_id):
    """
    Iterate over all links present in the experiment and collect item information.

    :param experiment_id: The experiment id given by the user.
    :type experiment_id: int
    :return: All the linked items.
    :rtype: list of dict
    """
    links = get_experiment(experiment_id).get("links", [])
    items = []
    for link in links:
        item = get_item(link["itemid"])
        item["data_dict"] = html_to_dict(item.get("body", ""))
        items.append(item)
    return items
