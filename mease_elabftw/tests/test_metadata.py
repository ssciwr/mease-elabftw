import mease_elabftw.metadata as elm


def test_import():
    return


def test_get_experiment():
    assert len(elm.get_experiment(156)) > 0
