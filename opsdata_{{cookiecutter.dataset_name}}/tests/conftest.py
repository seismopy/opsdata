"""
Useful description.
"""
from pathlib import Path

import obsplus
import pytest

DATASET_NAME = "{{ cookiecutter.dataset_name }}"


@pytest.fixture(scope='session')
def dataset():
    """Ensure the dataset is downloaded and return."""
    return obsplus.load_dataset(DATASET_NAME)


@pytest.fixture(scope='session', autouse=True)
def create_file_hashes(dataset):
    """A fixture to generate the file hashes if they don't exist."""
    expected = Path(dataset.source_path) / dataset._hash_filename
    if not expected.exists():
        dataset.create_sha256_hash(path=dataset.source_path)
