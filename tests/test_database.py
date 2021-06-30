import pytest
from src.database.database import DatabaseProbe

@pytest.mark.skip
def test_database_placeholder():
    assert "" == ""


def test_can_generate_database_probe_from_repr(database_probe):
    result = eval(repr(database_probe))
    assert isinstance(result, DatabaseProbe)
