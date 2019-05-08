"""
Tests for creating an empty dataset.
"""
from subprocess import run
from shlex import split

import pytest


@pytest.fixture(scope='class')
def new_dataset(project_path):
    """ Create a new (empty) dataset and pip install it. """
    cmd = f'cookiecutter {project_path}'
