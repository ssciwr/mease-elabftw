import mease_elabftw


def test_list_experiments():
    lines = mease_elabftw.list_experiments()
    assert len(lines) > 10


def test_list_experiments_with_owner():
    lines = mease_elabftw.list_experiments("Liam")
    assert len(lines) == 2
    assert (
        lines[0]
        == "163: test fake experiment without json metadata (Liam Keegan, 2021-10-07)"
    )
