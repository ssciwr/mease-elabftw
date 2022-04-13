import pytest
from mease_elabftw.util import convert_weight
import mease_elabftw


mease_elabftw.activate_logger(True)
mease_elabftw.set_log_level(20)


def test_convert_weight():

    assert convert_weight(2) == 0.002
    assert convert_weight(2.23) == 0.00223
    assert convert_weight("2") == 0.002
    assert convert_weight("2 g") == 0.002
    assert convert_weight("2.23 G") == 0.00223
    assert convert_weight("2g") == 0.002
    assert convert_weight("2 kg") == 2
    assert convert_weight("2kg") == 2
