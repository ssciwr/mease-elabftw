from click.testing import CliRunner
from mease_elabftw.scripts.cli import elabftw_list


def test_elabftw_list():
    runner = CliRunner()
    result = runner.invoke(elabftw_list, args="Liam")
    assert result.exit_code == 0
    lines = result.output.split("\n")
    assert len(lines) == 4
    assert lines[0][:5] == "1128:"
    assert lines[1][:4] == "163:"
    assert lines[2][:4] == "156:"
    assert lines[3] == ""


def test_elabftw_list_no_token(monkeypatch):
    monkeypatch.delenv("ELABFTW_TOKEN")
    runner = CliRunner()
    result = runner.invoke(elabftw_list, args="Liam")
    assert result.exit_code == 1
    assert (
        result.output
        == "The ELABFTW_TOKEN environment variable needs to be set to your eLabFTW access token.\n"
    )
