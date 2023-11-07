import pytest
from nornir import InitNornir

@pytest.fixture(scope="session", autouse=True)

def pytestnr():
    pytestnr = InitNornir(config_file="config.yml")
    yield pytestnr
    pytestnr.close_connections()