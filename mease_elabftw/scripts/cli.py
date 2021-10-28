import click
from mease_elabftw import list_experiments


@click.command()
@click.argument("owner", required=False, default="")
def list(owner):
    """
    Prints a list of eLabFTW experiments belonging to OWNER

    If OWNER is not specified, all experiments are printed.
    """
    for experiment in list_experiments(owner):
        print(experiment)
