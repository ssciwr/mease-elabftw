import pytest
from mease_elabftw.util import convert_weight


def test_convert_weight():

    assert convert_weight(2) == "2 g"
    assert convert_weight(2.23) == "2.23 g"

    assert convert_weight("2") == "2 g"
    assert convert_weight("2 g") == "2 g"
    assert convert_weight("2.23 G") == "2.23 g"
    assert convert_weight("2g") == "2 g"
    assert convert_weight("2 kg") == "2 g"
    assert convert_weight("2kg") == "2 g"
    assert convert_weight("2,0 dfs") == "2,0 g"
