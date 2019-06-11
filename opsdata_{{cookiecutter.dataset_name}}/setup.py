"""
The setup script for the dataset.
"""
import sys
from pathlib import Path

from setuptools import setup, find_packages

# make sure python 3 is running
if sys.version_info.major < 3:
    raise Exception(f"Obsplus datasets cannot be run on python 2")


# get path references
here = Path(__file__).absolute().parent
version_file = here / "opsdata_{{ cookiecutter.dataset_name }}" / "version.py"


# --- get version
with version_file.open() as fi:
    content = fi.read().split("=")[-1].strip()
    __version__ = content.replace('"', "").replace("'", "")


# get requirements
requirements = open("requirements.txt")
test_requirements = open("tests/requirements.txt")

license_classifiers = {"BSD license": "License :: OSI Approved :: BSD License"}

setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email="{{ cookiecutter.email }}",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="{{ cookiecutter.dataset_description }}",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "obsplus.datasets": [
            "{{ cookiecutter.dataset_name }}=opsdata_{{ cookiecutter.dataset_name }}.core"
        ]
    },
    install_requires=requirements,
    license="BSD",
    include_package_data=True,
    name="opsdata_{{ cookiecutter.dataset_name }}",
    packages=find_packages(include=["ops_dataset{{ cookiecutter.dataset_name }}"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.dataset_name }}",
    version=__version__,
    zip_safe=False,
)
