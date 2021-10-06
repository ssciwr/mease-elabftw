import mease_elabftw.metadata as elm


def test_get():
    data = elm.get(156)
    assert len(data.keys()) == 2
    assert len(data["Custom"].keys()) == 6
    assert len(data["Electrophysiology"].keys()) == 1
