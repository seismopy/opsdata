"""
Configs for tests
"""
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def project_path():
    """ return the path to opsdata_template directory, """
    return Path(__file__).parent.parent
