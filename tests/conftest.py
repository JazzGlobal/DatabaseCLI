""" Shared Test Fixtures """

import pytest
from icecream import ic
from src.database.database import DatabaseProbe


@pytest.fixture()
def database_probe():
    passed_database_probe_obj = DatabaseProbe()
    yield passed_database_probe_obj
    ic(str(passed_database_probe_obj))
