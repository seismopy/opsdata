"""
Tests for creating an empty dataset.
"""
from pathlib import Path
from shlex import split
from subprocess import run

import pytest
from click.testing import CliRunner

runner = CliRunner()

# the default name
NAME = "testdataset"

CONFIG_STR = """
default_context:
    full_name: "{full_name}"
    email: "{email}"
    github_username: "{github_username}"
    dataset_name: "{dataset_name}"
    dataset_description: "{dataset_description}"
    pypi_username: "{pypi_username}"
    version: "0.1.0"
abbreviations:
    gh: https://github.com
    bb: https://bitbucket.org
"""


def _make_config_files(path, **kwargs):
    """ Make a config file and save it to path. """
    defaults = dict(
        full_name='Bob Ham',
        email='example@gmail.com',
        github_username='bobh',
        dataset_name=NAME,
        dataset_description='A cool dataset for sure',
        pypi_username='BoH',
        version='0.1.0',
    )
    defaults.update(kwargs)
    save_str = CONFIG_STR.format(**defaults)

    path = Path(path)
    with path.open('w') as fi:
        fi.write(save_str)


@pytest.fixture(scope='class')
def temp_dirs(tmp_path_factory):
    """ Create two temporary directories. """
    p1 = Path(tmp_path_factory.mktemp('default'))
    p2 = Path(tmp_path_factory.mktemp('configs'))
    return p1, p2


@pytest.fixture(scope='class')
def new_dataset_default(temp_dirs, project_path):
    """ Create a new (empty) dataset and return its path """
    config_path = temp_dirs[1] / 'config.txt'
    out_path = temp_dirs[0]
    _make_config_files(config_path)
    cmd = (f'cookiecutter {project_path} --output-dir {out_path} '
           f'--config-file {config_path} --no-input')
    run(split(cmd), check=True)
    return out_path


@pytest.fixture(scope='class')
def pip_installed_dataset(new_dataset_default):
    """ install the new dataset with pip """
    path = new_dataset_default / ('opsdata_' + NAME)
    cmd = f'pip install -e {path}'
    run(split(cmd), check=True)
    yield new_dataset_default
    run(split(f"pip uninstall -y opsdata_{NAME}"), check=True)


class TestEmptyDataset:
    """ tests for the empty dataset. """

    def test_exists(self, pip_installed_dataset):
        """ Ensure the new directory exists. """
        assert pip_installed_dataset.exists()

    def test_load_dataset(self, pip_installed_dataset):
        """ Ensure the dataset can be loaded by obsplus """
        cmd1 = (f'import obsplus; ds = obsplus.load_dataset("{NAME}"); '
                'assert(isinstance(ds, obsplus.DataSet))')
        cmd = (f"python -c '{cmd1}'")
        # if this doesn't raise the dataset is discoverable
        run(split(cmd), check=True)

    def test_run_dataset_tests(self, pip_installed_dataset):
        """ Ensure the generated tests also pass. """
        cmd = f'pytest {pip_installed_dataset}'
        run(split(cmd), check=True)

