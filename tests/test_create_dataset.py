"""
Tests for creating an empty dataset.
"""
from pathlib import Path
from shlex import split
from subprocess import run, PIPE

import pytest
from click.testing import CliRunner
from cookiecutter.main import cookiecutter

runner = CliRunner()

# the default name
NAME = "testdataset"

CONFIG_STR = """
default_context:
    author_name: "{author_name}"
    email: "{email}"
    dataset_name: "{dataset_name}"
    project_url: "{project_url}"
    dataset_description: "{dataset_description}"
    version: "0.1.0"
abbreviations:
    gh: https://github.com
    bb: https://bitbucket.org
"""


def _path_to_waveform_file(path):
    """ return the path to a simple waveform file. """
    return path / "waveforms" / "somefile.txt"


def _path_to_event_file(path):
    """ return path to event file. """
    return path / "events" / "2017" / "01" / "anotherfile.txt"


def _make_config_files(path, **kwargs):
    """ Make a config file and save it to path. """
    defaults = dict(
        author_name="Bob Ham",
        email="example@gmail.com",
        dataset_name=NAME,
        project_url=f"https://github.com/bob-h/{NAME}",
        dataset_description="A cool dataset for sure",
        version="0.1.0",
    )
    defaults.update(kwargs)
    save_str = CONFIG_STR.format(**defaults)

    path = Path(path)
    with path.open("w") as fi:
        fi.write(save_str)


@pytest.fixture(scope="class")
def temp_dirs(tmp_path_factory):
    """ Create two temporary directories. """
    p1 = Path(tmp_path_factory.mktemp("default"))
    p2 = Path(tmp_path_factory.mktemp("configs"))
    return p1, p2


@pytest.fixture(scope="class")
def new_dataset_default(temp_dirs, project_path):
    """ Create a new dataset and return its path """
    config_path = temp_dirs[1] / "config.txt"
    out_path = temp_dirs[0]
    _make_config_files(config_path)
    cmd = (
        f"cookiecutter {project_path} --output-dir {out_path} "
        f"--config-file {config_path} --no-input"
    )
    run(split(cmd), check=True)
    # path to newly created package
    path = out_path / ("opsdata_" + NAME)
    # a simple file, and then a really nested file
    source_path = path / path.name / NAME
    simple_data = _path_to_waveform_file(source_path)
    nested_file = _path_to_event_file(source_path)
    # create data directories and files
    simple_data.parent.mkdir(exist_ok=True, parents=True)
    with simple_data.open("w") as fi:
        fi.write("data")
    nested_file.parent.mkdir(exist_ok=True, parents=True)
    with nested_file.open("w") as fi:
        fi.write("more data")
    return path


@pytest.fixture(scope="class")
def pip_installed_dataset(new_dataset_default):
    """ install the new dataset with pip """
    cmd = f"pip install {new_dataset_default}"
    run(split(cmd), check=True)
    yield new_dataset_default
    run(split(f"pip uninstall -y {new_dataset_default.name}"), check=True)


class TestDataset:
    """ tests for the empty dataset. """

    @pytest.fixture(scope="class")
    def installed_path(self, pip_installed_dataset):
        """ return the installed path of the new dataset. """
        cmd1 = f'import obsplus; ds = obsplus.load_dataset("{NAME}"); ' "print(ds.data_path)"
        cmd = f"python -c '{cmd1}'"
        # if this doesn't raise the dataset is discoverable
        result = run(split(cmd), check=True, stdout=PIPE)
        return Path(result.stdout.decode("utf-8").rstrip())

    def test_datafiles_exist(self, installed_path):
        """ Determine where the file lives and assert it has the datafiles. """
        wave_file = _path_to_waveform_file(installed_path)
        event_file = _path_to_event_file(installed_path)
        assert wave_file.exists()
        assert event_file.exists()

    def test_exists(self, pip_installed_dataset):
        """ Ensure the new directory exists. """
        assert pip_installed_dataset.exists()

    def test_load_dataset(self, pip_installed_dataset):
        """ Ensure the dataset can be loaded by obsplus """
        cmd1 = (
            f'import obsplus; ds = obsplus.load_dataset("{NAME}"); '
            "assert(isinstance(ds, obsplus.DataSet))"
        )
        cmd = f"python -c '{cmd1}'"
        # if this doesn't raise the dataset is discoverable
        run(split(cmd), check=True)

    def test_run_dataset_tests(self, pip_installed_dataset):
        """ Ensure the generated tests also pass. """
        cmd = f"pytest {pip_installed_dataset}"
        run(split(cmd), check=True)
