import sys
import click
from mease_elabftw import list_experiments


@click.command()
@click.argument("owner", required=False, default="")
def elabftw_list(owner):
    """
    Prints a list of eLabFTW experiments belonging to OWNER

    If OWNER is not specified, all experiments are printed.
    """
    try:
        for experiment in list_experiments(owner):
            click.echo(experiment)
    except Exception as e:
        click.echo(e)
        sys.exit(1)
