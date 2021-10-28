from click.testing import CliRunner
from mease_elabftw.scripts.cli import list


def test_cli_list():
    runner = CliRunner()
    result = runner.invoke(list, args="Liam")
    assert result.exit_code == 0
    lines = result.output.split("\n")
    assert len(lines) == 3
    assert lines[0][:4] == "163:"
    assert lines[1][:4] == "156:"
    assert lines[2] == ""
